import logging
import os
from datetime import datetime

class EventLogger:
    """
    システムイベントやエラーをロギングするクラス。
    シミュレーション中のイベントを記録し、デバッグやトラブルシューティングに役立てます。
    """

    def __init__(self, log_dir="logs", log_level=logging.INFO):
        """
        EventLogger の初期化。

        Args:
            log_dir (str): ログファイルを保存するディレクトリ。デフォルトは "logs"。
            log_level (int): ログのレベル（例: logging.INFO, logging.DEBUG）。
        """
        self.log_dir = log_dir  # ログファイルの保存先ディレクトリ
        self.log_level = log_level  # ログのレベル（INFO、DEBUGなど）
        self.logger = logging.getLogger("EventLogger")  # ロガーのインスタンスを作成
        self.logger.setLevel(self.log_level)  # ログレベルを設定

        # ログフォルダが存在しない場合は作成
        if not os.path.exists(self.log_dir):
            os.makedirs(self.log_dir)

        # ログファイル名にタイムスタンプを追加
        log_filename = f"simulation_{datetime.now().strftime('%Y%m%d_%H%M%S')}.log"
        log_filepath = os.path.join(self.log_dir, log_filename)

        # ファイルハンドラとフォーマットを設定
        file_handler = logging.FileHandler(log_filepath)  # ファイルにログを保存するハンドラ
        formatter = logging.Formatter('%(asctime)s - %(levelname)s - %(message)s')  # ログのフォーマット
        file_handler.setFormatter(formatter)
        self.logger.addHandler(file_handler)  # ロガーにハンドラを追加

        # コンソールにもログを出力
        console_handler = logging.StreamHandler()  # コンソールに出力するハンドラ
        console_handler.setFormatter(formatter)
        self.logger.addHandler(console_handler)

    def log_event(self, message, level=logging.INFO):
        """
        イベントをロギングします。

        Args:
            message (str): ログに記録するメッセージ。
            level (int): ログレベル（例: logging.INFO, logging.DEBUG）。
        """
        self.logger.log(level, message)  # 指定されたレベルでメッセージをロギング

    def log_error(self, message):
        """
        エラーメッセージをロギングします。

        Args:
            message (str): ログに記録するエラーメッセージ。
        """
        self.logger.error(message)  # エラーレベルでメッセージをロギング