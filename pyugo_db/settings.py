import os

# クローリング結果のテーブルデータを保存するDBのURI
PYUGO_DB_CRAWLING_DB_URI = os.environ.get('PYUGO_DB_CRAWLING_DB_URI', 'sqlite:///crawling.sqlite3')
# サイト運営者に迷惑をかけないための連続クローリング禁止秒数
PYUGO_DB_CRAWLING_WAIT_SECONDS = float(os.environ.get('PYUGO_DB_CRAWLING_WAIT_SECONDS', '3'))
# カードリスト取得用サイトのURL
PYUGO_DB_LIST_CRAWLING_ROOT_URL = \
    os.environ.get('PYUGO_DB_LIST_CRAWLING_ROOT_URL', 'https://ocg-card.com/')
