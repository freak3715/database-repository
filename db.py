import psycopg2

def get_connection():
    try:
        # psycopg2.connect を使用
        conn = psycopg2.connect(
            host="localhost",  
            port=15432,
            dbname="delivery_db", # 修正: 前のメッセージでエラーが出ていた箇所の名前を合わせています
            user="postgres",
            password="password"
        )
        print("接続成功！")
        return conn
    except Exception as e:
        print(f"接続エラーが発生しました: {e}")
        return None

def create_table():
    conn = None
    try:
        # 1. データベースに接続
        conn = psycopg2.connect(
            host="localhost",
            port=15432,
            dbname="delivery_db",
            user="postgres",
            password="password"
        )
        
        # 2. カーソルを作成（SQLを実行するための窓口）
        cur = conn.cursor()
        
        # 3. テーブル作成のSQLを実行
        # db.py の create_table 関数内を修正
        cur.execute("DROP TABLE IF EXISTS deliveries;")
        
        create_query = """
        CREATE TABLE IF NOT EXISTS deliveries (
            id SERIAL PRIMARY KEY,
            item_name VARCHAR(100) NOT NULL,
            address VARCHAR(255),
            status VARCHAR(20) DEFAULT 'pending' CHECK (status IN ('pending', 'shipping', 'done')),
            deadline DATE,
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
        );
        """
        cur.execute(create_query)
        
        # 4. 変更を確定させる（これを行わないと反映されません）
        conn.commit()
        print("テーブルの作成に成功しました！")
        
        # カーソルを閉じる
        cur.close()

    except Exception as e:
        print(f"エラーが発生しました: {e}")
        if conn:
            conn.rollback() # エラー時はロールバックして安全に戻す
    finally:
        # 5. 接続を閉じる
        if conn:
            conn.close()

def insert_data(item_name):
    with get_connection() as conn:
        with conn.cursor() as cur:
            cur.execute("INSERT INTO deliveries (item_name) VALUES (%s)", (item_name,))
            conn.commit()
            print(f"データ登録完了: {item_name}")

if __name__ == "__main__":
    create_table()
    conn = get_connection()