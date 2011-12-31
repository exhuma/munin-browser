import unittest2 as unittest
from muninbrowser.model import Munin

class TestModel(unittest.TestCase):

    def setUp(self):
        from os.path import join, dirname
        conf_name = join(dirname(__file__), 'test_config.conf')
        self._model = Munin(conf_name)

    def test_groups(self):
        "test retrieval of host groups"
        expected = set(['hostgroup', 'localdomain', 'testgroup'])
        self.assertEquals(set(self._model.groups), expected)

    def test_hosts(self):
        "test retrieval of hosts"
        self.assertEquals(self._model.hosts('testgroup'), [])
        self.assertEquals(self._model.hosts('localdomain'), ['localhost.localdomain'])
        self.assertEquals(self._model.hosts('hostgroup'), ['hostname'])

    def test_graphs(self):
        pass

