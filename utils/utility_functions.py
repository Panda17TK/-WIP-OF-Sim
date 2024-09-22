import json
import os
import csv
from datetime import datetime
from components.host import Host
from components.switch import Switch
from components.link import Link
from controller.custom_controller import CustomController

def load_config(file_path):
    """
    JSON設定ファイルを読み込み、辞書形式で返します。

    Args:
        file_path (str): JSONファイルのパス。

    Returns:
        dict: JSONファイルから読み込んだ設定データ。

    Raises:
        FileNotFoundError: ファイルが見つからない場合に発生。
        ValueError: JSONの読み込みに失敗した場合に発生。
    """
    if not os.path.exists(file_path):
        raise FileNotFoundError(f"設定ファイルが見つかりません: {file_path}")

    with open(file_path, 'r') as file:
        try:
            config = json.load(file)
            return config
        except json.JSONDecodeError as e:
            raise ValueError(f"設定ファイルの読み込みに失敗しました: {e}")

def get_node_by_name(nodes, name):
    """
    ノードのリストから、名前でノードオブジェクトを取得します。

    Args:
        nodes (list): ノードオブジェクトのリスト。
        name (str): ノードの名前。

    Returns:
        Node: 名前に一致するノードオブジェクト。見つからない場合は None。
    """
    for node in nodes:
        if node.name == name:
            return node
    return None

def build_network_from_config(emulator, config):
    """
    network_config.json の内容に基づいてネットワークを構築します。

    Args:
        emulator (Emulator): エミュレータインスタンス。
        config (dict): network_config.json から読み込んだ設定データ。

    Returns:
        None
    """
    nodes = []

    # ノードの生成
    for node_config in config['nodes']:
        if node_config['type'] == 'host':
            node = Host(
                name=node_config['name'],
                ip_address=node_config.get('ip_address'),
                mac_address=node_config.get('mac_address')
            )
        elif node_config['type'] == 'switch':
            node = Switch(name=node_config['name'])
        else:
            raise ValueError(f"未知のノードタイプ: {node_config['type']}")

        emulator.add_node(node)
        nodes.append(node)

    # リンクの生成
    for link_config in config['links']:
        node1 = get_node_by_name(nodes, link_config['node1'])
        node2 = get_node_by_name(nodes, link_config['node2'])
        if node1 is None or node2 is None:
            raise ValueError(f"リンクのノードが見つかりません: {link_config['node1']}, {link_config['node2']}")

        link = Link(
            node1=node1,
            node2=node2,
            bandwidth=link_config.get('bandwidth', 100),
            delay=link_config.get('delay', 10),
            packet_loss_rate=link_config.get('packet_loss_rate', 0.0)
        )
        node1.add_link(link)
        node2.add_link(link)

def initialize_controllers(emulator, config):
    """
    controller_config.json の内容に基づいてコントローラを初期化し、スイッチに設定します。

    Args:
        emulator (Emulator): エミュレータインスタンス。
        config (dict): controller_config.json から読み込んだ設定データ。

    Returns:
        list: 作成されたコントローラのリスト。
    """
    controllers = []

    for controller_data in config['controllers']:
        controller = CustomController()
        controller.set_ip(controller_data['ip_address'])
        controller.set_port(controller_data['port'])

        # ルールを各スイッチに設定
        for rule in controller_data['rules']:
            switch = get_node_by_name(emulator.nodes, rule.get('switch_name'))
            if switch:
                switch.install_flow(
                    (rule['src_ip'], rule['dst_ip']),
                    {'out_port': rule['out_port']}
                )

        # コントローラを各スイッチに設定
        for node in emulator.nodes:
            if isinstance(node, Switch):
                controller.add_switch(node)

        controllers.append(controller)

    return controllers

def save_results_to_csv(stats, folder_path, file_prefix):
    """
    統計データを指定されたフォルダに CSV ファイルとして保存します。

    Args:
        stats (dict): 統計データ（各ノードのパケット送受信量など）。
        folder_path (str): 結果を保存するフォルダのパス。
        file_prefix (str): ファイル名の接頭辞。

    Returns:
        str: 保存されたファイルのパス。
    """
    # フォルダが存在しない場合は作成
    if not os.path.exists(folder_path):
        os.makedirs(folder_path)

    # ファイル名にタイムスタンプを追加
    timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
    file_path = os.path.join(folder_path, f"{file_prefix}_{timestamp}.csv")

    # CSV ファイルにデータを保存
    with open(file_path, 'w', newline='') as file:
        writer = csv.writer(file)
        # ヘッダー行
        writer.writerow(['Node Name', 'Packets Sent', 'Packets Received', 'Bytes Sent', 'Bytes Received'])
        # 統計データの書き込み
        for node_name, data in stats.items():
            writer.writerow([
                node_name,
                data['packets_sent'],
                data['packets_received'],
                data['bytes_sent'],
                data['bytes_received']
            ])

    print(f"結果をファイルに保存しました: {file_path}")
    return file_path