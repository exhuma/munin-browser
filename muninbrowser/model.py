class Munin(object):

    def __init__(self, configfile):
        from muninbrowser.configparser import read
        self.__config = read(open(configfile))

    @property
    def groups(self):
        return sorted([_ for _ in self.__config.keys() if not
            _.startswith('__')])

    @property
    def tree(self):
        tree = {}
        for group in self.groups:
            hosts = self.hosts(group)
            if not hosts:
                continue
            tree[group] = hosts
        return tree

    def hosts(self, groupname):
        if groupname not in self.__config:
            return None
        return sorted([_ for _ in self.__config[groupname].keys() if not
            _.startswith('__')])

