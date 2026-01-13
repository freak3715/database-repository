from flask import Flask, render_template, request, redirect
from db import get_connection, create_table

app = Flask(__name__)

create_table()

@app.route('/')
def index():
    with get_connection() as conn:
        with conn.cursor() as cur:
            cur.execute("SELECT * FROM deliveries;")
            data = cur.fetchall()
    return render_template('index.html', deliveries=data)

@app.route('/add', methods=['POST'])
def add():
    item_name = request.form.get('item_name')
    # �f�[�^��}��
    with get_connection() as conn:
        with conn.cursor() as cur:
            cur.execute("INSERT INTO deliveries (item_name) VALUES (%s)", (item_name,))
            conn.commit()
    return redirect('/')

@app.route('/delete/<int:id>', methods=['POST'])
def delete(id):
    # データベースから指定されたIDのデータを削除
    with get_connection() as conn:
        with conn.cursor() as cur:
            cur.execute("DELETE FROM deliveries WHERE id = %s", (id,))
            conn.commit()
    return redirect('/')

@app.route('/update/<int:id>', methods=['POST'])
def update(id):
    with get_connection() as conn:
        with conn.cursor() as cur:
            # 指定されたIDのstatusを 'done' に更新
            cur.execute("UPDATE deliveries SET status = 'done' WHERE id = %s", (id,))
            conn.commit()
    return redirect('/')

# --- main.py に追加 ---

@app.route('/add_page')
def add_page():
    # add.html を表示するだけ
    return render_template('add.html')

# 既存の @app.route('/add', methods=['POST']) はそのままでOK！
# 登録が終わった後に return redirect('/') で一覧に戻るようになっているためです。

if __name__ == '__main__':
    app.run(debug=True, port=5000)