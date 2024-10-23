import random
import time
import queue
import threading

from components.node import Node
from components.host import Host

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

        # スレッド管理用
        self.lock = threading.Lock()
        self.processing_thread = threading.Thread(target=self._process_buffer)
        self.processing_thread.daemon = True  # メインスレッドが終了したら停止する
        self.processing_thread.start()

        # リンクをノードに追加
        self.node1.add_link(self)
        self.node2.add_link(self)

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

    def _process_buffer(self):
        """
        バッファ内のパケットを処理します。
        同時に処理できるパケット数に上限を設定し、超えた分は待機させます。
        """
        while True:
            with self.lock:
                if not self.buffer.empty() and self.currently_processing < self.processing_limit:
                    packet = self.buffer.get()
                    self.currently_processing += 1
                    threading.Thread(target=self._transfer_with_delay, args=(packet,)).start()

            time.sleep(0.01)  # 少し待機して次のチェックに進む

    def _transfer_with_delay(self, packet):
        """
        リンクの遅延をシミュレートし、遅延後にパケットを宛先ノードに転送します。
        """
        time.sleep(self.delay / 1000.0)  # 遅延のシミュレーション

        # ノードの種類に応じて宛先ノードを決定
        if isinstance(self.node1, Host) and packet.src != self.node1.ip_address:
            dest_node = self.node1
        else:
            dest_node = self.node2
        
        # 宛先ノードへのパケット転送
        in_port = self.get_port_number(dest_node)
        dest_node.receive_packet(packet, in_port)

        # 処理が終了したことを記録
        with self.lock:
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