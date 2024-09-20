class Emulator:
	def __init__(self):
		self.nodes = {}
		self.links = []
		self.event_queue = EventQueue()
		self.current_time = 0

	def add_node(self, node):
		self.nodes[node.name] = node

	def add_link(self, link):
		self.links.append(link)
		link.node1.add_link(link)
		link.node2.add_link(link)

	def schedule_event(self, event):
		self.event_queue.push(event)

	def run_simulation(self, duration):
		end_time = self.current_time + duration
		while self.current_time < end_time and not self.event_queue.is_empty():
			event = self.event_queue.pop()
			self.current_time = event.time
			self.process_event(event)

	def process_event(self, event):
		if event.type == "PACKET_ARRIVAL":
			self.handle_packet_arrival(event)
		# 他のイベントタイプの処理を追加可能

	def handle_packet_arrival(self, event):
		# パケット到着イベントの処理
		pass