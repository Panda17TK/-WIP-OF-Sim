from components.node import Node
from core.packet import Packet

class Host(Node):
    """
    ネットワークホスト（エンドデバイス）を表します。
    パケットの生成と受信を行い、特定のトラフィックを生成することができます。
    """

    def __init__(self, name, ip_address, mac_address):
        """
        ホストを初期化します。

        Args:
            name (str): ホストの名前。
            ip_address (str): ホストのIPアドレス。
            mac_address (str): ホストのMACアドレス。
        """
        super().__init__(name)
        self.ip_address = ip_address
        self.mac_address = mac_address

    def generate_packet(self, dst_ip, payload):
        """
        新しいパケットを生成し、ホストから送信します。

        Args:
            dst_ip (str): パケットの宛先IPアドレス。
            payload (str): パケットに含まれるデータ。
        """
        # このホストを送信元としてパケットを作成
        packet = Packet(src=self.ip_address, dst=dst_ip, payload=payload)
        # ポート0（シンプルな構成の場合）からパケットを送信
        self.send_packet(packet, 0)

    def receive_packet(self, packet, in_port=None):
        """
        パケットを受信し、処理を行います。

        Args:
            packet (Packet): 受信したパケット。
            in_port (int or None): パケットを受信したポート番号（オプション）。
        """
        print(f"ホスト {self.name} がパケットを受信しました: {packet.get_info()}")