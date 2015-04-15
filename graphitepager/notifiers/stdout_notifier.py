from graphitepager.notifiers.base import BaseNotifier


class StdoutNotifier(BaseNotifier):

    def __init__(self, storage, config):
        super(StdoutNotifier, self).__init__(storage, config)
        self._rooms = set()

        self.enabled = config.has_keys(['STDOUT_ENABLED'])

    def _notify(self,
                alert,
                level,
                description,
                html_description,
                nominal=None):

        print '[{0}] {1}'.format(
            level,
            description.stdout().replace("\n", ' ')
        )
