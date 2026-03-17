import time

from graphitepager.level import Level


class BaseNotifier(object):

    def __init__(self, storage, config):
        self._client = None
        self._storage = storage
        self._config = config
        self._domain = self.__class__.__name__.replace('Notifier', '')

    def notify(self, alert, alert_key, level, description, circuit_breaker_active=False):
        notified = self._storage.is_locked_for_domain_and_key(
            self._domain,
            alert_key
        )
        should_notify = (Level.WARNING, Level.CRITICAL)
        if level == Level.NOMINAL and notified:
            self._notify(
                alert,
                level,
                description,
                nominal=True
            )
            self._storage.reset_no_data_count_for_alert(alert_key)
            self._storage.clear_first_no_data_timestamp(alert_key)
            self._storage.remove_lock_for_domain_and_key(
                self._domain,
                alert_key
            )
        elif level == Level.NO_DATA:
            # Global circuit breaker: suppress all NO_DATA if circuit breaker is active
            if circuit_breaker_active:
                return
            
            # Check no_data_timeout if configured
            current_time = time.time()
            first_no_data_time = self._storage.get_first_no_data_timestamp(alert_key)
            
            # If this is the first time we see NO_DATA, record the timestamp
            if first_no_data_time is None:
                self._storage.set_first_no_data_timestamp(alert_key, current_time)
                first_no_data_time = current_time
            
            # If no_data_timeout is set, only notify after the timeout has elapsed
            if alert.no_data_timeout_seconds is not None:
                elapsed = current_time - first_no_data_time
                if elapsed < alert.no_data_timeout_seconds:
                    # Timeout hasn't elapsed yet, don't notify
                    return
            
            counter = self._storage.increment_no_data_count_for_alert(alert_key)
            if counter > self._config.get('NO_DATA_NOTIFICATION_THRESHOLD', 3):
                self._notify(
                    alert,
                    level,
                    description,
                    nominal=False
                )
        elif level in should_notify and not notified:
            # Clear NO_DATA timestamp when we get real data (WARNING/CRITICAL)
            self._storage.clear_first_no_data_timestamp(alert_key)
            self._notify(
                alert,
                level,
                description,
                nominal=False
            )
            self._storage.set_lock_for_domain_and_key(
                self._domain,
                alert_key
            )
        elif level == Level.NOMINAL:
            # Clear NO_DATA timestamp when we get nominal data
            self._storage.clear_first_no_data_timestamp(alert_key)

    def _notify(self,
                alert,
                level,
                description,
                nominal=None):
        pass
