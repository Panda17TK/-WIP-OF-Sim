import random
import time
import queue

class Link:
    """
    2つのノードを接続するネットワークリンクを表します。
    パケット転送を行い、帯域幅、遅延、パケット損失率などの特性をシミュレートします。
    """

    def __init__(self, node1, node2, bandwidth=100, delay=10, packet_loss_rate=0.0, buffer_size=10):
        """
        リンクを初期化します。

        Args:
            node1 (Node): リンクで接続される最初のノード。
            node2 (Node): リンクで接続される2番目のノード。
            bandwidth (int): リンクの帯域幅（Mbps）。
            delay (int): リンクの遅延（ミリ秒）。
            packet_loss_rate (float): パケット損失率（0.0〜1.0）。
            buffer_size (int): リンクのバッファサイズ（待ち行列の最大数）。
        """
        self.node1 = node1
        self.node2 = node2
        self.bandwidth = bandwidth
        self.delay = delay
        self.packet_loss_rate = packet_loss_rate
        self.buffer = queue.Queue(maxsize=buffer_size)  # バッファを初期化
        self.currently_processing = 0  # 現在処理中のパケット数
        self.processing_limit = bandwidth // 10  # 処理できるパケット数を帯域幅に応じて設定

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

        # バッファに空きがあるか確認
        if self.buffer.full():
            print(f"リンク ({self.node1.name} - {self.node2.name}) のバッファが満杯です。パケットをドロップします。")
            return

        # バッファにパケットを追加
        self.buffer.put(packet)
        print(f"リンク ({self.node1.name} - {self.node2.name}) のバッファにパケットを追加しました。")

        # バッファの処理を非同期で行う
        self._process_buffer()

    def _process_buffer(self):
        """
        バッファ内のパケットを処理します。
        同時に処理できるパケット数に上限を設定し、超えた分は待機させます。
        """
        if self.currently_processing < self.processing_limit and not self.buffer.empty():
            packet = self.buffer.get()
            self.currently_processing += 1
            # 転送遅延をシミュレーション
            time.sleep(self.delay / 1000.0)

            # 宛先ノードを決定し、パケットを送信
            dest_node = self.node1 if packet.src_ip != self.node1.ip_address else self.node2
            in_port = self.get_port_number(dest_node)

            # 宛先ノードにパケットを転送
            dest_node.receive_packet(packet, in_port)

            # 処理が終了したことを記録
            self.currently_processing -= 1

    def get_port_number(self, node):
        """
        ノードに接続されているこのリンクのポート番号を取得します。

        Args:
            node (Node): ノード（送信先または受信元のノード）。

        Returns:
            int: ノード内のリンクのインデックスとしてのポート番号。
        """
        return node.links.index(self)