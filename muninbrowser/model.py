class UnboundObjectError(ValueError):
    pass

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

class MuninObject(object):

    def __init__(self):
        self._conf = None

    def bind(self, config):
        self._conf = config

class Group(MuninObject):
    """
    A class representing a group of hosts
    """

    def __init__(self, name, conf=None):
        super(Group, self).__init__()
        self.name = name
        if conf:
            self.bind(conf)

    def __repr__(self):
        return "<%s %s>" % (
                self.__class__.__name__,
                self.name
                )

    def __eq__(self, other):
        return isinstance(other, Group) and (
                other.name == self.name)

    def __hash__(self):
        return self.name.__hash__()

    @classmethod
    def all(self, conf):
        "retrieve all groups"

        out = []
        for group in conf.members:
            tmp = Group(group, conf=conf)
            out.append(tmp)

        return out

    @classmethod
    def get(self, conf, name):
        "get one group by name"
        if name not in conf.members:
            return None
        return Group(name, conf=conf)

    @property
    def hosts(self):
        out = []
        for host in self._conf[self.name].members:
            tmp = Host(self.name, host, self._conf)
            out.append(tmp)
        return out

class Host(MuninObject):
    """
    A class representing a monitored host
    """

    def __init__(self, group, name, conf=None):
        super(Host, self).__init__()
        self.group = group
        self.name = name
        if conf:
            self.graphs = conf[group][name]['__graphs']
            self.bind(conf)

    def __repr__(self):
        return "<%s %s[%s]>" % (
                self.__class__.__name__,
                self.group,
                self.name
                )

    def __eq__(self, other):
        return isinstance(other, Host) and (
                other.name == self.name and
                other.group == self.group)

    def __hash__(self):
        return self.group.__hash__() ^ self.name.__hash__()

    @classmethod
    def all(self, conf, groupname=None):
        "retrieve all hosts"

        out = []
        if groupname:
            for host in conf[groupname].members:
                tmp = Host(groupname, host, conf=conf)
                out.append(tmp)
        else:
            for group in conf.members:
                for host in conf[group].members:
                    tmp = Host(group, host, conf=conf)
                    out.append(tmp)
        return out

class Graph(MuninObject):
    """
    A class representing a graph
    """

    def __init__(self, host, name, conf=None):
        super(Graph, self).__init__()
        self.host = host
        self.name = name
        if conf:
            self.bind(conf)

    def __repr__(self):
        return "<%s %s:%s>" % (
                self.__class__.__name__,
                self.host,
                self.name)

    def __eq__(self, other):
        return isinstance(other, Graph) and (
                other.host == self.host and
                other.name == self.name)

    def __hash__(self):
        return (self.host.__hash__() ^
                self.name.__hash__())

    @property
    def attributes(self):
        if not self._conf:
            raise UnboundObjectError('The instance %r is not bound to a config instance!' % self)
        return self._conf[self.host.group][self.host.name]['__graphs'][self.name].keys()

    @classmethod
    def all_names(self, conf):
        """
        Returns a list of all known graph names
        """
        all_graphs = set()
        for host in Host.all(conf):
            all_graphs.update([name for name in host.graphs.keys()])
        return all_graphs

    @classmethod
    def all_categories(self, conf):
        """
        Returns a list of all known graph categories
        """
        categories = set()
        for host in Host.all(conf):
            for key in host.graphs:
                categories.add(host.graphs[key]['graph_category'])
        return categories
