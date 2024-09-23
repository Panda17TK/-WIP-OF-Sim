import unittest
from core.emulator import Emulator
from utils.utility_functions import load_config, build_network_from_config, initialize_controllers

class TestNetworkConfig(unittest.TestCase):

    def setUp(self):
        self.emulator = Emulator()
        self.network_config = load_config('config/network_config.json')
        self.controller_config = load_config('config/controller_config.json')

    def test_network_and_controller_initialization(self):
        # ネットワーク構築
        build_network_from_config(self.emulator, self.network_config)
        self.assertEqual(len(self.emulator.nodes), len(self.network_config['nodes']))

        # コントローラ設定
        controllers = initialize_controllers(self.emulator, self.controller_config)
        self.assertEqual(len(controllers), len(self.controller_config['controllers']))

    def test_flow_entries(self):
        build_network_from_config(self.emulator, self.network_config)
        controllers = initialize_controllers(self.emulator, self.controller_config)
        switch = self.emulator.get_node_by_name("Switch1")
        self.assertIn(("10.0.0.1", "10.0.0.2"), switch.flow_table)

if __name__ == '__main__':
    unittest.main()