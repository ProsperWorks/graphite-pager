import json


class RedisStorage(object):

    def __init__(self, redis_lib, url, config):
        self._client = redis_lib.from_url(url)
        self._config = config

    def get_incident_key_for_alert_key(self, alert):
        key = self._redis_key_from_alert_key(alert)
        resp = self._client.get(key)
        if resp is not None:
            return json.loads(resp)['incident']

    def set_incident_key_for_alert_key(self, alert, ik):
        data = {'incident': ik}
        key = self._redis_key_from_alert_key(alert)
        exp = int(self._config.get('INCIDENT_EXPIRATION_SECONDS',3600))
        self._client.set(key, json.dumps(data))
        self._client.expire(key, exp)

    def remove_incident_for_alert_key(self, alert):
        key = self._redis_key_from_alert_key(alert)
        self._client.delete(key)

    def set_lock_for_domain_and_key(self, domain, key):
        key = 'LOCK-{0}-{1}'.format(domain, key)
        exp = int(self._config.get('NOTIFICATION_EXPIRATION_SECONDS',300))
        self._client.set(key, True)
        self._client.expire(key, exp)

    def remove_lock_for_domain_and_key(self, domain, key):
        key = 'LOCK-{0}-{1}'.format(domain, key)
        self._client.delete(key)

    def is_locked_for_domain_and_key(self, domain, key):
        key = 'LOCK-{0}-{1}'.format(domain, key)
        value = self._client.get(key)
        if value is None:
            return False
        return True

    def _recovery_pending_key(self, domain, key):
        return 'RECOVERY-PENDING-{0}-{1}'.format(domain, key)

    def set_recovery_pending_for_domain_and_key(self, domain, key):
        """Mark that we owe a Nominal/OK notification when the metric recovers.

        Separate from the notification lock: the lock expires after
        NOTIFICATION_EXPIRATION_SECONDS (re-alert path), but recovery_pending
        stays until we send OK or TTL expires. Call again on each cycle while
        still WARNING/CRITICAL to refresh TTL (including lock-suppressed cycles).
        """
        rkey = self._recovery_pending_key(domain, key)
        exp = int(self._config.get('RECOVERY_PENDING_EXPIRATION_SECONDS', 604800))
        self._client.set(rkey, True, ex=exp)

    def is_recovery_pending_for_domain_and_key(self, domain, key):
        rkey = self._recovery_pending_key(domain, key)
        return self._client.get(rkey) is not None

    def clear_recovery_pending_for_domain_and_key(self, domain, key):
        rkey = self._recovery_pending_key(domain, key)
        self._client.delete(rkey)

    def _redis_key_from_alert_key(self, alert_key):
        return '{0}-incident-key'.format(alert_key)

    def increment_no_data_count_for_alert(self, alert):
        key = '{0}-no-data-counter'.format(alert)
        exp = int(self._config.get('NO_DATA_COUNTER_EXPIRATION_SECONDS',600))
        counter = int(self._client.get(key) or 0) + 1
        if self._config.get('NO_DATA_COUNTER_VERBOSE',None):
            print("incrementing 'NO DATA' counter for {0} to {1} with TTL {2}".format(key, counter, exp))
        self._client.set(key, counter, ex=exp)
        return counter

    def reset_no_data_count_for_alert(self, alert):
        key = '{0}-no-data-counter'.format(alert)
        exp = int(self._config.get('NO_DATA_COUNTER_EXPIRATION_SECONDS',600))
        if self._config.get('NO_DATA_COUNTER_VERBOSE',None):
            print("resetting 'NO DATA' count for {0} to 0 with TTL {1}".format(key, exp))
        self._client.set(key, 0, ex=exp)
        return 0

    def get_first_no_data_timestamp(self, alert_key):
        """Get the timestamp when NO_DATA was first detected for an alert."""
        key = '{0}-no-data-first-timestamp'.format(alert_key)
        value = self._client.get(key)
        if value is not None:
            try:
                return float(value)
            except (ValueError, TypeError):
                return None
        return None

    def set_first_no_data_timestamp(self, alert_key, timestamp):
        """Set the timestamp when NO_DATA was first detected for an alert."""
        key = '{0}-no-data-first-timestamp'.format(alert_key)
        # Use a long expiration (24 hours) to handle extended outages
        exp = int(self._config.get('NO_DATA_TIMESTAMP_EXPIRATION_SECONDS', 86400))
        self._client.set(key, str(timestamp), ex=exp)

    def clear_first_no_data_timestamp(self, alert_key):
        """Clear the first NO_DATA timestamp when data returns."""
        key = '{0}-no-data-first-timestamp'.format(alert_key)
        self._client.delete(key)
