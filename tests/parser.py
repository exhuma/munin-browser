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

    def test_first_graph_loaded(self):
        "Test if the first graph in the file is properly loaded"

        self.assertIn('postgres_connections_ALL',
                self._conf['localdomain']['localhost.localdomain']['__graphs'])
        pg_graph = self._conf['localdomain']['localhost.localdomain']['__graphs']['postgres_connections_ALL']

        self.assertEquals(pg_graph['graph_title'], 'PostgreSQL connections')
        self.assertEquals(pg_graph['graph_vlabel'], 'Connections')
        self.assertEquals(pg_graph['graph_category'], 'PostgreSQL')
        self.assertEquals(pg_graph['graph_info'], 'Number of connections')
        self.assertEquals(pg_graph['graph_args'], '--base 1000')
        self.assertEquals(pg_graph['graph_order'], 'active waiting idle idletransaction unknown')

        self.assertEquals(pg_graph['meters']['waiting']['draw'], 'STACK')
        self.assertEquals(pg_graph['meters']['waiting']['min'], 'U')
        self.assertEquals(pg_graph['meters']['waiting']['max'], 'U')
        self.assertEquals(pg_graph['meters']['waiting']['label'], 'Waiting for lock')
        self.assertEquals(pg_graph['meters']['waiting']['type'], 'GAUGE')
        self.assertEquals(pg_graph['meters']['unknown']['draw'], 'STACK')
        self.assertEquals(pg_graph['meters']['unknown']['min'], 'U')
        self.assertEquals(pg_graph['meters']['unknown']['max'], 'U')
        self.assertEquals(pg_graph['meters']['unknown']['label'], 'Unknown')
        self.assertEquals(pg_graph['meters']['unknown']['type'], 'GAUGE')
        self.assertEquals(pg_graph['meters']['active']['draw'], 'AREA')
        self.assertEquals(pg_graph['meters']['active']['min'], 'U')
        self.assertEquals(pg_graph['meters']['active']['max'], 'U')
        self.assertEquals(pg_graph['meters']['active']['label'], 'Active')
        self.assertEquals(pg_graph['meters']['active']['type'], 'GAUGE')
        self.assertEquals(pg_graph['meters']['idletransaction']['draw'], 'STACK')
        self.assertEquals(pg_graph['meters']['idletransaction']['min'], 'U')
        self.assertEquals(pg_graph['meters']['idletransaction']['max'], 'U')
        self.assertEquals(pg_graph['meters']['idletransaction']['label'], 'Idle in transaction')
        self.assertEquals(pg_graph['meters']['idletransaction']['type'], 'GAUGE')
        self.assertEquals(pg_graph['meters']['idle']['draw'], 'STACK')
        self.assertEquals(pg_graph['meters']['idle']['min'], 'U')
        self.assertEquals(pg_graph['meters']['idle']['max'], 'U')
        self.assertEquals(pg_graph['meters']['idle']['label'], 'Idle')
        self.assertEquals(pg_graph['meters']['idle']['type'], 'GAUGE')

    def test_last_graph_loaded(self):
        "Test if the last graph in the file is properly loaded"

        self.assertIn('postgres_connections_ALL',
                self._conf['hostgroup']['hostname']['__graphs'])
        dl_graph = self._conf['hostgroup']['hostname']['__graphs']['postgres_connections_ALL']

        self.assertEquals(dl_graph['graph_title'], 'PostgreSQL connections')
        self.assertEquals(dl_graph['graph_args'], '--base 1000')
        self.assertEquals(dl_graph['graph_vlabel'], 'Connections')
        self.assertEquals(dl_graph['graph_category'], 'PostgreSQL')
        self.assertEquals(dl_graph['graph_order'], 'active waiting idle idletransaction unknown')

        self.assertEquals(dl_graph['meters']['waiting']['draw'], 'STACK')
        self.assertEquals(dl_graph['meters']['waiting']['min'], 'U')
        self.assertEquals(dl_graph['meters']['waiting']['max'], 'U')
        self.assertEquals(dl_graph['meters']['waiting']['label'], 'Waiting for lock')
        self.assertEquals(dl_graph['meters']['waiting']['type'], 'GAUGE')
        self.assertEquals(dl_graph['meters']['unknown']['draw'], 'STACK')
        self.assertEquals(dl_graph['meters']['unknown']['min'], 'U')
        self.assertEquals(dl_graph['meters']['unknown']['max'], 'U')
        self.assertEquals(dl_graph['meters']['unknown']['label'], 'Unknown')
        self.assertEquals(dl_graph['meters']['unknown']['type'], 'GAUGE')
        self.assertEquals(dl_graph['meters']['active']['draw'], 'AREA')
        self.assertEquals(dl_graph['meters']['active']['min'], 'U')
        self.assertEquals(dl_graph['meters']['active']['max'], 'U')
        self.assertEquals(dl_graph['meters']['active']['label'], 'Active')
        self.assertEquals(dl_graph['meters']['active']['type'], 'GAUGE')
        self.assertEquals(dl_graph['meters']['idletransaction']['draw'], 'STACK')
        self.assertEquals(dl_graph['meters']['idletransaction']['min'], 'U')
        self.assertEquals(dl_graph['meters']['idletransaction']['max'], 'U')
        self.assertEquals(dl_graph['meters']['idletransaction']['label'], 'Idle in transaction')
        self.assertEquals(dl_graph['meters']['idletransaction']['type'], 'GAUGE')
        self.assertEquals(dl_graph['meters']['idle']['draw'], 'STACK')
        self.assertEquals(dl_graph['meters']['idle']['min'], 'U')
        self.assertEquals(dl_graph['meters']['idle']['max'], 'U')
        self.assertEquals(dl_graph['meters']['idle']['label'], 'Idle')
        self.assertEquals(dl_graph['meters']['idle']['type'], 'GAUGE')

    def test_middle_graph(self):
        "Test if a graph in the 'middle' of the file is properly parsed"

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

