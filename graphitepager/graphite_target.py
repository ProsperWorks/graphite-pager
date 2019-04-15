
def get_records(base_url,
                http_get,
                data_record,
                target,
                from_                   = '-1min',
                until_                  = None,
                http_connect_timeout_s_ = 0.1,
                http_read_timeout_s_    = 1.0):
    url = _graphite_url_for_target(base_url, target, from_=from_, until_=until_)
    resp = http_get(
        url,
        verify  = True,
        timeout = (http_connect_timeout_s_,http_read_timeout_s_),
    )
    resp.raise_for_status()
    records = []
    for line in resp.content.split('\n'):
        if line:
            record = data_record(line)
            records.append(record)
    return records


def _graphite_url_for_target(base, target, from_='-1min', until_=None):
    url = '{0}/render/?target={1}&format=raw&from={2}'.format(
        base,
        target,
        from_
    )
    if until_:
        url += '&until={0}'.format(until_)
    return url
