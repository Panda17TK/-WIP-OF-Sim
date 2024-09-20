from topology.topology_builder import TopologyBuilder

def create_example_topology():
    """
    サンプルのネットワークトポロジを構築し、定義します。

    トポロジ:
    - ホスト1 (10.0.0.1)
    - ホスト2 (10.0.0.2)
    - スイッチ (Switch1)
    - ホスト1 <-> スイッチ
    - ホスト2 <-> スイッチ
    """
    builder = TopologyBuilder()

    # ホストを追加
    host1 = builder.add_host("Host1", "10.0.0.1", "AA:BB:CC:DD:EE:01")
    host2 = builder.add_host("Host2", "10.0.0.2", "AA:BB:CC:DD:EE:02")

    # スイッチを追加
    switch = builder.add_switch("Switch1")

    # リンクを追加
    builder.add_link(host1, switch, bandwidth=100, delay=5, packet_loss_rate=0.0)
    builder.add_link(host2, switch, bandwidth=100, delay=5, packet_loss_rate=0.0)

    # トポロジを構築
    topology = builder.build()
    return topology

def create_mesh_topology():
    """
    メッシュ構造のネットワークトポロジを構築します。

    トポロジ:
    - ホスト1, ホスト2, ホスト3 (10.0.0.1, 10.0.0.2, 10.0.0.3)
    - スイッチ1, スイッチ2, スイッチ3
    - 各ホストはそれぞれのスイッチに接続
    - スイッチ間は相互に接続 (メッシュ構造)
    """
    builder = TopologyBuilder()

    # ホストを追加
    host1 = builder.add_host("Host1", "10.0.0.1", "AA:BB:CC:DD:EE:01")
    host2 = builder.add_host("Host2", "10.0.0.2", "AA:BB:CC:DD:EE:02")
    host3 = builder.add_host("Host3", "10.0.0.3", "AA:BB:CC:DD:EE:03")

    # スイッチを追加
    switch1 = builder.add_switch("Switch1")
    switch2 = builder.add_switch("Switch2")
    switch3 = builder.add_switch("Switch3")

    # ホストとスイッチをリンクで接続
    builder.add_link(host1, switch1, bandwidth=100, delay=5, packet_loss_rate=0.0)
    builder.add_link(host2, switch2, bandwidth=100, delay=5, packet_loss_rate=0.0)
    builder.add_link(host3, switch3, bandwidth=100, delay=5, packet_loss_rate=0.0)

    # スイッチ間をリンクで接続（メッシュ構造）
    builder.add_link(switch1, switch2, bandwidth=1000, delay=5, packet_loss_rate=0.0)
    builder.add_link(switch2, switch3, bandwidth=1000, delay=5, packet_loss_rate=0.0)
    builder.add_link(switch3, switch1, bandwidth=1000, delay=5, packet_loss_rate=0.0)

    # トポロジを構築
    topology = builder.build()
    return topology

def create_ring_topology():
    """
    リング構造のネットワークトポロジを構築します。

    トポロジ:
    - ホスト1, ホスト2, ホスト3 (10.0.0.1, 10.0.0.2, 10.0.0.3)
    - スイッチ1, スイッチ2, スイッチ3
    - 各ホストはそれぞれのスイッチに接続
    - スイッチ間はリング状に接続 (Switch1 -> Switch2 -> Switch3 -> Switch1)
    """
    builder = TopologyBuilder()

    # ホストを追加
    host1 = builder.add_host("Host1", "10.0.0.1", "AA:BB:CC:DD:EE:01")
    host2 = builder.add_host("Host2", "10.0.0.2", "AA:BB:CC:DD:EE:02")
    host3 = builder.add_host("Host3", "10.0.0.3", "AA:BB:CC:DD:EE:03")

    # スイッチを追加
    switch1 = builder.add_switch("Switch1")
    switch2 = builder.add_switch("Switch2")
    switch3 = builder.add_switch("Switch3")

    # ホストとスイッチをリンクで接続
    builder.add_link(host1, switch1, bandwidth=100, delay=5, packet_loss_rate=0.0)
    builder.add_link(host2, switch2, bandwidth=100, delay=5, packet_loss_rate=0.0)
    builder.add_link(host3, switch3, bandwidth=100, delay=5, packet_loss_rate=0.0)

    # スイッチ間をリング状にリンクで接続
    builder.add_link(switch1, switch2, bandwidth=1000, delay=5, packet_loss_rate=0.0)
    builder.add_link(switch2, switch3, bandwidth=1000, delay=5, packet_loss_rate=0.0)
    builder.add_link(switch3, switch1, bandwidth=1000, delay=5, packet_loss_rate=0.0)

    # トポロジを構築
    topology = builder.build()
    return topology