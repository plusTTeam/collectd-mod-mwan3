TYPES = {
    'LATENCY': {
        'parser': float,
        'type': 'conn_latency'
    },
    'STATUS': {
        'parser': None,
        'type': 'conn_status'
    }
}


class Measure:
    def __init__(self, name, value):
        self.name = name
        _type = TYPES[name]
        parser = _type['parser']
        self.type = _type['type']
        self.value = Value(raw=value, parser=parser)

    def __str__(self):
        return ''.join([self.name, '=', str(self.value)])


class Value:
    def __init__(self, raw, parser):
        self.raw = raw
        self.parser = parser

    def __str__(self):
        return str(self.value)

    @property
    def value(self):
        if self.parser:
            return self.parser(self.raw)
        else:
            return self.raw.decode("utf-8")
