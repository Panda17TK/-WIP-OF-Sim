# components/node.py

class Node:
    """
    ネットワーク内の基本ノードを表します。
    ホストやスイッチなど、ネットワーク内のすべてのデバイスの基本クラスとなります。
    ノード間はリンクを介して接続され、パケットを送受信します。
    """

    def __init__(self, name):
        """
        ノードの初期化。

        Args:
            name (str): ノードの名前。
        """
        self.name = name  # ノードの名前
        self.links = []  # このノードに接続されているリンクのリスト
        # 統計情報の初期化
        self.sent_packets = 0  # 送信したパケット数
        self.received_packets = 0  # 受信したパケット数
        self.sent_bytes = 0  # 送信したバイト数
        self.received_bytes = 0  # 受信したバイト数

    def add_link(self, link):
        """
        ノードにリンクを追加します。

        Args:
            link (Link): ノードに追加するリンク。
        """
        self.links.append(link)

    def receive_packet(self, packet, in_port=None):
        """
        パケットを受信し、処理を行います。
        サブクラスでオーバーライド可能です。

        Args:
            packet (Packet): 受信したパケット。
            in_port (int or None): パケットを受信したポート番号（オプション）。
        """
        # 受信したパケット数とバイト数を更新
        self.received_packets += 1
        self.received_bytes += len(packet.payload)
        # パケット受信の情報を表示
        print(f"{self.name} がパケットを受信しました: {packet.get_info()} (ポート {in_port})")

    def send_packet(self, packet, out_port):
        """
        指定されたポートからパケットを送信します。

        Args:
            packet (Packet): 送信するパケット。
            out_port (int): 送信先のポート番号。
        """
        # 指定されたポートが有効か確認
        if out_port < len(self.links):
            link = self.links[out_port]
            # 送信したパケット数とバイト数を更新
            self.sent_packets += 1
            self.sent_bytes += len(packet.payload)
            # パケット送信の情報を表示
            print(f"{self.name} からパケットを送信しました: {packet.get_info()} (ポート {out_port})")
            # リンクを介してパケットを転送
            link.transfer_packet(packet, self)
        else:
            print(f"{self.name} のポート {out_port} は無効です。")

    def get_packets_sent(self):
        """
        送信パケット数を返します。

        Returns:
            int: ノードが送信したパケットの総数。
        """
        return self.sent_packets

    def get_packets_received(self):
        """
        受信パケット数を返します。

        Returns:
            int: ノードが受信したパケットの総数。
        """
        return self.received_packets

    def get_bytes_sent(self):
        """
        送信バイト数を返します。

        Returns:
            int: ノードが送信したデータの総バイト数。
        """
        return self.sent_bytes

    def get_bytes_received(self):
        """
        受信バイト数を返します。

        Returns:
            int: ノードが受信したデータの総バイト数。
        """
        return self.received_bytes