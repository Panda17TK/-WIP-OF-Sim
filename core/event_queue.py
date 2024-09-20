import heapq

class EventQueue:
    def __init__(self):
        # 優先度付きキューとしてイベントを格納するリスト
        self.queue = []

    def push(self, event):
        # ヒープにイベントを追加（優先度はevent.timeで決定）
        heapq.heappush(self.queue, event)

    def pop(self):
        # ヒープからイベントを取り出す（最も早い時間のイベント）
        return heapq.heappop(self.queue)

    def is_empty(self):
        # キューが空かどうかを確認する
        return len(self.queue) == 0