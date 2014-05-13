import os
import yaml

from alerts import Alert


def contents_of_file(filename):
    open_file = open(filename)
    contents = open_file.read()
    open_file.close()
    return contents


def get_config(path):
    return Config(path)


class Config(object):

    def __init__(self, path):
        alert_yml = contents_of_file(path)
        self._data = yaml.load(alert_yml)

    def data(self, key):
        return self._data[key]

    def get(self, key, default=None):
        return os.environ.get(key, self._data.get(key.lower(), default))

    def get_alerts(self, config):
        alerts = []
        doc_url = self.config.data('docs_url')
        for alert_string in self.config.data('alerts'):
            alerts.append(Alert(alert_string, doc_url))
        return alerts

    def has_keys(self, keys):
        for key in keys:
            if self.get(key) is None:
                return False
        return True
