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
                 'dbdir': 'test_dbdir'}
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

    def test_datafile_version(self):
        "Test the datafile version (currently tested against 1.4.4)"
        self.assertEquals(self._conf['__datafile_version'], '1.4.4')

    def test_datafile_contents(self):
        self.assertIn('open_inodes', self._conf['localdomain']['localhost.localdomain']['__graphs'])
        inode_graph = self._conf['localdomain']['localhost.localdomain']['__graphs']['open_inodes']

        self.assertIn('graph_title', inode_graph)
        self.assertIn('graph_args', inode_graph)
        self.assertIn('graph_vlabel', inode_graph)
        self.assertIn('graph_category', inode_graph)
        self.assertIn('graph_info', inode_graph)
        self.assertIn('graph_order', inode_graph)

        self.assertEquals(inode_graph['graph_title'], 'Inode table usage')
        self.assertEquals(inode_graph['graph_args'], '--base 1000 -l 0')
        self.assertEquals(inode_graph['graph_vlabel'], 'number of open inodes')
        self.assertEquals(inode_graph['graph_category'], 'system')
        self.assertEquals(inode_graph['graph_info'], 'This graph monitors the Linux open inode table.')
        self.assertEquals(inode_graph['graph_order'], 'used max')

        inode_used = inode_graph['meters']['used']
        self.assertIn('info', inode_used)
        self.assertIn('min', inode_used)
        self.assertIn('max', inode_used)
        self.assertIn('label', inode_used)
        self.assertIn('type', inode_used)

        self.assertEquals(inode_used['info'], 'The number of currently open inodes.')
        self.assertEquals(inode_used['min'], 'U')
        self.assertEquals(inode_used['max'], 'U')
        self.assertEquals(inode_used['label'], 'open inodes')
        self.assertEquals(inode_used['type'], 'GAUGE')

        #used.min U
        #used.max U
        #used.label open inodes
        #used.type GAUGE
        #max.info The size of the system inode table. This is dynamically
        #max.min U
        #max.max U
        #max.label inode table size
        #max.type GAUGE




