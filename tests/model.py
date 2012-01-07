import unittest2 as unittest
from muninbrowser.model import Group, Host, Graph

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

class TestGraphs(unittest.TestCase):

    def setUp(self):
        from muninbrowser.configparser import read
        from os.path import join, dirname
        conf_name = join(dirname(__file__), 'test_config.conf')
        self._conf = read(open(conf_name))

    def test_graphs(self):
        expected = set(['apt_upgradable', 'cpu', 'cpuspeed', 'df', 'df_inode',
            'diskstats_iops', 'diskstats_iops.sda', 'diskstats_iops.sdb',
            'diskstats_iops.sdc', 'diskstats_iops.sdd', 'diskstats_iops.sde',
            'diskstats_iops.md0', 'diskstats_iops.md1', 'diskstats_latency',
            'diskstats_latency.sda', 'diskstats_latency.sdb',
            'diskstats_latency.sdc', 'diskstats_latency.sdd',
            'diskstats_latency.sde', 'diskstats_throughput',
            'diskstats_throughput.sda', 'diskstats_throughput.sdb',
            'diskstats_throughput.sdc', 'diskstats_throughput.sdd',
            'diskstats_throughput.sde', 'diskstats_throughput.md0',
            'diskstats_throughput.md1', 'diskstats_utilization',
            'diskstats_utilization.sda', 'diskstats_utilization.sdb',
            'diskstats_utilization.sdc', 'diskstats_utilization.sdd',
            'diskstats_utilization.sde', 'du_backups', 'entropy',
            'exim_mailqueue', 'exim_mailstats', 'forks', 'fw_packets',
            'http_loadtime', 'if_err_eth0', 'if_eth0', 'interrupts', 'iostat',
            'iostat_ios', 'irqstats', 'load', 'lpstat', 'memory',
            'munin_stats', 'netstat', 'ntp_kernel_err', 'ntp_kernel_pll_freq',
            'ntp_kernel_pll_off', 'open_files', 'open_inodes',
            'postgres_bgwriter', 'postgres_cache_ALL',
            'postgres_cache_filemeta', 'postgres_cache_filemeta_old',
            'postgres_cache_travelguide_sa', 'postgres_cache_zlidr',
            'postgres_checkpoints', 'postgres_connections_ALL',
            'postgres_connections_db', 'postgres_connections_filemeta',
            'postgres_connections_filemeta_old',
            'postgres_connections_travelguide_sa',
            'postgres_connections_zlidr', 'postgres_locks_ALL',
            'postgres_locks_filemeta', 'postgres_locks_filemeta_old',
            'postgres_locks_travelguide_sa', 'postgres_locks_zlidr',
            'postgres_querylength_ALL', 'postgres_querylength_filemeta',
            'postgres_querylength_filemeta_old',
            'postgres_querylength_travelguide_sa',
            'postgres_querylength_zlidr', 'postgres_size_ALL',
            'postgres_size_filemeta', 'postgres_size_filemeta_old',
            'postgres_size_travelguide_sa', 'postgres_size_zlidr',
            'postgres_transactions_ALL', 'postgres_transactions_filemeta',
            'postgres_transactions_filemeta_old',
            'postgres_transactions_travelguide_sa',
            'postgres_transactions_zlidr', 'postgres_users', 'postgres_xlog',
            'processes', 'proc_pri', 'squid_cache', 'squid_objectsize',
            'squid_requests', 'squid_traffic', 'swap', 'threads', 'uptime',
            'users', 'vmstat', 'random_foo'])
        self.assertEquals(set(Graph.all_names(self._conf)), expected)

    def test_categories(self):
        expected = set(['PostgreSQL', 'disk', 'exim', 'munin', 'network',
                'printing', 'processes', 'squid', 'system', 'time'])
        self.assertEquals(Graph.all_categories(self._conf), expected)
