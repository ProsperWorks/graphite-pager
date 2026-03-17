import datetime
from datetime import timezone
import time

import redis
import requests
import requests.exceptions

from graphitepager import __version__
from graphitepager.config import get_config
from graphitepager.description import get_description
from graphitepager.description import missing_target_description
from graphitepager.graphite_data_record import GraphiteDataRecord
from graphitepager.graphite_target import get_records
from graphitepager.level import Level
from graphitepager.redis_storage import RedisStorage
from graphitepager.utils import parse_args

from .notifiers.notifier_proxy import NotifierProxy
from .notifiers.hipchat_notifier import HipChatNotifier
from .notifiers.pagerduty_notifier import PagerdutyNotifier
from .notifiers.pushbullet_notifier import PushBulletNotifier
from .notifiers.slack_notifier import SlackNotifier
from .notifiers.stdout_notifier import StdoutNotifier


def update_notifiers(notifier_proxy, alert, record, graphite_url, circuit_breaker_active=False):
    alert_key = '{} {}'.format(alert.get('name'), record.target)

    alert_level, value = alert.check_record(record)

    description = get_description(
        graphite_url,
        alert,
        record,
        alert_level,
        value
    )

    notifier_proxy.notify(
        alert,
        alert_key,
        alert_level,
        description,
        circuit_breaker_active=circuit_breaker_active
    )
    
    return alert_level


def update_notifiers_missing(notifier_proxy, alert, config, circuit_breaker_active=False):
    graphite_url = config.get('GRAPHITE_URL')
    description = missing_target_description(
        graphite_url,
        alert,
        alert.get('target'),
        Level.NO_DATA,
        None
    )

    notifier_proxy.notify(
        alert,
        alert.get('target'),
        Level.NO_DATA,
        description,
        circuit_breaker_active=circuit_breaker_active
    )
    
    return Level.NO_DATA


def create_notifier_proxy(config):
    redis_url = config.get(
        'REDISTOGO_URL',
        config.get('REDIS_URL', 'redis://localhost:6379/0'))
    STORAGE = RedisStorage(redis, redis_url, config)

    klasses = [
        HipChatNotifier,
        PagerdutyNotifier,
        PushBulletNotifier,
        StdoutNotifier,
        SlackNotifier,
    ]

    notifier_proxy = NotifierProxy()
    for klass in klasses:
        notifier = klass(STORAGE, config)
        if notifier.enabled:
            print('Enabling {0}'.format(notifier._domain))
            notifier_proxy.add_notifier(notifier)

    return notifier_proxy


def verify(args):
    config = get_config(args.config)
    config.alerts()
    print('Valid configuration, good job!')
    return


def run(args):
    print('graphite-pager {0}'.format(__version__))
    config = get_config(args.config)
    alerts = config.alerts()
    notifier_proxy = create_notifier_proxy(config)
    graphite_url = config.get('GRAPHITE_URL')
    heartbeat_seconds = config.get('HEARTBEAT_SECONDS','60')
    http_connect_timeout_s = config.get('GRAPHITE_CONNECT_TIMEOUT_S','0.5')
    http_read_timeout_s    = config.get('GRAPHITE_READ_TIMEOUT_S',   '10')
    http_connect_timeout_s = float(http_connect_timeout_s)
    http_read_timeout_s    = float(http_read_timeout_s)
    # Circuit breaker threshold: fraction of NO_DATA alerts to trigger (default 0.5 = 50%)
    circuit_breaker_threshold = float(config.get('CIRCUIT_BREAKER_THRESHOLD', '0.5'))
    
    while True:
        start_time = time.time()
        seen_alert_targets = set()
        cycle_results = []  # Collect all alert results for this cycle
        pending_notifications = []  # Store notifications to send after circuit breaker check
        
        # First pass: collect all alert results
        for alert in alerts:
            target = alert.get('target')
            try:
                records = get_records(
                    graphite_url,
                    requests.get,
                    GraphiteDataRecord,
                    target,
                    from_=alert.get('from'),
                    until_=alert.get('until'),
                    http_connect_timeout_s_ = http_connect_timeout_s,
                    http_read_timeout_s_    = http_read_timeout_s,
                )
            except (ValueError, requests.exceptions.RequestException) as e:
                if not alert.alert_data['allow_no_data']:
                    print("Error, {0}".format(alert.alert_data))
                    # Store for notification after circuit breaker check
                    pending_notifications.append(('missing', alert, None))
                    cycle_results.append(Level.NO_DATA)
                print("Exception in %s: %s" % (alert.get('name'),e))
                records = []

            for record in records:
                name = alert.get('name')
                if not record.target:
                    continue

                target = record.target

                if (name, target) not in seen_alert_targets:
                    # Check the record to get the level
                    alert_level, value = alert.check_record(record)
                    cycle_results.append(alert_level)
                    # Store for notification after circuit breaker check
                    pending_notifications.append(('record', alert, record))
                    seen_alert_targets.add((name, target))
        
        # Calculate circuit breaker status at the end of the cycle
        circuit_breaker_active = False
        if cycle_results:
            no_data_count = sum(1 for level in cycle_results if level == Level.NO_DATA)
            total_count = len(cycle_results)
            no_data_fraction = float(no_data_count) / total_count if total_count > 0 else 0.0
            
            circuit_breaker_active = no_data_fraction >= circuit_breaker_threshold
            
            if circuit_breaker_active:
                print('WARNING: {0:.1f}% ({1}/{2}) alerts are NO_DATA. '
                      'Most likely problem from HostedGraphite'.format(
                    no_data_fraction * 100, no_data_count, total_count))
        
        # Second pass: send notifications with circuit breaker flag
        for notification_type, alert, record in pending_notifications:
            if notification_type == 'missing':
                update_notifiers_missing(notifier_proxy, alert, config, circuit_breaker_active=circuit_breaker_active)
            elif notification_type == 'record':
                update_notifiers(notifier_proxy, alert, record, graphite_url, circuit_breaker_active=circuit_breaker_active)
        
        time_diff = time.time() - start_time
        sleep_for = int(heartbeat_seconds) - time_diff
        if sleep_for > 0:
            print('{0}: ran for {1} seconds, sleeping for {2} seconds'.format(
                datetime.datetime.now(timezone.utc),
                time_diff,
                sleep_for
            ))
            time.sleep(sleep_for)
        else:
            print('{0}: ran for {1} seconds, not sleeping'.format(
                datetime.datetime.now(timezone.utc),
                time_diff
            ))

def main():
    command_map = {
        'verify': verify,
        'run': run,
    }
    args = parse_args()
    return command_map[args.command](args)


if __name__ == '__main__':
    main()
