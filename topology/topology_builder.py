from components.host import Host
from components.switch import Switch
from components.link import Link

class TopologyBuilder:
    """
    ネットワークトポロジを構築するためのクラス。
    ホストやスイッチなどのノードを追加し、それらをリンクで接続することでトポロジを定義します。
    """

    def __init__(self):
        """
        TopologyBuilder の初期化。ノードとリンクのリストを初期化します。
        """
        self.nodes = []  # トポロジに含まれる全ノードのリスト
        self.links = []  # トポロジに含まれる全リンクのリスト

    def add_host(self, name, ip_address, mac_address):
        """
        ホストをトポロジに追加します。

        Args:
            name (str): ホストの名前。
            ip_address (str): ホストのIPアドレス。
            mac_address (str): ホストのMACアドレス。

        Returns:
            Host: 追加されたホストオブジェクト。
        """
        host = Host(name, ip_address, mac_address)
        self.nodes.append(host)
        return host

    def add_switch(self, name):
        """
        スイッチをトポロジに追加します。

        Args:
            name (str): スイッチの名前。

        Returns:
            Switch: 追加されたスイッチオブジェクト。
        """
        switch = Switch(name)
        self.nodes.append(switch)
        return switch

    def add_link(self, node1, node2, bandwidth=100, delay=10, packet_loss_rate=0.0):
        """
        ノード間にリンクを追加し、リンクの特性を設定します。

        Args:
            node1 (Node): リンクで接続される最初のノード。
            node2 (Node): リンクで接続される2番目のノード。
            bandwidth (int): リンクの帯域幅（Mbps）。
            delay (int): リンクの遅延（ミリ秒）。
            packet_loss_rate (float): パケット損失率（0.0〜1.0）。

        Returns:
            Link: 追加されたリンクオブジェクト。
        """
        link = Link(node1, node2, bandwidth, delay, packet_loss_rate)
        node1.add_link(link)
        node2.add_link(link)
        self.links.append(link)
        return link

    def build(self):
        """
        トポロジを構築し、ノードとリンクの情報を出力します。

        Returns:
            dict: トポロジのノードオブジェクトとリンク情報を持つ辞書。
        """
        # ノードオブジェクトとリンク情報を持つ辞書を返す
        topology_info = {
            "nodes": self.nodes,  # ノードオブジェクトを返す
            "links": self.links
        }
        print(f"トポロジを構築しました: {{'nodes': {[node.name for node in self.nodes]}, 'links': {[(link.node1.name, link.node2.name) for link in self.links]}}}")
        return topology_info