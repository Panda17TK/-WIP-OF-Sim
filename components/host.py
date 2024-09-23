from components.node import Node
from core.packet import Packet
import threading
import time

class Host(Node):
    """
    ホストを表すクラス。ネットワークのエンドポイントとして、パケットの送受信を行います。
    """

    def __init__(self, name, ip_address, mac_address):
        """
        ホストの初期化。

        Args:
            name (str): ホストの名前。
            ip_address (str): ホストのIPアドレス。
            mac_address (str): ホストのMACアドレス。
        """
        super().__init__(name)
        self.ip_address = ip_address
        self.mac_address = mac_address
        # 統計情報の初期化
        self.sent_packets = 0
        self.received_packets = 0
        self.sent_bytes = 0
        self.received_bytes = 0
        self.packet_sending_thread = None  # パケット送信スレッド

    def generate_packet(self, destination_ip, payload):
        """
        新しいパケットを生成し、送信します。

        Args:
            destination_ip (str): 宛先の IP アドレス。
            payload (str): パケットのペイロード。
        """
        packet = Packet(
            src_ip=self.ip_address,
            dst_ip=destination_ip,
            src_mac=self.mac_address,
            dst_mac="ff:ff:ff:ff:ff:ff",  # ブロードキャスト MAC アドレス（仮）
            protocol="TCP",
            payload=payload
        )
        # 送信ポートはゼロで仮置き
        self.send_packet(packet, 0)

    def send_packet(self, packet, port):
        """
        パケットを送信する際に呼び出されるメソッド。

        Args:
            packet (Packet): 送信するパケット。
            port (int): パケットを送信するポート番号。
        """
        # 送信パケット数と送信バイト数を更新
        self.sent_packets += 1
        self.sent_bytes += len(packet.payload)
        print(f"{self.name} からパケットを送信しました: {packet.payload}")
        # パケットをリンクに転送（仮実装）
        if self.links:
            self.links[port].transfer_packet(packet, self)

    def receive_packet(self, packet, port):
        """
        パケットを受信する際に呼び出されるメソッド。

        Args:
            packet (Packet): 受信したパケット。
            port (int): パケットを受信したポート番号。
        """
        # 受信パケット数と受信バイト数を更新
        self.received_packets += 1
        self.received_bytes += len(packet.payload)
        print(f"{self.name} がパケットを受信しました: {packet.payload}")

    def start_sending_packets(self, dst_ip, payload, interval=1.0, duration=10):
        """
        パケット送信を一定間隔で繰り返すスレッドを開始します。

        Args:
            dst_ip (str): 送信先の IP アドレス。
            payload (str): パケットのペイロードデータ。
            interval (float): パケットを送信する間隔（秒）。
            duration (float): パケット送信を行う合計時間（秒）。
        """
        def send_packets():
            end_time = time.time() + duration
            while time.time() < end_time:
                self.generate_packet(dst_ip, payload)
                time.sleep(interval)

        # パケット送信スレッドを開始
        self.packet_sending_thread = threading.Thread(target=send_packets)
        self.packet_sending_thread.start()

    def stop_sending_packets(self):
        """
        パケット送信スレッドを停止します。
        """
        if self.packet_sending_thread and self.packet_sending_thread.is_alive():
            self.packet_sending_thread.join()  # スレッドの終了を待機

    # 統計情報取得用のメソッド
    def get_packets_sent(self):
        """
        送信パケット数を返します。
        Returns:
            int: ホストが送信したパケットの総数。
        """
        return self.sent_packets

    def get_packets_received(self):
        """
        受信パケット数を返します。
        Returns:
            int: ホストが受信したパケットの総数。
        """
        return self.received_packets

    def get_bytes_sent(self):
        """
        送信バイト数を返します。
        Returns:
            int: ホストが送信したデータの総バイト数。
        """
        return self.sent_bytes

    def get_bytes_received(self):
        """
        受信バイト数を返します。
        Returns:
            int: ホストが受信したデータの総バイト数。
        """
        return self.received_bytes