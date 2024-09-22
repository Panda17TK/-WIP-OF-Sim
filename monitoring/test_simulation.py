from core.emulator import Emulator
from controller.custom_controller import CustomController
from topology.example_topology import create_mesh_topology
from traffic.flow_manager import FlowManager
from traffic.stats_collector import StatsCollector
from components.switch import Switch
from monitoring.monitor import SimulationMonitor
from monitoring.logger import EventLogger
from monitoring.visualizer import NetworkVisualizer

# エミュレータとカスタムコントローラのインスタンスを作成
emulator = Emulator()
controller = CustomController()

# サンプルトポロジを作成
topology = create_mesh_topology()

# トポロジ内のノードをエミュレータに追加
for node in topology['nodes']:
    emulator.add_node(node)

# コントローラをスイッチに追加
for node in emulator.nodes:
    if isinstance(node, Switch):
        controller.add_switch(node)

# シミュレーションモニタリングを初期化
simulation_monitor = SimulationMonitor(emulator, interval=2)  # シミュレーションモニタリングを2秒間隔で設定
logger = EventLogger()  # イベントロガーを初期化
visualizer = NetworkVisualizer(network=topology)  # ネットワークビジュアライザを初期化

# トラフィックフローを管理する FlowManager を初期化
flow_manager = FlowManager()

# 統計データを収集する StatsCollector を初期化
stats_collector = StatsCollector(emulator)
stats_collector.start()  # 統計データの収集を開始

# トラフィックフローを追加（Host1 -> Host2）
host1 = emulator.get_node_by_name("Host1")
host2_ip = "10.0.0.2"
if host1:
    flow1 = flow_manager.add_flow(host1, host2_ip, interval=1.0, payload="Hello from Host1")

# シミュレーションモニタリングを別スレッドで開始
import threading
monitor_thread = threading.Thread(target=simulation_monitor.start)
monitor_thread.start()

# シミュレーションを実行（5秒間）
emulator.run_simulation(duration=5)

# シミュレーションモニタリングを停止
simulation_monitor.stop()
monitor_thread.join()  # モニタリングスレッドの終了を待つ

# 統計データを表示
stats_collector.print_stats()

# 統計データを CSV ファイルに保存
stats_collector.save_to_csv(folder_path="results", file_prefix="network_stats")

# ネットワークの視覚化を表示
visualizer.visualize_network()

# 統計データの収集を停止
stats_collector.stop()

# ログイベントの記録
logger.log_event("シミュレーションが完了しました。")

# トラフィックフローを削除
flow_manager.clear_all_flows()