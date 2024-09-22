from components.node import Node
from core.packet import Packet

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

    def generate_packet(self, destination, payload="Test Packet"):
        """
        パケットを生成し、指定された宛先に送信します。

        Args:
            destination (str): 宛先のIPアドレス。
            payload (str): パケットのペイロードデータ。
        """
        packet = Packet(src=self.ip_address, dst=destination, payload=payload)
        # 送信ポートは仮に0とする
        self.send_packet(packet, 0)

    def send_packet(self, packet, port):
        """
        パケットを送信する際に呼び出されるメソッド。

        Args:
            packet (Packet): 送信するパケット。
            port (int): パケットを送信するポート番号。

        このメソッドは、ホストがパケットを送信する際に送信パケット数と送信バイト数を更新します。
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

        このメソッドは、ホストがパケットを受信する際に受信パケット数と受信バイト数を更新します。
        """
        # 受信パケット数と受信バイト数を更新
        self.received_packets += 1
        self.received_bytes += len(packet.payload)
        print(f"{self.name} がパケットを受信しました: {packet.payload}")

    def get_packets_sent(self):
        """
        送信パケット数を返します。

        Returns:
            int: ホストが送信したパケットの総数。

        このメソッドは、シミュレーション中にホストが送信した全てのパケット数を取得するために使用されます。
        """
        return self.sent_packets

    def get_packets_received(self):
        """
        受信パケット数を返します。

        Returns:
            int: ホストが受信したパケットの総数。

        このメソッドは、シミュレーション中にホストが受信した全てのパケット数を取得するために使用されます。
        """
        return self.received_packets

    def get_bytes_sent(self):
        """
        送信バイト数を返します。

        Returns:
            int: ホストが送信したデータの総バイト数。

        このメソッドは、シミュレーション中にホストが送信したデータの総バイト数を取得するために使用されます。
        """
        return self.sent_bytes

    def get_bytes_received(self):
        """
        受信バイト数を返します。

        Returns:
            int: ホストが受信したデータの総バイト数。

        このメソッドは、シミュレーション中にホストが受信したデータの総バイト数を取得するために使用されます。
        """
        return self.received_bytes