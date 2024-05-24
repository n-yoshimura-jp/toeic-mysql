# ライブラリをインポート
import pdfplumber
import re
from pprint import pprint
import requests
import mysql.connector
import os

# PDFファイル
pdf_file = "toeic_vocabulary.pdf"

# PDFファイルの読み込み
with pdfplumber.open(pdf_file) as pdf:
    # 全ページの取得
    pages = pdf.pages
    
    # 全ページのテキストを抽出
    all_text = ""
    for page in pages:
        all_text += page.extract_text()

# ページ数を確認
print("Number of pages:", len(pages))

# 全テキストを出力
print(all_text)

# 英単語を抽出する関数
def extract_words(text):
    words = re.findall(r"[a-zA-Z]+", text)
    return words

# テキストから英単語を抽出
words_list = extract_words(all_text)
# 重複を除いてユニークな値のみをリストに追加
words_list_unique_value = list(set(words_list))

# リストを確認
print(words_list_unique_value)

# 英単語と意味を格納するリスト
words_and_meanings = []

# 英単語と意味のタプルをリストに追加
for word in words_list_unique_value:
    # URL(APIのエンドポイント)
    url = f"https://api.dictionaryapi.dev/api/v2/entries/en/{word}"
    # データを取得
    response = requests.get(url)
    json_data = response.json()
    # 意味を取得しリストに追加
    meaning = json_data[0]["meanings"][0]["definitions"][0]["definition"]
    word_and_meaning_tuple = (word, meaning)
    words_and_meanings.append(word_and_meaning_tuple)

# リストを確認
pprint(words_and_meanings)

# ホスト
host = "localhost"

# ユーザー名 (環境変数から取得)
user = os.getenv("YOUR_USER_NAME")

# パスワード (環境変数から取得)
password = os.getenv("YOUR_PASSWORD")

# データベース名
db = "your_database_name"

# MySQLに接続
conn = mysql.connector.connect(
    host=host, 
    user=user, 
    password=password, 
    database=db
)

# カーソルを取得
cursor = conn.cursor()

# SQL(insert文)
base_sql = "INSERT INTO toeic (word, meaning) VALUES (%s, %s)"

# バリュー
values = words_and_meanings

# SQLを実行
cursor.executemany(base_sql, values)

# コミット
conn.commit()

# 追加されたレコード数を確認
print(cursor.rowcount, "record(s) inserted.")

# 接続をクローズ
cursor.close()
conn.close()