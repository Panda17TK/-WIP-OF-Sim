import time

class SimulationMonitor:
    """
    シミュレーション内の各ノードの状態やパフォーマンスをモニタリングするクラス。
    ノードのパケット送受信量や内部状態を監視し、デバッグや性能評価に役立てます。
    """

    def __init__(self, emulator, interval=1):
        """
        SimulationMonitor の初期化。

        Args:
            emulator (Emulator): 監視対象のエミュレータインスタンス。
            interval (int): モニタリングの間隔（秒）。
        """
        self.emulator = emulator  # 監視対象のエミュレータ
        self.interval = interval  # モニタリングの間隔
        self.running = False  # モニタリングの実行状態を管理するフラグ

    def start(self):
        """
        モニタリングを開始します。システムの状態を定期的に出力します。
        """
        self.running = True
        print("シミュレーションモニタリングを開始します。")
        while self.running:
            self.monitor_simulation()
            time.sleep(self.interval)

    def stop(self):
        """
        モニタリングを停止します。
        """
        self.running = False
        print("シミュレーションモニタリングを停止しました。")

    def monitor_simulation(self):
        """
        エミュレータ内の各ノードの状態をモニタリングし、情報を出力します。
        """
        for node in self.emulator.nodes:
            sent_packets = node.get_packets_sent()
            received_packets = node.get_packets_received()
            sent_bytes = node.get_bytes_sent()
            received_bytes = node.get_bytes_received()

            print(f"ノード {node.name}: 送信パケット数 = {sent_packets}, 受信パケット数 = {received_packets}, "
                f"送信バイト数 = {sent_bytes}, 受信バイト数 = {received_bytes}")