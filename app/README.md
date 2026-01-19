**配送管理システム (Delivery Management System)**
Python (Flask) と PostgreSQL を使用した、シンプルで使いやすい配送状況管理アプリケーションです。</p>

**主な機能**
荷物登録: 荷物名、配達先住所、配達期日を指定して新規登録。ステータス管理: 「待機中」「運搬中」「完了」の3段階をワンクリックで更新。
一括操作: 複数の荷物を選んで一括で「完了」ステータスに変更。
検索・フィルタリング: 荷物名や住所での検索、およびステータス別の絞り込み。期限切れ警告: 配達期日が今日を過ぎている未完了の荷物を赤字で強調表示。
レスポンシブデザイン: water.css を採用した、シンプルで清潔感のあるUI。? 使用技術Backend: 
Python 3.x / FlaskDatabase: 
PostgreSQLLibrary: 
psycopg2 (Database Driver)Frontend: 
HTML5 / Jinja2 / water.css

**セットアップ手順**
1. データベースの準備PostgreSQLで delivery_db という名前のデータベースを作成してください。（接続設定は db.py 内のパラメータを適宜変更してください）

2. テーブルの作成・初期化初回実行時、またはデータベース構造を変更した際は、以下のコマンドを実行してテーブルを生成します。注意: この操作により既存のデータは一度リセットされます。Bashpython db.py

3. アプリケーションの起動Bashpython main.py
起動後、ブラウザで http://127.0.0.1:5000 にアクセスしてください。

**ファイル構成**
main.py: Flaskのルート定義、ビジネスロジック。
db.py: データベース接続設定、テーブル作成スクリプト。
templates/index.html: 配送リスト一覧、検索、ステータス変更画面。
add.html: 新規荷物登録画面。

** データベース設計 (ER図)**
本システムは2つのテーブルを紐付けて管理しています。
1. statuses (マスタテーブル)
ステータスの種類と表示名を定義します。
status_code: 'pending', 'shipping', 'done' (PK)
display_name: '待機中', '運搬中', '完了'

2. deliveries (トランザクションテーブル)
具体的な配送データを保持します。
id: シリアル番号 (PK)
item_name: 荷物名
address: 配達先住所
deadline: 配達期日 (DATE)

status: 現在のステータス (FK: statuses.status_code)

