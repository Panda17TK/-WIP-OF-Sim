from traffic.traffic_generator import TrafficGenerator

class FlowManager:
    """
    トラフィックフローを管理するクラス。
    各フローを生成・削除し、トラフィックの動的な管理を行います。
    """

    def __init__(self):
        """
        FlowManager の初期化。全フローを管理するリストを初期化します。
        """
        self.flows = []  # 管理中のトラフィックフローのリスト

    def add_flow(self, source, destination, interval=1.0, payload="Test Packet"):
        """
        新しいトラフィックフローを追加し、生成を開始します。

        Args:
            source (Host): フローの送信元となるホスト。
            destination (str): フローの宛先となるIPアドレス。
            interval (float): パケットを生成する間隔（秒）。
            payload (str): 送信するパケットのペイロード。

        Returns:
            TrafficGenerator: 生成されたトラフィックジェネレーターオブジェクト。
        """
        traffic_generator = TrafficGenerator(source, destination, interval, payload)
        self.flows.append(traffic_generator)
        traffic_generator.start()  # フローを開始
        print(f"新しいフローを追加しました: {source.name} -> {destination}, インターバル: {interval}秒")
        return traffic_generator

    def remove_flow(self, traffic_generator):
        """
        指定されたトラフィックフローを削除し、生成を停止します。

        Args:
            traffic_generator (TrafficGenerator): 削除するトラフィックジェネレーター。
        """
        if traffic_generator in self.flows:
            traffic_generator.stop()
            self.flows.remove(traffic_generator)
            print(f"フローを削除しました: {traffic_generator.source.name} -> {traffic_generator.destination}")

    def clear_all_flows(self):
        """
        全てのトラフィックフローを削除し、生成を停止します。
        """
        for flow in self.flows:
            flow.stop()
        self.flows.clear()
        print("全てのトラフィックフローを削除しました。")