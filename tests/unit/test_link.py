import unittest
from components.link import Link
from components.host import Host
from core.packet import Packet

class TestLink(unittest.TestCase):

    def setUp(self):
        self.host1 = Host("Host1", "10.0.0.1", "00:00:00:00:00:01")
        self.host2 = Host("Host2", "10.0.0.2", "00:00:00:00:00:02")
        self.link = Link(self.host1, self.host2, bandwidth=100, delay=10, packet_loss_rate=0.1)

    def test_initialization(self):
        self.assertEqual(self.link.bandwidth, 100)
        self.assertEqual(self.link.delay, 10)
        self.assertEqual(self.link.packet_loss_rate, 0.1)

    def test_transfer_packet(self):
        packet = Packet(
            src_ip="10.0.0.1",
            dst_ip="10.0.0.2",
            src_mac="00:00:00:00:00:01",
            dst_mac="00:00:00:00:00:02",
            protocol="TCP",
            payload="Test payload"
        )
        with self.assertLogs() as log:
            self.link.transfer_packet(packet, self.host1)
            self.assertIn("リンク (Host1 - Host2) のバッファにパケットを追加しました", log.output[0])

if __name__ == '__main__':
    unittest.main()