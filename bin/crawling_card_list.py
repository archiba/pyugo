import logging
from logging import StreamHandler
from sys import stdout

import fire

from pyugo_db.crawlers.list import YGOCardListCrawler
from pyugo_db.models import YGOCrawlingPack, YGOCrawlingCardInfo, get_session

logger = logging.Logger('crawling_script')


def run(log_level: str = 'INFO'):
    logger.setLevel(log_level)
    logger.addHandler(StreamHandler(stream=stdout))
    logger.info('カードリストのクローリングを開始します。')
    logger.info('クローラーを初期化しています。')
    crawler = YGOCardListCrawler()
    logger.info('パックの一覧を取得します。')
    pack_urls = crawler.get_pack_urls()
    for i, pack_url in enumerate(pack_urls):
        logger.info(f'{i}番目のパックの情報とカードリストを取得します。')
        try:
            pack_title = crawler.get_pack_name(pack_url)
        except AssertionError:
            logger.warning(f'{i}番目のパック@{pack_url}は正しいページではなかったため処理をスキップします。')
            continue
        logger.info(f'パック「{pack_title}」をDBへと登録しています。')
        pack = YGOCrawlingPack(id=pack_url.split('/')[-2], name=pack_title, url=pack_url)
        session = get_session()
        session.add(instance=pack)

        card_list = crawler.get_card_infos(pack_url)
        for card in card_list:
            logger.info(f'カード「{card["name"]}」をDBへと登録しています。')
            card_info = YGOCrawlingCardInfo(name=card['name'], password=card['password'], card_no=card['number'],
                                            pack_id=pack.id)
            session.add(card_info)
        logger.info(f'パック情報とカード情報の追加を適用します。')
        session.commit()
    logger.info('カードリストのクローリングが完了しました。')


if __name__ == '__main__':
    fire.Fire(run)
