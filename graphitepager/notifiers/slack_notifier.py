import json
import urllib
import urllib2

from graphitepager.level import Level
from graphitepager.notifiers.base import BaseNotifier


class SlackNotifier(BaseNotifier):

    def __init__(self, storage, config):
        super(SlackNotifier, self).__init__(storage, config)
        self._rooms = set()

        required = ['SLACK_URL']
        self.enabled = config.has_keys(required)
        if self.enabled:
            self._slack_url = config.get('SLACK_URL')

    def _notify(self,
                alert,
                level,
                description,
                nominal=None):
        colors = {
            Level.NOMINAL: '00FF00',  # green
            Level.WARNING: 'ffff00',  # yellow
            Level.CRITICAL: '#FF0000',  # red
        }
        color = colors.get(level, '#FF0000')  # red

        description = str(description.slack())
        self._message_room(
            message=description,
            color=color,
            level=level,
        )

    # #800080 == purple
    def _message_room(self,
                      message,
                      color='#800080',
                      level=None,
                      icon_emoji=None):
        args = {
            'text': 'graphite-pager alert',
            'attachments': [{
                'color': color,
                'fields': [{
                    'title': level,
                    'value': message.replace("\n", ' '),
                    'short': False,
                }]
            }]
        }

        if icon_emoji is not None:
            args['icon_emoji'] = icon_emoji

        values = {'payload': json.dumps(args)}
        encoded_args = urllib.urlencode(values)

        try:
            url = self._slack_url
            response = urllib2.urlopen(url, encoded_args).read()
        except urllib2.HTTPError as e:
            print '--> Unable to send message to slack: "{0}"'.format(
                e
            )
            return False

        if response == 'ok':
            return True

        print '--> Unable to send message to slack: "{0}"'.format(
            message
        )
        return False
