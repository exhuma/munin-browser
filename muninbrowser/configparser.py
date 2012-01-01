import re
import logging
from os.path import join

"""
This module is used to read a munin config file.

The configuration is accessible as a subclass of a standard dict.
The specialised class offers a couple of convenience methods over the standard
dict:

* It has a ``globals`` property representing the global settings for that group

* It has a ``members`` property representing the direct child without the
  globals. Members of ``conf`` are the host groups, wile members of a host
  group are the hosts

The config object can be constructed with the ``read`` method::

    from muninbrowser import configparser
    conf = configparser.read(open('/etc/munin/munin.conf'))

    print 'global settings: %r' % conf.globals
    for group in conf.members:
        print 'Group: %s' % group
        print 'group globals: %r' % conf[group].globals
        for host in conf[group].members:
            print 'Host: %s' % host
"""

class MuninConfig(dict):
    """
    A subclass of dict providing some helper functions
    """

    @property
    def members(self):
        """Return a list of non-special keys"""
        return [_ for _ in self.keys() if not _.startswith('__')]

    @property
    def globals(self):
        """Return the global settings"""
        return self['__global']

LOG = logging.getLogger(__name__)

# Defaults
CONF = MuninConfig(__global = MuninConfig(
    dbdir='/var/lib/munin'))

P_COMMENT = re.compile(r'#.*$')
P_HOST = re.compile(r'^\[(.*)\]$')
P_SEPARATOR = re.compile(r'\s+')

def read_datafile(conf, file):
    """
    Read the munin data-file and merge the contents with the config object
    """

    last_graph = {}
    line = file.readline().strip()
    _, version = line.split()
    conf['__datafile_version'] = version
    current_state = 'initial'

    for line in file:
        line = line.strip()
        group, host_graph = line.split(';', 1)
        host, graph_meta = host_graph.split(':', 1)
        graph_path, value = graph_meta.split(' ', 1)
        graph_name, tail_var = graph_path.rsplit('.', 1)

        #
        # As long as the values start with "graph_" we have general graph
        # metadata
        #
        if tail_var.startswith('graph_'):

            if current_state != 'graph_info':
                current_state = 'graph_info'
                if '__name' in last_graph:
                    conf[group][host]['__graphs'][last_graph['__name']] = last_graph
                last_graph = {
                        '__name': graph_name,
                        'meters': {}}
                last_graph[tail_var] = value
                continue

            last_graph[tail_var] = value

            if tail_var == 'graph_order':
                # initialise the meter collections
                for meter in value.split():
                    last_graph['meters'].setdefault(meter, {})

        else:
            #
            # if the values don't start with "graph_" we assume we have meters
            #
            graph_name, meter_name, meter_var = graph_path.rsplit('.', 2)
            last_graph['meters'].setdefault(meter_name, {})
            last_graph['meters'][meter_name][meter_var] = value
            current_state = 'graph_meters'

        conf[group][host]['__graphs'][last_graph['__name']] = last_graph

def read(file):
    """
    Read the config from a file-like object, and return a ``dict`` as
    explained above.

    Example::

        muninbrowser.read(open('/path/to/munin.conf'))
    """
    current_section = ('__global',)
    for line in file:
        line = line.strip()
        if not line or line.startswith('#'):
            continue

        # remove comments
        line = P_COMMENT.sub('', line).strip()

        # if we encounter a host-line, close the current section and
        # reopen a new one.
        m = P_HOST.match(line)
        if m:
            line = m.groups()[0]
            # if no group specified (i.e. no semicolon in the line), then
            # we remove the first part of the FQDN and take the remainder
            # as group name
            if ';' not in line:
                host = line
                group = line.split('.', 1)[1]
            else:
                group, host = line.split(';')
            CONF.setdefault(group, MuninConfig(__global = {}))
            if not host:
                host = '__global'
            host_dict = CONF[group].setdefault(host, {})
            host_dict.setdefault('__graphs', {})
            current_section = (group, host)
            continue

        # Everything else should be a value and can be appended to the
        # conf-dict
        try:
            key, value = P_SEPARATOR.split(line)
        except ValueError, ex:
            LOG.error('Unable to parse line %r' % line)
            raise

        if len(current_section) == 1:
            CONF['__global'][key.strip()] = value.strip()
        else:
            group, host = current_section
            CONF[group][host][key.strip()] = value.strip()

    datafile = join(CONF.globals['dbdir'], 'datafile')
    with open(datafile) as fp:
        read_datafile(CONF, fp)
    return CONF
