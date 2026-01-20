from flask import Flask, render_template, request, redirect
from db import get_connection, create_table
from datetime import date # 1. 文頭のインポートに追加
from pykakasi import kakasi

app = Flask(__name__)

# 起動時にテーブル作成（db.pyを修正済みならここでもOK）
create_table()

@app.route('/')
def index():
    # 検索クエリとステータスフィルターの取得
    query = request.args.get('q', '')
    status_filter = request.args.get('status', '')
    
    with get_connection() as conn:
        with conn.cursor() as cur:
            # statuses テーブルを JOIN して表示名（display_name）を取得する
            # d.status (外部キー) と s.status_code を紐付け
            sql = """
                SELECT 
                    d.id, 
                    d.item_name, 
                    d.address, 
                    d.status, 
                    d.deadline, 
                    s.display_name 
                FROM deliveries d
                JOIN statuses s ON d.status = s.status_code
                WHERE 1=1
            """
            params = []
            
            # 検索機能（荷物名または住所）
            if query:
                # item_nameの代わりに search_info を検索対象にする
                sql += " AND (d.search_info ILIKE %s OR d.address ILIKE %s)"
                params.extend([f"%{query}%", f"%{query}%"])
            
            # ステータス絞り込み機能
            if status_filter:
                sql += " AND d.status = %s"
                params.append(status_filter)
            
            # ID順に並び替え
            sql += " ORDER BY d.id;"
            
            cur.execute(sql, tuple(params))
            data = cur.fetchall()
            
    # HTML側にデータを渡す
    # today=date.today() を渡すことで、HTML側で期日の比較が可能になる
    return render_template(
        'index.html', 
        deliveries=data, 
        query=query, 
        status_filter=status_filter, 
        today=date.today()
    )

app.route('/add', methods=['POST'])
def add():
    item_name = request.form.get('item_name')
    address = request.form.get('address')
    deadline = request.form.get('deadline')

    # ★ここで自動変換を実行
    search_info = generate_search_info(item_name)

    with get_connection() as conn:
        with conn.cursor() as cur:
            cur.execute(
                "INSERT INTO deliveries (item_name, address, deadline, search_info) VALUES (%s, %s, %s, %s)",
                (item_name, address, deadline, search_info)
            )
            conn.commit()
    return redirect('/')

@app.route('/update/<int:id>/<string:new_status>', methods=['POST'])
def update(id, new_status):
    # get_connection() で取得した conn を with で使うことで確実に close される
    with get_connection() as conn:
        with conn.cursor() as cur:
            # 実行
            cur.execute("UPDATE deliveries SET status = %s WHERE id = %s", (new_status, id))
            # 変更を確定させる
            conn.commit()
    return redirect('/')

@app.route('/delete/<int:id>', methods=['POST'])
def delete(id):
    with get_connection() as conn:
        with conn.cursor() as cur:
            cur.execute("DELETE FROM deliveries WHERE id = %s", (id,))
            conn.commit()
    return redirect('/')

@app.route('/add_page')
def add_page():
    return render_template('add.html')

@app.route('/bulk_update', methods=['POST'])
def bulk_update():
    # 1. チェックされたIDのリストを取得（この時点では文字列のリスト ['1', '2', ...]）
    selected_ids = request.form.getlist('item_ids')
    
    if not selected_ids:
        return redirect('/')

    # 2. 文字列のリストを数値（整数）のリストに変換する
    # これにより 'integer = text' のエラーを回避します
    try:
        int_ids = [int(id) for id in selected_ids]
    except ValueError:
        return redirect('/') # IDが数値として解釈できない場合

    try:
        with get_connection() as conn:
            with conn.cursor() as cur:
                # 3. 数値に変換したリストを使って一括更新
                cur.execute(
                    "UPDATE deliveries SET status = 'done' WHERE id = ANY(%s)",
                    (int_ids,)
                )
                conn.commit()
    except Exception as e:
        print(f"一括更新エラー: {e}")
        
    return redirect('/')

def generate_search_info(text):
    kks = kakasi()
    result = kks.convert(text)
    # ひらがな、カタカナ、ローマ字を抽出して1つの文字列にまとめる
    hira = "".join([item['hira'] for item in result])
    kana = "".join([item['kana'] for item in result])
    romaji = "".join([item['hepburn'] for item in result])
    
    # 検索で見つかりやすいようにスペース区切りで結合
    return f"{text} {hira} {kana} {romaji}"

@app.route('/add', methods=['POST'])
def add():
    item_name = request.form.get('item_name')
    address = request.form.get('address')
    deadline = request.form.get('deadline')

    # 検索用情報の生成
    search_info = generate_search_info(item_name)

    with get_connection() as conn:
        with conn.cursor() as cur:
            # search_infoも一緒に保存する
            cur.execute(
                "INSERT INTO deliveries (item_name, address, deadline, search_info) VALUES (%s, %s, %s, %s)",
                (item_name, address, deadline, search_info)
            )
            conn.commit()
    return redirect('/')
        

if __name__ == '__main__':
    app.run(debug=True, port=5000)