<h2>配送管理システム (Delivery Management System)</h2>
Python (Flask) と PostgreSQL を使用した、シンプルで使いやすい配送状況管理アプリケーションです。</p>

<h3>主な機能</h3>
荷物登録: 荷物名、配達先住所、配達期日を指定して新規登録。<br>
ステータス管理: 「待機中」「運搬中」「完了」の3段階をワンクリックで更新。<br> 
一括操作: 複数の荷物を選んで一括で「完了」ステータスに変更。<br>
高度な検索: pykakasi を利用し、漢字・ひらがな・カタカナ・ローマ字のどれでもヒットする日本語検索機能。<br>
期限切れ警告: 配達期日が今日を過ぎている未完了の荷物を赤字で強調表示。<br>
レスポンシブデザイン: <code>water.css</code> を採用した、シンプルで清潔感のあるUI。

<h3>使用技術</h3>
Backend: Python 3.x Flask<br>
Database: Postgre<br>
Libraries: psycopg2, pykakasi (Database Driver)<br>
Frontend: HTML5 / Jinja2 / water.css<br>

<h3>セットアップ手順</h3>
1. データベースの準備PostgreSQLで <code>delivery_db</code> という名前のデータベースを作成してください。（接続設定は <code>db.py</code> 内のパラメータを適宜変更してください）<br>
2. ライブラリのインストール <code>pip install flask psycopg2 pykakasi</code> <br>
3. テーブルの作成・初期化初回実行時、またはデータベース構造を変更した際は、<code>python main.py</code>を実行してテーブルを生成します。<br>
注意: この操作により既存のデータは一度リセットされます。<br>
3. <code>main.py </code>起動後、ブラウザで[http://127.0.0.1:5000] にアクセスしてください。<br>

<h3>ファイル構成</h3>
<code>main.py</code>: Flaskのルート定義、ビジネスロジック。<br>
<code>db.py</code>: データベース接続設定、テーブル作成スクリプト。<br>
<code>templates/index.html</code>: 配送リスト一覧、検索、ステータス変更画面。<br>
<code>add.html</code>: 新規荷物登録画面。<br>

<h3>データベース設計</h3>
本システムは2つのテーブルを紐付けて管理しています。</p>
1. statuses (マスタテーブル)</p>
ステータスの種類と表示名を定義します。<br>
<code>status_code</code>: 'pending', 'shipping', 'done' (PK)<br>
<code>display_name</code>: '待機中', '運搬中', '完了'</p>
2. deliveries (トランザクションテーブル)</p>
具体的な配送データを保持します。<br>
<code>id</code>: シリアル番号 (PK)<br>
<code>item_name</code>: 荷物名<br>
<code>addres</code>s: 配達先住所<br>
<code>deadline</code>: 配達期日 (DATE)<br>
<code>search_info</code>【重要】 検索効率化のための正規化テキスト（後述）
<code>status</code>: 現在のステータス (FK: statuses.status_code)






























