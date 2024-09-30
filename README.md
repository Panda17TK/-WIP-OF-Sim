
# ネットワークエミュレータ

このプロジェクトは、OpenFlowベースのネットワークエミュレータをPythonで実装したものです。パケットの転送、コントローラの設定、ネットワークのシミュレーションを行い、ネットワークの動作を詳細に分析することを目指します。

## 目次

- [ネットワークエミュレータ](#ネットワークエミュレータ)
	- [目次](#目次)
	- [インストール](#インストール)
	- [使用方法](#使用方法)
		- [1. 設定ファイルの作成](#1-設定ファイルの作成)
			- [network\_config.json](#network_configjson)
			- [controller\_config.json](#controller_configjson)
		- [2. エミュレータの起動](#2-エミュレータの起動)
		- [3. シミュレーションの実行](#3-シミュレーションの実行)
		- [4. 結果の保存と可視化](#4-結果の保存と可視化)
	- [テストの実行](#テストの実行)
	- [ディレクトリ構成](#ディレクトリ構成)
	- [貢献](#貢献)

## インストール

このプロジェクトをローカルにクローンし、必要なパッケージをインストールしてください。

```bash
# プロジェクトをクローン
git clone https://github.com/Panda17TK/OF-SIM.git
cd OF-SIM

# 仮想環境の作成
python -m venv venv
source venv/bin/activate  # Windowsの場合: venv\Scripts\activate

# 必要なパッケージをインストール
pip install -r requirements.txt
```

## 使用方法

### 1. 設定ファイルの作成

シミュレーションを行う前に、`config` フォルダ内にネットワークとコントローラの設定ファイルを作成します。

#### network_config.json

ネットワークのノードとリンクを定義します。

```json
{
  "nodes": [
    {"name": "Host1", "type": "host", "ip_address": "10.0.0.1", "mac_address": "00:00:00:00:00:01"},
    {"name": "Host2", "type": "host", "ip_address": "10.0.0.2", "mac_address": "00:00:00:00:00:02"},
    {"name": "Switch1", "type": "switch"}
  ],
  "links": [
    {"node1": "Host1", "node2": "Switch1", "bandwidth": 100, "delay": 10},
    {"node1": "Host2", "node2": "Switch1", "bandwidth": 100, "delay": 10}
  ]
}
```

#### controller_config.json

コントローラの設定を行います。各スイッチに対して、どのようなルールを適用するかを定義します。

```json
{
  "controllers": [
    {
      "ip_address": "127.0.0.1",
      "port": 6633,
      "rules": [
        {"switch_name": "Switch1", "src_ip": "10.0.0.1", "dst_ip": "10.0.0.2", "out_port": 1}
      ]
    }
  ]
}
```

### 2. エミュレータの起動

設定ファイルをもとにエミュレータを起動します。

```bash
python run_emulator.py
```

`run_emulator.py` は、エミュレータをセットアップし、ネットワークトポロジを構築し、シミュレーションを実行するスクリプトです。基本的な使用方法は以下の通りです。

```python
from core.emulator import Emulator
from utils.utility_functions import load_config, build_network_from_config, initialize_controllers

# エミュレータの初期化
emulator = Emulator()

# 設定ファイルの読み込み
network_config = load_config('config/network_config.json')
controller_config = load_config('config/controller_config.json')

# ネットワークの構築
build_network_from_config(emulator, network_config)

# コントローラの初期化
initialize_controllers(emulator, controller_config)

# シミュレーションの実行
emulator.run_simulation(10)  # 10秒間シミュレーションを実行
```

### 3. シミュレーションの実行

`run_simulation.py` などのスクリプトを使用して、シミュレーションを実行できます。

```bash
python run_simulation.py
```

シミュレーションの設定やシナリオは、`config` フォルダ内の設定ファイルでカスタマイズできます。

### 4. 結果の保存と可視化

シミュレーションの結果は `results` フォルダにCSVファイルとして保存されます。保存されたデータを分析し、可視化出来るようになる予定です。

```bash
# 結果を可視化するには
python visualize_results.py
```

このスクリプトは、`matplotlib` や `networkx` を使用して、ネットワークトポロジの可視化や、パケット転送状況を表示します。

## テストの実行

単体テストと統合テストを実行して、各モジュールが正しく動作するかを確認します。

```bash
# 単体テストの実行
python -m unittest discover tests/unit

# 統合テストの実行
python -m unittest discover tests/integration

# すべてのテストを実行（test_runner.pyを使用）
python test_runner.py
```

## ディレクトリ構成

プロジェクトのディレクトリ構成は以下の通りです。

```
project_root/
├── components/          # 各ネットワークコンポーネント（Host, Switch, Link）
│   ├── __init__.py
│   ├── host.py
│   ├── switch.py
│   └── link.py
├── controller/          # コントローラ（OpenFlowコントローラの実装）
│   ├── __init__.py
│   └── custom_controller.py
├── core/                # エミュレータのコア機能（イベントキュー、エミュレータ本体）
│   ├── __init__.py
│   ├── emulator.py
│   └── event_queue.py
├── tests/               # 単体テストと統合テスト
│   ├── __init__.py
│   ├── unit/
│   │   ├── __init__.py
│   │   └── test_host.py
│   ├── integration/
│   │   ├── __init__.py
│   │   └── test_network_simulation.py
├── config/              # 設定ファイル（ネットワークとコントローラ）
│   ├── network_config.json
│   └── controller_config.json
├── results/             # シミュレーション結果の保存先
│   └── (自動生成されるファイル)
├── run_emulator.py      # エミュレータを起動するメインスクリプト
├── run_simulation.py    # シミュレーションを実行するスクリプト
├── test_runner.py       # テストを一括で実行するスクリプト
└── README.md            # このファイル
```
