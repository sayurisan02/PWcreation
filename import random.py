import sqlite3
import random
import csv
import os
from datetime import datetime

# CSVファイルの保存先をスクリプトの場所に設定
script_dir = os.path.dirname(os.path.abspath(__file__))  # スクリプトのディレクトリ
csv_path = os.path.join(script_dir, "passwords.csv")
print("CSVファイルはここに保存されます:", csv_path)

# SQLite データベースの保存先
db_path = os.path.join(script_dir, "passwords.db")
print("SQLite データベースはここに保存されます:", db_path)


# パスワード生成関数
def generate_password(length=12):
    # """ランダムなパスワードを生成"""
    characters = 'abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ0123456789-_.'  # 使用する文字
    password = ''.join(random.choice(characters) for _ in range(length))
    return password

# パスワード保存関数
def save_to_csv(service_name, password, file_path):
    
    # 現在の時刻を取得
    timestamp = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
    
    # CSVファイルが存在するか確認
    file_exists = os.path.isfile(file_path)

    # CSVファイルを開いて追記モードで書き込み
    with open(file_path, mode="a", newline="", encoding="shift-jis") as file:
        writer = csv.writer(file)
        # ファイルが新規の場合、ヘッダー行を追加
        if not file_exists:
            writer.writerow(["サービス名", "パスワード", "時刻"])  # ヘッダー行
        writer.writerow([service_name, password, timestamp])  # データを追加
    print(f"パスワードが {file_path} に保存されました！")
    
    # SQLiteデータベースに保存する関数
def save_to_db(service_name, password, timestamp, db_path):
    # SQLiteデータベースに接続
    conn = sqlite3.connect(db_path)
    cursor = conn.cursor()

    # テーブルが存在しない場合は作成
    cursor.execute('''
    CREATE TABLE IF NOT EXISTS passwords (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        service_name TEXT,
        password TEXT,
        generated_at TEXT
    )''')
    
        # パスワードと生成時刻をデータベースに挿入
    cursor.execute('''
    INSERT INTO passwords (service_name, password, generated_at)
    VALUES (?, ?, ?)
    ''', (service_name, password, timestamp))

    # 変更を保存して接続を閉じる
    conn.commit()
    conn.close()
    print(f"パスワードがデータベース {db_path} に保存されました！")

# メイン処理
if __name__ == "__main__":
    service_name = input("サービス名を入力してください: ")
    password = generate_password(12)
    print(f"生成されたパスワード: {password}")
 
     # 現在の時刻を取得
    timestamp = datetime.now().strftime('%Y-%m-%d %H:%M:%S')

    # CSVにも保存
    save_to_csv(service_name, password, csv_path)

    # SQLiteにも保存
    save_to_db(service_name, password, timestamp, db_path)