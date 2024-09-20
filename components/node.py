class Node:
    """
    ネットワーク内の基本ノードを表します。
    ホストやスイッチなど、ネットワーク内のすべてのデバイスの基本クラスとなります。
    ノード間はリンクを介して接続され、パケットを送受信します。
    """

    def __init__(self, name):
        """
        ノードを初期化します。

        Args:
            name (str): ノードの名前。
        """
        self.name = name
        self.links = []  # このノードに接続されているリンクのリスト

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
            # リンクを介してパケットを転送
            link.transfer_packet(packet, self)
        else:
            print(f"{self.name} のポート {out_port} は無効です。")