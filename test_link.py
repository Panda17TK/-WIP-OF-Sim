import unittest
from components.node import Node
from components.link import Link
from components.host import Host
from components.switch import Switch
from core.packet import Packet
import time

class TestLink(unittest.TestCase):
    
    def setUp(self):
        # テスト用のノードを作成
        self.node1 = Node("Node1")
        self.node2 = Node("Node2")
        
        # リンクを作成
        self.link = Link(self.node1, self.node2, bandwidth=100, delay=50, packet_loss_rate=0.1, buffer_size=5)
    
    def test_packet_transfer_host_to_switch(self):
        host = Host("Host1", ip_address="10.0.0.1", mac_address="AA:BB:CC:DD:EE:01")
        switch = Switch("Switch1")

        # リンク作成
        link = Link(host, switch)
        
        # Switchにフローテーブルを追加
        switch.install_flow(("10.0.0.1", "10.0.0.2"), {"out_port": 0})
        
        # パケットをホストからスイッチに送信
        packet = Packet(src=host.ip_address, dst="10.0.0.2", payload="Test Packet")
        host.send_packet(packet, 0)
        
        # Switchがパケットを受信したことを確認
        self.assertEqual(switch.get_packets_received(), 1)
    
    def test_packet_loss(self):
        packet_count = 100
        lost_packets = 0

        # リンクの損失率を 10% に設定
        link = Link(self.node1, self.node2, packet_loss_rate=0.1, buffer_size=200)
        
        for i in range(packet_count):
            packet = Packet(src=self.node1.name, dst=self.node2.name, payload=f"Packet {i}")
            link.transfer_packet(packet, self.node1)
            if link.buffer.qsize() < i + 1:
                lost_packets += 1

        actual_loss_rate = lost_packets / packet_count
        self.assertAlmostEqual(actual_loss_rate, 0.1, delta=0.05)

    def test_buffer_overflow(self):
        # バッファサイズを確認（バッファサイズは5）
        self.assertEqual(self.link.buffer.maxsize, 5)

        # バッファサイズを超えるパケットを転送
        for i in range(10):
            packet = Packet(src=self.node1.name, dst=self.node2.name, payload=f"Packet {i}")
            self.link.transfer_packet(packet, self.node1)

        # バッファが満杯か確認
        self.assertTrue(self.link.buffer.full())
        self.assertEqual(self.link.buffer.qsize(), 5)  # 最大サイズ5で制限されるはず

    def test_packet_processing(self):
        # パケットを転送
        packet = Packet(src=self.node1.name, dst=self.node2.name, payload="Test Packet")
        self.link.transfer_packet(packet, self.node1)

        # バッファが処理されるまで少し待つ
        time.sleep(0.1)

        # 現在処理中のパケット数が0であることを確認
        self.assertEqual(self.link.currently_processing, 0)
    
    def test_link_delay(self):
        # パケットを転送し、遅延をシミュレーション
        packet = Packet(src=self.node1.name, dst=self.node2.name, payload="Test Packet with Delay")

        start_time = time.time()
        self.link.transfer_packet(packet, self.node1)

        # パケットが転送される時間を確認
        time.sleep(self.link.delay / 1000.0 + 0.1)  # 遅延時間 + 少し待機
        end_time = time.time()

        # 遅延が正しく適用されたか確認
        self.assertGreaterEqual(end_time - start_time, self.link.delay / 1000.0)

if __name__ == "__main__":
    unittest.main()