import re
import logging

"""
This module is used to read a munin config file.

The configuration is accessible as a standard dict via either the ``CONF``
member or the value returned by the ``read`` method::

    from muninbrowser import configparser
    conf = configparser.read(open('/etc/munin/munin.conf'))

    print 'global settings: %r' % conf['__global']
    for group in conf:
        if not group.startswith('__'):
            print 'Group: %s' % group
            print 'group globals: %r' % conf[group]['__global']
            for host in conf['group']:
                if not host.startswith('__'):
                print 'Host: %s' % host

As you can see, the global munin settings are exposed under the ``__global``
key. Each key not beginnig with ``__`` is a group specification. Each group
contains the hosts. Again, also the groups can have global settings under the
``__global`` key.

Note that the ``__global`` key is *always* present!
"""

LOG = logging.getLogger(__name__)
CONF = {'__global': {}}

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
            CONF.setdefault(group, {'__global': {}})
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
