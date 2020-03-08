from typing import Set, List, Dict

from bs4 import Tag

from pyugo_db import crawler_logger
from pyugo_db.crawlers.base import YGOCrawlerBase
from pyugo_db.settings import PYUGO_DB_LIST_CRAWLING_ROOT_URL

logger = crawler_logger


class YGOCardListCrawler(YGOCrawlerBase):
    def __init__(self):
        super().__init__()
        self.root_url = PYUGO_DB_LIST_CRAWLING_ROOT_URL

    def get_pack_urls(self) -> Set[str]:
        crawler_logger.info('パック一覧の取得を開始')
        series_list_html = self.get_html(self.root_url + '/list')
        series_titles = series_list_html.find_all('dt', class_='list-series-title')
        pack_links = []
        for series_title in series_titles:
            packs_in_series = series_title.parent.find('dd').find_all('a')
            crawler_logger.debug(f'{packs_in_series}を走査中。')
            pack_links_in_series = [pack_elm.attrs['href'] for pack_elm in packs_in_series if
                                    not pack_elm.attrs['href'].startswith('#')]
            crawler_logger.debug(f'{pack_links_in_series}をパックと認識しました。')
            pack_links.extend(pack_links_in_series)

        unique_pack_links = set(pack_links)
        n_unique_packs = len(unique_pack_links)
        crawler_logger.info(f'{n_unique_packs}件のパックが見つかりました。')
        return unique_pack_links

    def get_pack_name(self, pack_path: str) -> str:
        crawler_logger.info('パック名の取得を開始')
        pack_html = self.get_html(self.root_url + pack_path)

        crawler_logger.info('パックのページ判定を実行します。')
        card_list = pack_html.find('div', id='list')
        assert card_list is not None

        pack_title = pack_html.find('h1', class_='entry-title').text.strip()
        crawler_logger.debug(f'パック名：{pack_title}')
        crawler_logger.info('パック名の取得を終了')
        return pack_title

    def get_card_infos(self, pack_path: str) -> List[Dict[str, str]]:
        crawler_logger.info('カード一覧の取得を開始')
        pack_html = self.get_html(self.root_url + pack_path)
        card_list = pack_html.find('div', id='list')
        card_inf_elms = [e for e in card_list.find_all('tr', class_=['status-height', 'spell-height'])
                         if e.find('td', class_='card-number') is not None]
        card_name_classes = ['n-mon', 'e-mon', 's-mon', 'x-mon', 'r-mon', 'l-mon', 'f-mon', 'p-mon', 'magic', 'trap',
                             'back-red', 'back-yellow', 'back-purple']
        pass_classes = ['card-pass', 'non-stts']
        card_infos = []
        for card_info in card_inf_elms:
            card_no = card_info.find('td', class_='card-number').text
            password = card_info.find('td', class_=pass_classes).text
            card_name_elm = card_info.find(class_=card_name_classes)
            card_name = ''
            for name_elm in card_name_elm.children:
                if isinstance(name_elm, Tag) and (name_elm.name == 'ruby'):
                    card_name += ''.join([e for e in name_elm.children if isinstance(e, str)])
                elif isinstance(name_elm, str):
                    card_name += name_elm
            logger.debug(f'カードが見つかりました。カード番号: {card_no}, パスワード: {password}, 名前: {card_name}')
            card_infos.append({'number': card_no, 'password': password, 'name': card_name})
        return card_infos
