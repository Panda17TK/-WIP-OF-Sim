from components.node import Node
from queue import Queue

class Switch(Node):
    """
    OpenFlow対応のネットワークスイッチを表します。
    フローテーブルを管理し、フローエントリに基づいてパケットを転送します。
    """

    def __init__(self, name, processing_limit=10, buffer_size=20):
        """
        スイッチを初期化します。

        Args:
            name (str): スイッチの名前。
            processing_limit (int): 同時に処理できるパケット数の上限。
            buffer_size (int): スイッチのバッファサイズ（待ち行列の最大数）。
        """
        super().__init__(name)
        self.flow_table = {}  # フローテーブル（マッチ条件 -> アクションの辞書）
        self.controller = None  # コントローラの参照を保持
        self.buffer = Queue(maxsize=buffer_size)  # スイッチの待ち行列
        self.processing_limit = processing_limit  # 同時に処理できるパケット数の上限
        self.currently_processing = 0  # 現在処理中のパケット数
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
        """
        # 受信パケット数と受信バイト数を更新
        self.received_packets += 1
        self.received_bytes += len(packet.payload)
        print(f"{self.name} がパケットを受信しました: {packet.payload}")

        # バッファに空きがあるか確認
        if self.buffer.full():
            print(f"{self.name}: バッファが満杯です。パケットをドロップします。")
            return

        # バッファにパケットを追加
        self.buffer.put((packet, in_port))
        print(f"{self.name}: バッファにパケットを追加しました。")

        # バッファの処理を非同期で行う
        self._process_buffer()

    def _process_buffer(self):
        """
        バッファ内のパケットを処理します。
        同時に処理できるパケット数に上限を設定し、超えた分は待機させます。
        """
        if self.currently_processing < self.processing_limit and not self.buffer.empty():
            packet, in_port = self.buffer.get()
            self.currently_processing += 1

            # パケットの送信元と宛先に基づいてフローテーブルを確認
            key = (packet.src, packet.dst)
            if key in self.flow_table:
                # フローテーブルに一致するエントリがある場合、アクションを取得
                action = self.flow_table[key]
                # アクションに基づいてパケットを転送
                self.send_packet(packet, action["out_port"])
            else:
                # フローテーブルに一致するエントリがない場合、コントローラにパケットを送信
                if self.controller:
                    print(f"{self.name}: パケットに対するフローエントリが存在しないため、コントローラに問い合わせます。")
                    self.send_packet_to_controller(packet, in_port)
                else:
                    print(f"{self.name}: コントローラが設定されていません。")

            # 処理が終了したことを記録
            self.currently_processing -= 1

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
            # 送信パケット数と送信バイト数を更新
            self.sent_packets += 1
            self.sent_bytes += len(packet.payload)
            print(f"{self.name} からパケットを送信しました: {packet.payload}")
            # リンクを介してパケットを転送
            link.transfer_packet(packet, self)
        else:
            print(f"{self.name} のポート {out_port} は無効です。")

    # 統計情報取得用のメソッド
    def get_packets_sent(self):
        """
        送信パケット数を返します。
        Returns:
            int: スイッチが送信したパケットの総数。
        """
        return self.sent_packets

    def get_packets_received(self):
        """
        受信パケット数を返します。
        Returns:
            int: スイッチが受信したパケットの総数。
        """
        return self.received_packets

    def get_bytes_sent(self):
        """
        送信バイト数を返します。
        Returns:
            int: スイッチが送信したデータの総バイト数。
        """
        return self.sent_bytes

    def get_bytes_received(self):
        """
        受信バイト数を返します。
        Returns:
            int: スイッチが受信したデータの総バイト数。
        """
        return self.received_bytes
