import unittest2 as unittest
from muninbrowser.model import Group, Host

class TestGroup(unittest.TestCase):

    def setUp(self):
        from muninbrowser.configparser import read
        from os.path import join, dirname
        conf_name = join(dirname(__file__), 'test_config.conf')
        self._conf = read(open(conf_name))

    def test_groups(self):
        "Retrieving all groups"
        expected = set([
            Group('testgroup'),
            Group('hostgroup'),
            Group('localdomain'),
            ])
        self.assertEquals(set(Group.all(self._conf)), expected)

    def test_hosts(self):
        "Retrieving hosts from a group"
        group = Group('localdomain', self._conf)
        expected = [Host('localdomain', 'localhost.localdomain', conf=self._conf)]
        self.assertEquals(group.hosts, expected)

    def test_get_group(self):
        expected = Group('localdomain')
        self.assertEquals(Group.get(self._conf, 'localdomain'), expected)

class TestHosts(unittest.TestCase):

    def setUp(self):
        from muninbrowser.configparser import read
        from os.path import join, dirname
        conf_name = join(dirname(__file__), 'test_config.conf')
        self._conf = read(open(conf_name))

    def test_hosts(self):
        expected = set([
            Host('hostgroup', 'hostname'),
            Host('localdomain', 'localhost.localdomain')
            ])
        self.assertEquals(set(Host.all(self._conf)), expected)

        expected = set([
            Host('localdomain', 'localhost.localdomain')
            ])
        self.assertEquals(set(Host.all(self._conf, 'localdomain')), expected)
