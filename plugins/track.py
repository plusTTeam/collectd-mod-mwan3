import collectd
from os import walk

from models.interface import Interface

plugin_name = 'mwan3_track'
PATH = '/var/run/mwan3track/'
# track_all = False
interfaces = []


def config_func(config):
    global interfaces
    path_set = False

    for node in config.children:
        key = node.key.lower()
        val = node.values[0]

        if key == 'path':
            global PATH
            PATH = val
            path_set = True
        # elif key == 'all':
        #     global track_all
        #     track_all = True
        else:
            interfaces.append(Interface(iface=key, name=val))

    collectd.info('plugin_load: plugin "mwan3track" successfully loaded.')

    # if track_all:
    #     collectd.info('mwan3track: tacking all interfaces')
    for i in interfaces:
        collectd.info('mwan3track: collecting interface %s' % i)

    if path_set:
        collectd.info('mwan3track: Using overridden path %s' % PATH)
    else:
        collectd.info('mwan3track: Using default path %s' % PATH)


def read_func():
    for (dirpath, dirnames, filenames) in walk(PATH):
        if dirpath != PATH:
            try:
                interface = next(x for x in interfaces if x.if_dir(path=dirpath))
                for measure in interface.get_measures(filenames):
                    val = collectd.Values(type=measure.type,
                                          type_instance=interface.iface,
                                          plugin=plugin_name)
                    val.dispatch(values=measure.values)
            except StopIteration as e:
                continue
        else:
            [i.path(dirpath) for i in interfaces if i.name in dirnames]


collectd.register_config(config_func)
collectd.register_read(read_func)
