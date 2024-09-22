import time
import csv
import os
from datetime import datetime

class StatsCollector:
    """
    シミュレーション中のノードやリンクの統計データを収集し、記録するクラス。
    パケット数、バイト数、遅延、損失率などの情報を収集します。
    """

    def __init__(self, emulator):
        """
        StatsCollector の初期化。

        Args:
            emulator (Emulator): 統計データを収集する対象のエミュレータ。
        """
        self.emulator = emulator  # 統計を収集するエミュレータ
        self.data = {}  # 統計情報を格納する辞書
        self.running = False  # データ収集を管理するフラグ

    def start(self):
        """
        統計データの収集を開始します。
        """
        self.running = True
        # ノードがオブジェクトであることを確認してデータ収集用の辞書を初期化
        self.data = {node.name: {'packets_sent': 0, 'packets_received': 0, 'bytes_sent': 0, 'bytes_received': 0}
                    for node in self.emulator.nodes if isinstance(node, object) and hasattr(node, 'name')}
        print("統計データの収集を開始しました。")

    def stop(self):
        """
        統計データの収集を停止します。
        """
        self.running = False
        print("統計データの収集を停止しました。")

    def update_stats(self):
        """
        ノードやリンクの統計データを定期的に更新します。
        """
        while self.running:
            for node in self.emulator.nodes:
                # ノードがオブジェクトであり、送信/受信メソッドを持っていることを確認
                if isinstance(node, object) and hasattr(node, 'get_packets_sent'):
                    # ノードの送信・受信パケット数とバイト数を収集（仮の例）
                    self.data[node.name]['packets_sent'] += node.get_packets_sent()
                    self.data[node.name]['packets_received'] += node.get_packets_received()
                    self.data[node.name]['bytes_sent'] += node.get_bytes_sent()
                    self.data[node.name]['bytes_received'] += node.get_bytes_received()
            time.sleep(1)  # 1秒ごとに統計情報を更新

    def get_stats(self, node_name):
        """
        指定されたノードの統計データを取得します。

        Args:
            node_name (str): 統計データを取得するノードの名前。

        Returns:
            dict: 指定されたノードの統計データ、存在しない場合は None を返す。
        """
        return self.data.get(node_name, None)

    def print_stats(self):
        """
        収集された全てのノードの統計データを表示します。
        """
        for node_name, stats in self.data.items():
            print(f"ノード {node_name} の統計データ: {stats}")

    def save_to_csv(self, folder_path="results", file_prefix="network_stats"):
        """
        収集された統計データを指定されたフォルダに CSV ファイルとして保存します。
        フォルダが存在しない場合は作成し、ファイル名にタイムスタンプを付けて保存します。

        Args:
            folder_path (str): 保存するフォルダのパス（デフォルト: results）。
            file_prefix (str): 保存するファイル名の接頭辞（デフォルト: network_stats）。
        """
        # 結果保存用のフォルダが存在しない場合は作成
        if not os.path.exists(folder_path):
            os.makedirs(folder_path)
            print(f"結果保存用フォルダを作成しました: {folder_path}")

        # タイムスタンプ付きのファイル名を生成
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        file_path = os.path.join(folder_path, f"{file_prefix}_{timestamp}.csv")

        try:
            with open(file_path, mode='w', newline='', encoding='utf-8') as file:
                writer = csv.writer(file)
                # ヘッダー行の書き込み
                writer.writerow(["Node Name", "Packets Sent", "Packets Received", "Bytes Sent", "Bytes Received"])
                # 統計データの書き込み
                for node_name, stats in self.data.items():
                    writer.writerow([node_name, stats['packets_sent'], stats['packets_received'], stats['bytes_sent'], stats['bytes_received']])
            print(f"統計データを {file_path} に保存しました。")
        except Exception as e:
            print(f"統計データの保存に失敗しました: {e}")

    def update_stats(self):
        """
        ノードやリンクの統計データを定期的に更新します。
        """
        while self.running:
            for node in self.emulator.nodes:
                # ノードがオブジェクトであり、送信/受信メソッドを持っていることを確認
                if isinstance(node, object) and hasattr(node, 'get_packets_sent'):
                    # デバッグメッセージ: 統計データを更新するノードの名前を表示
                    print(f"ノード {node.name} の統計データを更新します。")

                    # ノードの送信・受信パケット数とバイト数を収集（仮の例）
                    self.data[node.name]['packets_sent'] += node.get_packets_sent()
                    self.data[node.name]['packets_received'] += node.get_packets_received()
                    self.data[node.name]['bytes_sent'] += node.get_bytes_sent()
                    self.data[node.name]['bytes_received'] += node.get_bytes_received()
            time.sleep(1)  # 1秒ごとに統計情報を更新