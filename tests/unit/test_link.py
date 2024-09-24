import unittest
from components.host import Host
from components.link import Link
from core.packet import Packet

class TestLink(unittest.TestCase):
    def setUp(self):
        self.host1 = Host(name="Host1", ip_address="10.0.0.1", mac_address="00:00:00:00:00:01")
        self.host2 = Host(name="Host2", ip_address="10.0.0.2", mac_address="00:00:00:00:00:02")
        self.link = Link(node1=self.host1, node2=self.host2)

        # リンクの初期化確認
        self.assertIn(self.link, self.host1.links, f"リンクが {self.host1.name} に追加されていません")
        self.assertIn(self.link, self.host2.links, f"リンクが {self.host2.name} に追加されていません")

    def test_transfer_packet(self):
        packet = Packet(
            src="10.0.0.1",
            dst="10.0.0.2",
            payload="Test Payload",
            protocol="TCP"
        )

        # transfer_packet メソッド呼び出し前にノードのリンク状態を確認
        print(f"Host1 links before transfer: {self.host1.links}")
        print(f"Host2 links before transfer: {self.host2.links}")

        self.link.transfer_packet(packet, self.host1)

        # パケットが正しく転送されたことを確認
        self.assertEqual(self.host2.get_packets_received(), 1, "パケットが Host2 に到達していません")