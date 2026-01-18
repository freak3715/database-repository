from flask import Flask, render_template, request, redirect
from db import get_connection, create_table
from datetime import date # 1. 文頭のインポートに追加

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
                sql += " AND (d.item_name ILIKE %s OR d.address ILIKE %s)"
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

@app.route('/add', methods=['POST'])
def add():
    item_name = request.form.get('item_name')
    address = request.form.get('address')
    deadline = request.form.get('deadline') # 追加
    with get_connection() as conn:
        with conn.cursor() as cur:
            # deadline も SQL に含める
            cur.execute(
                "INSERT INTO deliveries (item_name, address, deadline) VALUES (%s, %s, %s)", 
                (item_name, address, deadline)
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
    # チェックされたIDのリストを取得
    selected_ids = request.form.getlist('item_ids')
    
    if not selected_ids:
        return redirect('/')

    conn = get_connection()
    try:
        # トランザクション開始
        with conn:
            with conn.cursor() as cur:
                # SQLの IN 句を使って一括更新
                cur.execute(
                    "UPDATE deliveries SET status = 'done' WHERE id = ANY(%s)",
                    (selected_ids,)
                )
        # ブロックを抜けると自動で commit される
    except Exception as e:
        print(f"一括更新エラー: {e}")
    finally:
        conn.close()
        
    return redirect('/')

if __name__ == '__main__':
    app.run(debug=True, port=5000)