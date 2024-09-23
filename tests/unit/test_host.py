import unittest
from components.host import Host
from core.packet import Packet

class TestHost(unittest.TestCase):

    def setUp(self):
        self.host = Host("Host1", "10.0.0.1", "00:00:00:00:00:01")

    def test_initialization(self):
        self.assertEqual(self.host.name, "Host1")
        self.assertEqual(self.host.ip_address, "10.0.0.1")
        self.assertEqual(self.host.mac_address, "00:00:00:00:00:01")

    def test_packet_generation(self):
        packet = Packet(
            src_ip="10.0.0.1",
            dst_ip="10.0.0.2",
            src_mac="00:00:00:00:00:01",
            dst_mac="00:00:00:00:00:02",
            protocol="TCP",
            payload="Test payload"
        )
        self.host.send_packet(packet, 0)
        self.assertEqual(self.host.get_packets_sent(), 1)
        self.assertEqual(self.host.get_bytes_sent(), len("Test payload"))

    def test_receive_packet(self):
        packet = Packet(
            src_ip="10.0.0.2",
            dst_ip="10.0.0.1",
            src_mac="00:00:00:00:00:02",
            dst_mac="00:00:00:00:00:01",
            protocol="TCP",
            payload="Test payload"
        )
        self.host.receive_packet(packet, 0)
        self.assertEqual(self.host.get_packets_received(), 1)
        self.assertEqual(self.host.get_bytes_received(), len("Test payload"))

if __name__ == '__main__':
    unittest.main()