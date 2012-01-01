import unittest2 as unittest

class TestConfigParser(unittest.TestCase):

    def setUp(self):
        from muninbrowser.configparser import read
        from os.path import join, dirname
        conf_name = join(dirname(__file__), 'test_config.conf')
        self._conf = read(open(conf_name))

    def test_read_type(self):
        self.assertIsInstance(self._conf, dict)

    def test_globals(self):
         expected = {
                 'graph_width': '500',
                 'includedir': '/etc/munin/munin-conf.d',
                 'graph_height': '300',
                 'dbdir': '/var/lib/munin'}
         self.assertEquals(self._conf.globals, expected)

    def test_groups(self):
        "Test if we get the expected host-groups"
        expected = set(['testgroup', 'hostgroup', 'localdomain'])
        result = set(self._conf.members)
        self.assertEquals(result, expected)

    def test_hosts(self):
        "Test if we get the expected hosts in each group"
        self.assertEquals(
                self._conf['testgroup'].members,
                [])
        self.assertEquals(
                self._conf['hostgroup'].members,
                ['hostname'])
        self.assertEquals(
                self._conf['localdomain'].members,
                ['localhost.localdomain'])

