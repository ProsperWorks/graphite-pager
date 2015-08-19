
from requests.auth import HTTPBasicAuth
from requests.auth import HTTPDigestAuth

def get_records(base_url, http_get, data_record, target, **kwargs):
    url = _graphite_url_for_target(base_url, target, **kwargs)
    print 'FULL URL: %s' % url
    graphite_user = config.get('GRAPHITE_USER')
    graphite_pass = config.get('GRAPHITE_PASS')
    resp = http_get(url,
                    verify=True,
                    auth=HTTPDigestAuth(graphite_user, graphite_pass)
                    #auth=HTTPBasicAuth(graphite_user, graphite_pass)
    )
    print 'RESP: %s' % resp
    resp.raise_for_status()
    records = []
    for line in resp.content.split('\n'):
        if line:
            record = data_record(line)
            records.append(record)
    return records

def _graphite_url_for_target(base, target, from_='-1min'):
    return '{0}/render/?target={1}&rawData=true&from={2}'.format(
        base,
        target,
        from_
    )
