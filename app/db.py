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
        
        create_query = """
        -- 1. ステータス定義テーブル
        CREATE TABLE IF NOT EXISTS statuses (
            id SERIAL PRIMARY KEY,
            status_code VARCHAR(20) UNIQUE NOT NULL, -- 'pending', 'shipping' など
            display_name VARCHAR(50) NOT NULL       -- '待機中', '運搬中' など
        );

        -- 2. メインの配送テーブル
        CREATE TABLE IF NOT EXISTS deliveries (
            id SERIAL PRIMARY KEY,
            item_name VARCHAR(100) NOT NULL,
            address VARCHAR(255),
            deadline DATE,
            -- statusを外部キーに変更 (statusesテーブルのstatus_codeを参照)
            status VARCHAR(20) DEFAULT 'pending' REFERENCES statuses(status_code),
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
        );

        -- 3. 初期データの投入 (既存になければ追加)
        INSERT INTO statuses (status_code, display_name) VALUES 
        ('pending', '待機中'),
        ('shipping', '運搬中'),
        ('done', '完了')
        ON CONFLICT (status_code) DO NOTHING;
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