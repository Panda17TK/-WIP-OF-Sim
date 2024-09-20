from core.emulator import Emulator
from core.packet import Packet
from components.host import Host
from components.switch import Switch
from components.link import Link
from controller.custom_controller import CustomController

# エミュレータとカスタムコントローラのインスタンスを作成
emulator = Emulator()
controller = CustomController()

# ホストとスイッチを作成
host1 = Host("Host1", ip_address="10.0.0.1", mac_address="AA:BB:CC:DD:EE:01")
host2 = Host("Host2", ip_address="10.0.0.2", mac_address="AA:BB:CC:DD:EE:02")
switch = Switch("Switch1")

# ノードをエミュレータに追加
emulator.add_node(host1)
emulator.add_node(host2)
emulator.add_node(switch)

# リンクを作成して接続
link1 = Link(host1, switch, bandwidth=100, delay=5, packet_loss_rate=0.0)
link2 = Link(host2, switch, bandwidth=100, delay=5, packet_loss_rate=0.0)
host1.add_link(link1)
switch.add_link(link1)
switch.add_link(link2)
host2.add_link(link2)

# スイッチをコントローラに追加
controller.add_switch(switch)

# パケット生成と送信
host1.generate_packet("10.0.0.2", "Hello from Host1")
host2.generate_packet("10.0.0.1", "Hello from Host2")

# シミュレーションの実行（イベントを処理）
emulator.run_simulation(duration=2)