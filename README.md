# 住之江オッズ監視（検証用）

GitHub Actionsで5分間隔の取得を試みるプロトタイプです。**オッズ抽出・変動検出・通知は未実装**です。BOATERSのHTML取得と更新時刻の検証を行い、`data/latest.json` と `data/history.jsonl` に結果を記録します。サイト構造やアクセス制限により動作しない場合があります。

## iPhoneからの準備
1. GitHubで新規リポジトリを作る。
2. このZIP内の `monitor.py` と `.github/workflows/monitor.yml` を同じ構造でアップロードする。
3. リポジトリの Settings > Actions > General で必要に応じてワークフローの書き込み権限を許可する。
4. Actionsで `Suminoe odds monitor` の `Run workflow` を押して初回テストする。
5. `data/latest.json` の `status` を確認する。

**注意**: GitHubのcronは遅延・スキップがあり、正確な5分実行は保証されません。無料枠・サイト利用規約・レート制限を確認してください。GitHubリポジトリを公開する場合、取得結果も公開されます。過去オッズは初回実行より前にはさかのぼれません。
