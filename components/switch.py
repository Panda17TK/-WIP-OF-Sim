from components.node import Node

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
        """
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
        """
        self.flow_table[match] = action

    def send_packet_to_controller(self, packet, in_port):
        """
        コントローラにPacket-Inメッセージを送信します。

        Args:
            packet (Packet): コントローラに送信するパケット。
            in_port (int): パケットを受信したポート番号。
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
        """
        # 指定されたポートが有効か確認
        if out_port < len(self.links):
            link = self.links[out_port]
            # リンクを介してパケットを転送
            link.transfer_packet(packet, self)
        else:
            print(f"{self.name} のポート {out_port} は無効です。")