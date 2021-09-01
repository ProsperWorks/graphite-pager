from graphitepager.level import Level


class BaseNotifier(object):

    def __init__(self, storage, config):
        self._client = None
        self._storage = storage
        self._domain = self.__class__.__name__.replace('Notifier', '')

    def notify(self, alert, alert_key, level, description):
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
            self._storage.remove_lock_for_domain_and_key(
                self._domain,
                alert_key
            )
        elif level == Level.NO_DATA:
            counter = self._storage.increment_no_data_count_for_alert(alert_key)
            if counter > self._config('NO_DATA_NOTIFICATION_THRESHOLD', 3):
                self._notify(
                    alert,
                    level,
                    description,
                    nominal=False
                )
        elif level in should_notify and not notified:
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

    def _notify(self,
                alert,
                level,
                description,
                nominal=None):
        pass
