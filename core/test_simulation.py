from core.emulator import Emulator
from core.packet import Packet
from core.event_queue import EventQueue

# シンプルなイベントクラスの定義
class Event:
    def __init__(self, time, event_type, node, packet=None):
        self.time = time          # イベントが発生するシミュレーション時刻
        self.type = event_type    # イベントのタイプ（例: "PACKET_ARRIVAL"）
        self.node = node          # イベントが発生するノード
        self.packet = packet      # パケット（オプション）
    
    # イベントの優先順位（時刻）を比較するためのメソッド
    def __lt__(self, other):
        return self.time < other.time

# シンプルなノードクラスの定義
class Node:
    def __init__(self, name):
        self.name = name
        self.links = []

    def add_link(self, link):
        self.links.append(link)

# テスト用のノードとエミュレータの作成
node_a = Node("Node A")
node_b = Node("Node B")

# エミュレータのインスタンスを作成
emulator = Emulator()

# ノードをエミュレータに追加
emulator.add_node(node_a)
emulator.add_node(node_b)

# パケット到着イベントをスケジュール（時間 10 でノード A に到着）
event = Event(time=10, event_type="PACKET_ARRIVAL", node=node_a)
emulator.schedule_event(event)

# パケット到着イベントをスケジュール（時間 15 でノード B に到着）
event = Event(time=15, event_type="PACKET_ARRIVAL", node=node_b)
emulator.schedule_event(event)

# シミュレーションの実行（シミュレーション時間 20）
emulator.run_simulation(duration=20)