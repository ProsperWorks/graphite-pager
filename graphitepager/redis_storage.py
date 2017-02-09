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

    def _redis_key_from_alert_key(self, alert_key):
        return '{0}-incident-key'.format(alert_key)
