import unittest
from core.emulator import Emulator
from components.host import Host
from utils.utility_functions import load_config, build_network_from_config

class TestEmulator(unittest.TestCase):

    def setUp(self):
        self.emulator = Emulator()
        self.config = load_config('config/network_config.json')

    def test_network_initialization(self):
        build_network_from_config(self.emulator, self.config)
        self.assertEqual(len(self.emulator.nodes), len(self.config['nodes']))
        self.assertEqual(len(self.emulator.links), len(self.config['links']))

    def test_run_simulation(self):
        build_network_from_config(self.emulator, self.config)
        self.emulator.run_simulation(5)
        # シミュレーション後の各ノードの状態を確認
        for node in self.emulator.nodes.values():
            if isinstance(node, Host):
                self.assertGreaterEqual(node.get_packets_sent(), 0)
                self.assertGreaterEqual(node.get_packets_received(), 0)

if __name__ == '__main__':
    unittest.main()