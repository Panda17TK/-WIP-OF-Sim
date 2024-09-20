from controller.base_controller import BaseController

class CustomController(BaseController):
    """
    カスタムコントローラの実装。
    スイッチからのPacket-Inメッセージを受け取り、適切なフローエントリを設定します。
    """

    def handle_packet_in(self, packet, switch, in_port):
        """
        スイッチからのPacket-Inメッセージを受信し、フローエントリを設定します。

        Args:
            packet (Packet): 受信したパケット。
            switch (Switch): パケットを受信したスイッチ。
            in_port (int): パケットを受信したポート番号。
        """
        print(f"カスタムコントローラがパケットを受信しました: {packet.get_info()}")

        # MACアドレスに基づくシンプルなフロー設定
        match = (packet.src, packet.dst)
        
        # 送信元と宛先が異なる場合に転送フローを設定
        if packet.src != packet.dst:
            # 簡単なルールに基づいてポートを設定（仮の設定）
            out_port = (in_port + 1) % len(switch.links)
            action = {"out_port": out_port}
            self.send_flow_mod(switch, match, action)  # 親クラスのメソッドを直接呼び出す
            print(f"フローエントリを設定: {match} -> ポート {out_port}")
        else:
            print(f"無効なフロー: {packet.get_info()}")

    def receive_packet_in(self, packet, switch, in_port):
        """
        スイッチからのパケット受信（Packet-In）メッセージを処理し、
        必要に応じてフローエントリを設定します。

        Args:
            packet (Packet): 受信したパケット。
            switch (Switch): パケットを受信したスイッチ。
            in_port (int): パケットを受信したポート番号。
        """
        print(f"カスタムコントローラがパケットを受信しました: {packet.get_info()}")

        # 送信元と宛先アドレスに基づくマッチ条件を定義
        match = (packet.src, packet.dst)

        # 送信元と宛先が異なる場合に転送フローを設定
        if packet.src != packet.dst:
            # 簡単なルールに基づいてポートを設定（ここでは次のポートを使用）
            out_port = (in_port + 1) % len(switch.links)
            action = {"out_port": out_port}
            self.send_flow_mod(switch, match, action)
            print(f"フローエントリを設定: {match} -> ポート {out_port}")
        else:
            print(f"無効なフロー: {packet.get_info()}")

    def send_flow_mod(self, switch, match, action):
        """
        スイッチにフローエントリを設定します。

        Args:
            switch (Switch): フローを設定するスイッチ。
            match (tuple): フローのマッチ条件（送信元と宛先アドレス）。
            action (dict): 実行するアクション（例: 特定のポートへの転送）。
        """
        print(f"フローエントリをスイッチ {switch.name} に設定: {match} -> {action}")
        # 親クラスのメソッドを直接呼び出す
        BaseController.send_flow_mod(self, switch, match, action)