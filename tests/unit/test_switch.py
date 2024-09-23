
import unittest
from components.switch import Switch
from core.packet import Packet

class TestSwitch(unittest.TestCase):

    def setUp(self):
        self.switch = Switch("Switch1")

    def test_initialization(self):
        self.assertEqual(self.switch.name, "Switch1")
        self.assertEqual(len(self.switch.flow_table), 0)

    def test_install_flow(self):
        self.switch.install_flow(("10.0.0.1", "10.0.0.2"), {"out_port": 1})
        self.assertIn(("10.0.0.1", "10.0.0.2"), self.switch.flow_table)
        self.assertEqual(self.switch.flow_table[("10.0.0.1", "10.0.0.2")], {"out_port": 1})

    def test_receive_packet_with_no_flow_entry(self):
        packet = Packet(
            src_ip="10.0.0.1",
            dst_ip="10.0.0.2",
            src_mac="00:00:00:00:00:01",
            dst_mac="00:00:00:00:00:02",
            protocol="TCP",
            payload="Test payload"
        )
        with self.assertLogs() as log:
            self.switch.receive_packet(packet, 0)
            self.assertIn("パケットに対するフローエントリが存在しません", log.output[0])

if __name__ == '__main__':
    unittest.main()