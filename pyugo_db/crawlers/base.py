import time
from datetime import datetime

import requests
from bs4 import BeautifulSoup

from pyugo_db import crawler_logger
from pyugo_db.settings import PYUGO_DB_CRAWLING_WAIT_SECONDS

logger = crawler_logger


class YGOCrawlerBase(object):
    """
    各種データをクローリングするクラスの基本クラス。
    サイト運営者に迷惑がかからない速度でゆっくりクローリングするぞ！
    """
    _last_crawling_datetime: datetime
    _wait_seconds: float

    def __init__(self):
        self._last_crawling_datetime = datetime.now()
        self._wait_seconds = PYUGO_DB_CRAWLING_WAIT_SECONDS

    def _avoid_frequent_access(self):
        current_time = datetime.now()
        elapsed = (current_time - self._last_crawling_datetime).total_seconds()
        logger.debug(f'最終クローリングアクセスからの経過時間は{elapsed}秒です。')
        if elapsed < self._wait_seconds:
            logger.debug(f'クローリング対象サイトへのアクセスを一時停止しています。')
            time.sleep(self._wait_seconds - elapsed)
            logger.debug(f'クローリング対象サイトへのアクセスを再会します。')

    def get_html(self, url: str) -> BeautifulSoup:
        """
        requestsを使ってHTTPリクエストを送信し、レスポンスをBeautifulSoupでHTMLパースして返す。
        例外は特に処理せずそのまま発生させる。
        :param url: 対象URL
        :return: HTMLパース結果
        """
        logger.debug(f'{url}に対するクローリング処理を開始します。')
        # 連続アクセスをしないための待ち処理
        self._avoid_frequent_access()
        logger.debug(f'{url}にリクエストします。')
        response = requests.get(url)
        logger.debug(f'{url}からレスポンスを受け取りました。ステータスコードは{response.status_code}です。')
        logger.debug(f'レスポンスをパースします。')
        bs = BeautifulSoup(response.text, 'html.parser')
        logger.debug(f'{url}に対するクローリング処理を終了します。')
        return bs

    def post_html(self, url: str, body: str) -> BeautifulSoup:
        """
        requestsを使ってPOSTリクエストを送信し、レスポンスをBeautifulSoupでHTMLパースして返す。
        例外は特に処理せずそのまま発生させる。
        :param url: 対象URL
        :param body: URLエンコード状態の文字列
        :return: HTMLパース結果
        """
        logger.debug(f'{url}に対するPOSTによるクローリング処理を開始します。')
        # 連続アクセスをしないための待ち処理
        self._avoid_frequent_access()
        logger.debug(f'{url}にPOSTリクエストします。')
        response = requests.post(url, data=body)
        logger.debug(f'{url}からレスポンスを受け取りました。ステータスコードは{response.status_code}です。')
        logger.debug(f'レスポンスをパースします。')
        bs = BeautifulSoup(response.text, 'html.parser')
        logger.debug(f'{url}に対するクローリング処理を終了します。')
        return bs
