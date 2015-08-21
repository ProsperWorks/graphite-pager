import pagerduty

from graphitepager.level import Level
from graphitepager.notifiers.base import BaseNotifier


class PagerdutyNotifier(BaseNotifier):

    def __init__(self, storage, config):
        super(PagerdutyNotifier, self).__init__(storage, config)

        required = ['PAGERDUTY_KEY']
        self.enabled = config.has_keys(required)
        print 'PagerdutyNotifier.enabled: %s' % self.enabled
        if self.enabled:
            print 'PAGERDUTY_KEY: %s' % config.get('PAGERDUTY_KEY')
            self._client = pagerduty.PagerDuty(config.get('PAGERDUTY_KEY'))
            self._pagerduty_config = config.get('pagerduty', {})
            self._pagerduty_keys = {
                Level.NOMINAL: self._pagerduty_config.get(
                    'nominal', self._client.service_key
                ),
                Level.WARNING: self._pagerduty_config.get(
                    'warning', self._client.service_key
                ),
                Level.CRITICAL: self._pagerduty_config.get(
                    'critical', self._client.service_key
                ),
                Level.NO_DATA: self._pagerduty_config.get(
                    'no_data', self._client.service_key
                ),
            }

    def notify(self, alert, alert_key, level, description):
        service_key = self._client.service_key
        self._client.service_key = self._get_service_key(alert, level)

        incident_key = self._storage.get_incident_key_for_alert_key(alert_key)
        if level != Level.NOMINAL:
            description = str(description)
            print 'TRIGGERING'
            print 'service_key:    %s' % service_key
            print 's._c.s_k:       %s' % self._client.service_key
            print 'alert_key:      %s' % alert_key
            print 'incident_key A: %s' % incident_key
            print 'description:    %s' % description
            incident_key = self._client.trigger(
                incident_key=incident_key,
                description=description
            )
            print 'incident_key B: %s' % incident_key
            self._storage.set_incident_key_for_alert_key(
                alert_key,
                incident_key
            )
        elif incident_key is not None:
            self._client.resolve(incident_key=incident_key)
            self._storage.remove_incident_for_alert_key(alert_key)

        self._client.service_key = service_key

        print 'PAGERDUTY NOTIFY'


    def _get_service_key(self, alert, level):
        service_key = self._pagerduty_keys.get(level, self._client.service_key)
        return alert.get('pagerduty_key', service_key)
