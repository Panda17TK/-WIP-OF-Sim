from core.emulator import Emulator
from controller.custom_controller import CustomController
from topology.example_topology import create_example_topology, create_mesh_topology, create_ring_topology
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
    emulator.add_node(node)  # ノードをエミュレータに追加

# コントローラをスイッチに追加
for node in emulator.nodes.values():  # 辞書の値としてのノードにアクセス
    if isinstance(node, Switch):
        controller.add_switch(node)

# メッシュトポロジの場合、ホスト間の通信をテスト
host1 = emulator.get_node_by_name("Host1")  # ノード名で取得
host2 = emulator.get_node_by_name("Host2")  # ノード名で取得

if host1 and host2:
    host1.generate_packet("10.0.0.2", "Hello from Host1")
    host2.generate_packet("10.0.0.1", "Hello from Host2")
else:
    print("ホストが見つかりません。トポロジの構築に失敗した可能性があります。")

# シミュレーションを実行
emulator.run_simulation(duration=2)