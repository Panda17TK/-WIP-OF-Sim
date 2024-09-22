from components.node import Node
from core.packet import Packet

class Switch(Node):
    """
    OpenFlow対応のネットワークスイッチを表します。
    フローテーブルを管理し、フローエントリに基づいてパケットを転送します。
    """

    def __init__(self, name):
        """
        スイッチを初期化します。

        Args:
            name (str): スイッチの名前。
        """
        super().__init__(name)
        self.flow_table = {}  # フローテーブル（マッチ条件 -> アクションの辞書）
        self.controller = None  # コントローラの参照を保持

        # 統計情報の初期化
        self.sent_packets = 0  # 送信したパケット数
        self.received_packets = 0  # 受信したパケット数
        self.sent_bytes = 0  # 送信したバイト数
        self.received_bytes = 0  # 受信したバイト数

    def set_controller(self, controller):
        """
        スイッチにコントローラを設定します。

        Args:
            controller (BaseController): コントローラのインスタンス。
        """
        self.controller = controller

    def receive_packet(self, packet, in_port):
        """
        パケットを受信し、フローテーブルに基づいて処理を行います。

        Args:
            packet (Packet): スイッチが受信したパケット。
            in_port (int): パケットを受信したポート番号。

        パケットを受信する際に、受信パケット数と受信バイト数を更新します。
        """
        # 受信パケット数と受信バイト数を更新
        self.received_packets += 1
        self.received_bytes += len(packet.payload)
        print(f"{self.name} がパケットを受信しました: {packet.payload}")

        # パケットの送信元と宛先に基づいてフローテーブルを確認
        key = (packet.src, packet.dst)
        if key in self.flow_table:
            # フローテーブルに一致するエントリがある場合、アクションを取得
            action = self.flow_table[key]
            # アクションに基づいてパケットを転送
            self.send_packet(packet, action["out_port"])
        else:
            # フローテーブルに一致するエントリがない場合、コントローラにパケットを送信
            print(f"{self.name}: パケットに対するフローエントリが存在しません: {packet.get_info()}")
            self.send_packet_to_controller(packet, in_port)

    def install_flow(self, match, action):
        """
        フローテーブルに新しいフローエントリをインストールします。

        Args:
            match (tuple): マッチ条件（通常は送信元と宛先アドレス）。
            action (dict): 実行するアクション（例: 特定のポートへの転送）。

        新しいフローエントリを追加して、特定のパケットに対する処理を定義します。
        """
        self.flow_table[match] = action

    def send_packet_to_controller(self, packet, in_port):
        """
        コントローラにPacket-Inメッセージを送信します。

        Args:
            packet (Packet): コントローラに送信するパケット。
            in_port (int): パケットを受信したポート番号。

        スイッチにフローエントリが存在しない場合、コントローラにパケットを転送して
        フローの設定を要求します。
        """
        if self.controller:
            # コントローラにパケットを送信
            self.controller.handle_packet_in(packet, self, in_port)
        else:
            print(f"{self.name}: コントローラが設定されていません。")

    def send_packet(self, packet, out_port):
        """
        指定されたポートからパケットを送信します。

        Args:
            packet (Packet): 送信するパケット。
            out_port (int): 送信先のポート番号。

        パケットを送信する際に、送信パケット数と送信バイト数を更新します。
        """
        # 指定されたポートが有効か確認
        if out_port < len(self.links):
            link = self.links[out_port]
            # 送信パケット数と送信バイト数を更新
            self.sent_packets += 1
            self.sent_bytes += len(packet.payload)
            print(f"{self.name} からパケットを送信しました: {packet.payload}")
            # リンクを介してパケットを転送
            link.transfer_packet(packet, self)
        else:
            print(f"{self.name} のポート {out_port} は無効です。")

    def get_packets_sent(self):
        """
        送信パケット数を返します。

        Returns:
            int: スイッチが送信したパケットの総数。

        このメソッドは、シミュレーション中にスイッチが送信した全てのパケット数を取得するために使用されます。
        """
        return self.sent_packets

    def get_packets_received(self):
        """
        受信パケット数を返します。

        Returns:
            int: スイッチが受信したパケットの総数。

        このメソッドは、シミュレーション中にスイッチが受信した全てのパケット数を取得するために使用されます。
        """
        return self.received_packets

    def get_bytes_sent(self):
        """
        送信バイト数を返します。

        Returns:
            int: スイッチが送信したデータの総バイト数。

        このメソッドは、シミュレーション中にスイッチが送信したデータの総バイト数を取得するために使用されます。
        """
        return self.sent_bytes

    def get_bytes_received(self):
        """
        受信バイト数を返します。

        Returns:
            int: スイッチが受信したデータの総バイト数。

        このメソッドは、シミュレーション中にスイッチが受信したデータの総バイト数を取得するために使用されます。
        """
        return self.received_bytes