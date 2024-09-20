import random
import time

class Link:
    """
    2つのノードを接続するネットワークリンクを表します。
    パケット転送を行い、帯域幅、遅延、パケット損失率などの特性をシミュレートします。
    """

    def __init__(self, node1, node2, bandwidth=100, delay=10, packet_loss_rate=0.0):
        """
        リンクを初期化します。

        Args:
            node1 (Node): リンクで接続される最初のノード。
            node2 (Node): リンクで接続される2番目のノード。
            bandwidth (int): リンクの帯域幅（Mbps）。
            delay (int): リンクの遅延（ミリ秒）。
            packet_loss_rate (float): パケット損失率（0.0〜1.0）。
        """
        self.node1 = node1
        self.node2 = node2
        self.bandwidth = bandwidth
        self.delay = delay
        self.packet_loss_rate = packet_loss_rate

    def transfer_packet(self, packet, src_node):
        """
        ソースノードから宛先ノードへパケットを転送します。
        リンクの遅延やパケット損失のシミュレーションを行います。

        Args:
            packet (Packet): 転送するパケット。
            src_node (Node): パケットを送信したソースノード。
        """
        # パケット損失率に基づいてパケットをドロップするかを決定
        if random.random() < self.packet_loss_rate:
            print(f"リンク ({self.node1.name} - {self.node2.name}) でパケットが損失しました。")
            return

        # 転送遅延をシミュレーション
        time.sleep(self.delay / 1000.0)

        # 宛先ノードを決定し、パケットを送信
        dest_node = self.node1 if src_node == self.node2 else self.node2
        dest_node.receive_packet(packet, self)