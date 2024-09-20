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

        # リンクのポート番号を決定する
        in_port = self.get_port_number(dest_node)

        dest_node.receive_packet(packet, in_port)

    def get_port_number(self, node):
        """
        ノードに接続されているこのリンクのポート番号を取得します。

        Args:
            node (Node): ノード（送信先または受信元のノード）。

        Returns:
            int: ノード内のリンクのインデックスとしてのポート番号。
        """
        # node.links の中でこのリンクが何番目にあるか（ポート番号）を返す
        return node.links.index(self)