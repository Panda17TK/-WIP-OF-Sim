
from core.emulator import Emulator
from controller.custom_controller import CustomController
from topology.example_topology import create_example_topology, create_mesh_topology, create_ring_topology
from traffic.flow_manager import FlowManager
from traffic.stats_collector import StatsCollector
from components.switch import Switch

# エミュレータとカスタムコントローラのインスタンスを作成
emulator = Emulator()
controller = CustomController()

# サンプルトポロジを作成（例: メッシュトポロジ）
topology = create_mesh_topology()  # メッシュトポロジを使用
# topology = create_example_topology()  # シンプルトポロジを使用
# topology = create_ring_topology()  # リングトポロジを使用

# トポロジ内のノードをエミュレータに追加
for node in topology['nodes']:
    emulator.add_node(node)

# コントローラをスイッチに追加
for node in emulator.nodes:
    if isinstance(node, Switch):
        controller.add_switch(node)

# トラフィックフローを管理する FlowManager を初期化
flow_manager = FlowManager()

# 統計データを収集する StatsCollector を初期化
stats_collector = StatsCollector(emulator)
stats_collector.start()  # 統計データの収集を開始

# トラフィックフローを追加（Host1 -> Host2）
host1 = emulator.get_node_by_name("Host1")  # ノード名で取得
host2_ip = "10.0.0.2"
if host1:
    flow1 = flow_manager.add_flow(host1, host2_ip, interval=1.0, payload="Hello from Host1")

# シミュレーションを実行（5秒間）
emulator.run_simulation(duration=5)

# 統計データを表示
stats_collector.print_stats()

# 統計データを CSV ファイルに保存（結果保存用フォルダにタイムスタンプ付きファイル名で）
stats_collector.save_to_csv(folder_path="results", file_prefix="network_stats")

# 統計データの収集を停止
stats_collector.stop()

# トラフィックフローを削除
flow_manager.clear_all_flows()