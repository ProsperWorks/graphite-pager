"""Data record for a single metric of Graphite data"""


class NoDataError(ValueError):
    pass


class GraphiteDataRecord(object):

    def __init__(self, metric_string):
        meta, data = metric_string.split('|')
        print 'GraphiteDataRecord(self,%s)' % metric_string
        print 'meta,data: %s,%s' % (meta,data)
        self.target, start_time, end_time, step = meta.rsplit(',', 3)
        print 't,st,et,s: %s,%s,%s,%s' % (self.target, start_time, end_time, step)
        self.start_time = int(start_time)
        self.end_time = int(end_time)
        self.step = int(step)
        self.values = [_float_or_none(value) for value in data.rsplit(',')]
        print 'values: %s' % self.values

    def get_average(self):
        values = [value for value in self.values if value is not None]
        if len(values) == 0:
            raise NoDataError()
        return sum(values) / len(values)

    def get_last_value(self):
        for value in reversed(self.values):
            if value is not None:
                return value
        raise NoDataError()


def _float_or_none(value):
    try:
        return float(value)
    except ValueError:
        return None
