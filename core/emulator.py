from core.event_queue import EventQueue

class Emulator:
	def __init__(self):
		# ノード、リンク、イベントキュー、シミュレーション時刻の初期化
		self.nodes = {}
		self.links = []
		self.event_queue = EventQueue()
		self.current_time = 0

	def add_node(self, node):
		# ノードを追加（名前をキーとした辞書に格納）
		self.nodes[node.name] = node

	def add_link(self, link):
		# リンクを追加し、リンクの両端のノードにリンクを登録
		self.links.append(link)
		link.node1.add_link(link)
		link.node2.add_link(link)

	def schedule_event(self, event):
		# イベントをイベントキューに追加
		self.event_queue.push(event)

	def run_simulation(self, duration):
		# 指定されたシミュレーション期間の間、イベントを順次処理
		end_time = self.current_time + duration
		while self.current_time < end_time and not self.event_queue.is_empty():
			# 次のイベントを取得し、シミュレーション時刻を更新
			event = self.event_queue.pop()
			self.current_time = event.time
			self.process_event(event)

	def process_event(self, event):
		# イベントのタイプに応じた処理を実行
		if event.type == "PACKET_ARRIVAL":
			self.handle_packet_arrival(event)
		# 他のイベントタイプの処理を追加可能

	def handle_packet_arrival(self, event):
		# パケット到着イベントの処理（仮の処理）
		print(f"Packet arrived at {event.node.name} at time {event.time}")

	def get_node_by_name(self, name):
		"""
		ノードの名前を指定して取得します。

		Args:
			name (str): ノードの名前。

		Returns:
			Node: 指定された名前のノード、存在しない場合は None を返す。
		"""
		return self.nodes.get(name, None)