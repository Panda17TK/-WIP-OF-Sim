import matplotlib.pyplot as plt
import networkx as nx

class NetworkVisualizer:
    """
    ネットワークの状態やパフォーマンスを視覚的に表示するクラス。
    各ノードやリンクの状態をグラフや図として表示します。
    """

    def __init__(self, network):
        """
        NetworkVisualizer の初期化。

        Args:
            network (dict): ネットワークのノードとリンク情報を持つ辞書（例: {'nodes': [], 'links': []}）。
        """
        self.network = network  # ネットワーク情報を保持
        self.graph = nx.Graph()  # NetworkX のグラフオブジェクトを作成
        self._initialize_graph()  # ネットワーク構造をグラフに反映

    def _initialize_graph(self):
        """
        ネットワーク情報に基づいてグラフを初期化します。
        """
        # ノードをグラフに追加
        for node in self.network['nodes']:
            # Node オブジェクトの場合は node.name を追加
            if hasattr(node, 'name'):
                self.graph.add_node(node.name)
            else:
                # 文字列の場合はそのまま追加
                self.graph.add_node(node)

        # リンクをグラフに追加
        for link in self.network['links']:
            # Link オブジェクトの場合は、接続しているノードの名前を取得
            if hasattr(link, 'node1') and hasattr(link, 'node2'):
                self.graph.add_edge(link.node1.name, link.node2.name)
            else:
                # ノード名のタプルの場合
                self.graph.add_edge(link[0], link[1])

    def visualize_network(self):
        """
        ネットワークの状態を視覚的に表示します。
        """
        pos = nx.spring_layout(self.graph)  # ノードの配置を設定
        plt.figure(figsize=(10, 8))  # 図のサイズを設定
        # ノードとリンクをグラフに描画
        nx.draw(self.graph, pos, with_labels=True, node_color='skyblue', node_size=3000, font_size=12, font_weight='bold')
        plt.title("Network Visualization")  # グラフのタイトルを設定
        plt.show()  # グラフを表示