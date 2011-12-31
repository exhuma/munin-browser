import re
import logging

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
CONF = MuninConfig(__global = MuninConfig())

P_COMMENT = re.compile(r'#.*$')
P_HOST = re.compile(r'^\[(.*)\]$')
P_SEPARATOR = re.compile(r'\s+')

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
            CONF[group].setdefault(host, {})
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

    return CONF
