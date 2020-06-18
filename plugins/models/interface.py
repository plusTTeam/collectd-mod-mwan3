from os.path import join

from . import Measure


class Interface:
    measures = []

    def __init__(self, iface, name):
        self.iface = iface
        self.name = name
        self._path = ''

    def path(self, path):
        self._path = join(path, self.name)

    def __str__(self):
        return ''.join([self.name, '=', self.iface])

    def if_dir(self, path):
        return self._path == path

    def get_measures(self, files):
        for f in files:
            with open(join(self._path, f), 'rb') as measure:
                try:
                    self.measures.append(Measure(name=f, value=measure.read().strip()))
                except KeyError as e:
                    print('Unrecognized measure %s' % f)
                    continue
        return self.measures
