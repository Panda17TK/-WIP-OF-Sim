import unittest
import sys
import os

# プロジェクトのルートディレクトリをsys.pathに追加
project_root = os.path.abspath(os.path.dirname(__file__))
sys.path.insert(0, project_root)

# テストディレクトリを追加
sys.path.insert(0, os.path.join(project_root, 'tests'))
print("Current sys.path:", sys.path)  # デバッグ用出力

def run_all_tests():
    """
    すべてのユニットテストと統合テストを実行します。
    """
    loader = unittest.TestLoader()
    suite = unittest.TestSuite()

    # カレントディレクトリをプロジェクトのルートに設定
    os.chdir(project_root)

    # テストパスを相対パスに変更
    unit_tests_path = 'tests/unit'
    integration_tests_path = 'tests/integration'
    print("Unit Tests Path:", unit_tests_path)  # デバッグ用出力
    print("Integration Tests Path:", integration_tests_path)  # デバッグ用出力

    try:
        # テストディレクトリ内のすべてのテストをロード
        suite.addTests(loader.discover('unit', pattern='test_*.py', top_level_dir='tests'))
        suite.addTests(loader.discover('integration', pattern='test_*.py', top_level_dir='tests'))
    except Exception as e:
        print(f"エラー発生: テストのロード中に問題が発生しました - {e}")
        return

    runner = unittest.TextTestRunner(verbosity=2)
    result = runner.run(suite)

    if result.wasSuccessful():
        print("すべてのテストが成功しました！")
    else:
        print(f"失敗したテスト数: {len(result.failures)}")
        print(f"エラー数: {len(result.errors)}")

if __name__ == '__main__':
    run_all_tests()