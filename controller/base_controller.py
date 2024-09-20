class BaseController:
    """
    コントローラの基底クラス。OpenFlowスイッチとの通信を管理し、
    ネットワークのフローを制御するための基本インターフェースを提供します。
    """

    def __init__(self):
        """
        コントローラの初期化。管理するスイッチのリストを初期化します。
        """
        self.switches = []  # コントローラが管理するスイッチのリスト

    def add_switch(self, switch):
        """
        コントローラにスイッチを追加し、管理対象にします。

        Args:
            switch (Switch): 管理するスイッチ。
        """
        self.switches.append(switch)
        # スイッチのコントローラを自身に設定
        switch.set_controller(self)

    def handle_packet_in(self, packet, switch, in_port):
        """
        スイッチからのPacket-Inメッセージを受信して処理を行います。

        Args:
            packet (Packet): 受信したパケット。
            switch (Switch): パケットを受信したスイッチ。
            in_port (int): パケットを受信したポート番号。
        """
        # サブクラスで具体的なロジックを実装
        raise NotImplementedError("このメソッドはサブクラスで実装する必要があります。")

    def send_flow_mod(self, switch, match, action):
        """
        スイッチにフローエントリを設定する（Flow-Mod）。

        Args:
            switch (Switch): フローを設定するスイッチ。
            match (tuple): フローのマッチ条件（通常は送信元と宛先アドレス）。
            action (dict): 実行するアクション（例: 特定のポートへの転送）。
        """
        switch.install_flow(match, action)