import hipchat

from graphitepager.level import Level
from graphitepager.notifiers.base import BaseNotifier


class HipChatNotifier(BaseNotifier):

    def __init__(self, storage, config):
        super(HipChatNotifier, self).__init__(storage, config)
        self._rooms = set()

        required = ['HIPCHAT_KEY', 'HIPCHAT_ROOM']
        self.enabled = config.has_keys(required)
        if self.enabled:
            self._client = hipchat.HipChat(config.get('HIPCHAT_KEY'))
            self.add_room(config.get('HIPCHAT_ROOM'))

    def _notify(self,
                alert,
                level,
                description,
                nominal=None):
        colors = {
            Level.NOMINAL: 'green',
            Level.WARNING: 'yellow',
            #
            # Per
            # https://www.hipchat.com/docs/api/method/rooms/message,
            # color choices are "yellow", "red", "green", "purple",
            # "gray", or "random". (default: yellow)
            #
            # I'd prefer orange, but I'm taking purple for NO_DATA
            # because yellow, red, and green are taken and gray is
            # gray.
            #
            Level.NO_DATA: 'purple',
            Level.CRITICAL: 'red',
        }
        color = colors.get(level, 'red')

        description = description.html()
        self._notify_room_with_args(
            'Graphite-Pager',
            description,
            message_format='html',
            color=color,
        )

    def _notify_room_with_args(self, *args, **kwargs):
        for room in self._rooms:
            self._client.message_room(room, *args, **kwargs)

    def add_room(self, room):
        self._rooms.add(room)
