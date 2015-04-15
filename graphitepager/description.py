from jinja2 import Template
from urllib import urlencode

from graphitepager.level import Level

ALERT_MISSING_TEMPLATE = r"""{{level}} alert for
{{alert.get('name')}} {{record.target}}. Go to {{graph_url}}.
{% if docs_url %}Documentation: {{docs_url}}{% endif %}.
"""

HTML_ALERT_MISSING_TEMPLATE = r"""{{level}} alert for
{{alert.get('name')}} {{record.target}}.
Go to <a href="{{graph_url}}">the graph</a>.
{% if docs_url %}<a href="{{docs_url}}">Documentation</a>{% endif %}.
"""

STDOUT_MISSING_TEMPLATE = r"""{{level}} alert for
{{alert.get('name')}} {{record.target}}. Go to {{graph_url}}.
"""

ALERT_TEMPLATE = r"""{{level}} alert for
{{alert.get('name')}} {{record.target}}. The current value is
{{current_value}} which passes the {{threshold_level|lower}}
value of {{threshold_value}}. Go to {{graph_url}}.
{% if docs_url %}Documentation: {{docs_url}}{% endif %}.
"""

HTML_ALERT_TEMPLATE = r"""{{level}} alert for
{{alert.get('name')}} {{record.target}}. The current value is
{{current_value}} which passes the {{threshold_level|lower}}
value of {{threshold_value}}.
Go to <a href="{{graph_url}}">the graph</a>.
{% if docs_url %}<a href="{{docs_url}}">Documentation</a>{% endif %}.
"""

STDOUT_TEMPLATE = r"""{{level}} alert for
{{alert.get('name')}} {{record.target}}. The current value is
{{current_value}} which passes the {{threshold_level|lower}}
value of {{threshold_value}}.
"""


class Description(object):

    def __init__(self, template, graphite_url, alert, record, level, value):
        self.template = template
        self.graphite_url = graphite_url
        self.alert = alert
        self.record = record
        self.level = level
        self.value = value

    def __str__(self):
        return self.description_for_alert(
            self.template,
            self.graphite_url,
            self.alert,
            self.record,
            self.level,
            self.value,
        )

    def stdout(self):
        template = STDOUT_TEMPLATE
        if self.level == Level.NO_DATA:
            template = STDOUT_MISSING_TEMPLATE

        return self.description_for_alert(
            template,
            self.graphite_url,
            self.alert,
            self.record,
            self.level,
            self.value,
        )

    def description_for_alert(self,
                              template,
                              graphite_url,
                              alert,
                              record,
                              level,
                              current_value):
        context = dict(locals())
        context['graphite_url'] = graphite_url
        if type(record) == str:
            context['docs_url'] = alert.documentation_url()
        else:
            context['docs_url'] = alert.documentation_url(record.target)

        url_params = (
            ('width', 586),
            ('height', 308),
            ('target', alert.get('target')),
            ('target', 'threshold({},"Warning")'.format(
                alert.get('warning'))),
            ('target', 'threshold({},"Critical")'.format(
                alert.get('critical'))),
            ('from', '-20mins'),
        )
        url_args = urlencode(url_params)
        url = '{}/render/?{}'.format(graphite_url, url_args)
        context['graph_url'] = url.replace('https', 'http')
        context['threshold_value'] = alert.value_for_level(level)
        if level == Level.NOMINAL:
            context['threshold_level'] = 'warning'
        else:
            context['threshold_level'] = level

        return Template(template).render(context)


def _get_descriptions(graphite_url,
                      alert,
                      record,
                      alert_level,
                      value,
                      alert_template,
                      html_alert_template):
    description = Description(
        alert_template,
        graphite_url,
        alert,
        record,
        alert_level,
        value
    )
    html_description = Description(
        html_alert_template,
        graphite_url,
        alert,
        record,
        alert_level,
        value
    )

    return description, html_description


def get_descriptions(graphite_url,
                     alert,
                     record,
                     alert_level,
                     value):
    return _get_descriptions(graphite_url,
                             alert,
                             record,
                             alert_level,
                             value,
                             ALERT_TEMPLATE,
                             HTML_ALERT_TEMPLATE)


def missing_target_descriptions(graphite_url,
                                alert,
                                record,
                                alert_level,
                                value):
    return _get_descriptions(graphite_url,
                             alert,
                             record,
                             alert_level,
                             value,
                             ALERT_MISSING_TEMPLATE,
                             HTML_ALERT_MISSING_TEMPLATE)
