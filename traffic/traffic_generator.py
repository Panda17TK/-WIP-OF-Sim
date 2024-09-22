import threading
import time
from core.packet import Packet

class TrafficGenerator:
    """
    テスト用トラフィックを生成するクラス。
    特定の送信元から宛先に向けて、定期的にパケットを生成し送信します。
    """

    def __init__(self, source, destination, interval=1.0, payload="Test Packet"):
        """
        TrafficGenerator の初期化。

        Args:
            source (Host): 送信元のホスト。
            destination (str): 宛先のIPアドレス。
            interval (float): パケットを生成する間隔（秒）。
            payload (str): 送信するパケットのペイロード。
        """
        self.source = source  # 送信元ホスト
        self.destination = destination  # 宛先IPアドレス
        self.interval = interval  # パケットを生成する間隔
        self.payload = payload  # パケットのペイロード
        self.running = False  # トラフィック生成を管理するフラグ
        self.thread = None  # トラフィック生成用のスレッド

    def start(self):
        """
        トラフィック生成を開始します。
        """
        self.running = True
        self.thread = threading.Thread(target=self._generate_traffic)
        self.thread.start()  # 新しいスレッドでトラフィック生成を開始
        print(f"トラフィック生成を開始しました: {self.source.name} -> {self.destination}")

    def stop(self):
        """
        トラフィック生成を停止します。
        """
        self.running = False
        if self.thread:
            self.thread.join()  # スレッドの終了を待つ
        print(f"トラフィック生成を停止しました: {self.source.name} -> {self.destination}")

    def _generate_traffic(self):
        """
        内部メソッド: 指定した間隔でパケットを生成し、送信元ホストから送信します。
        """
        while self.running:
            packet = Packet(src=self.source.ip_address, dst=self.destination, payload=self.payload)
            self.source.send_packet(packet, 0)  # 送信元ホストからパケットを送信
            print(f"{self.source.name} から {self.destination} へパケットを送信しました: {self.payload}")
            time.sleep(self.interval)  # 次のパケット生成までの間隔を待機