from core.emulator import Emulator
from core.packet import Packet
from components.node import Node
from components.link import Link
from components.host import Host
from components.switch import Switch

# ノード（ホストとスイッチ）の作成
host1 = Host("Host1", ip_address="10.0.0.1", mac_address="AA:BB:CC:DD:EE:01")
host2 = Host("Host2", ip_address="10.0.0.2", mac_address="AA:BB:CC:DD:EE:02")
switch = Switch("Switch1")

# エミュレータのインスタンスを作成
emulator = Emulator()

# ノードをエミュレータに追加
emulator.add_node(host1)
emulator.add_node(host2)
emulator.add_node(switch)

# リンクの作成（ホストとスイッチを接続）
link1 = Link(host1, switch, bandwidth=100, delay=5, packet_loss_rate=0.0)
link2 = Link(host2, switch, bandwidth=100, delay=5, packet_loss_rate=0.0)

# リンクをノードに追加（物理的な接続を設定）
host1.add_link(link1)  # Host1 と Switch のリンクを設定
switch.add_link(link1)  # Switch と Host1 のリンクを設定
switch.add_link(link2)  # Switch と Host2 のリンクを設定
host2.add_link(link2)  # Host2 と Switch のリンクを設定

# スイッチのフローテーブルにエントリを設定
switch.install_flow(("10.0.0.1", "10.0.0.2"), {"out_port": 1})  # Host1 から Host2 へのフロー
switch.install_flow(("10.0.0.2", "10.0.0.1"), {"out_port": 0})  # Host2 から Host1 へのフロー

# ホストからパケットを生成して送信
host1.generate_packet("10.0.0.2", "Hello from Host1!")
host2.generate_packet("10.0.0.1", "Hello from Host2!")

# シミュレーションを短時間実行してイベントを処理
emulator.run_simulation(duration=2)