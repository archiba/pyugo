import logging
import traceback
from logging import StreamHandler
from sys import stdout

import fire

from pyugo_db.crawlers.text import YGOCardTextCrawler
from pyugo_db.models import YGOCrawlingCardInfo, get_session, YGOCrawlingCardText

logger = logging.Logger('crawling_script')


def run(log_level: str = 'INFO', reload: bool = False):
    logger.setLevel(log_level)
    logger.addHandler(StreamHandler(stream=stdout))
    logger.info('カードテキストのクローリングを開始します。')
    logger.info('クローラーを初期化しています。')
    crawler = YGOCardTextCrawler()
    logger.info('クローリング済みのカード情報一覧をDBから取得します。')
    session = get_session()
    all_cards = list(session.query(YGOCrawlingCardInfo.id, YGOCrawlingCardInfo.card_no, YGOCrawlingCardInfo.name,
                                   YGOCrawlingCardInfo.password))
    logger.info('クローリング済みのカード情報一覧をDBから取得しました。')
    if not reload:
        logger.info('未クローリングのカードのみテキスト情報のクローリングを行ます。')
    else:
        logger.info('クローリング済みのカードを含む全てのカードのテキスト情報のクローリングを行ます。')

    for card in all_cards:
        logger.info(f'カードを調査中: ID: {card.id}, NO: {card.card_no}, 名前: {card.name}')
        result = list(session.query(YGOCrawlingCardText.id).filter(YGOCrawlingCardText.id == card.id).all())
        existing = None
        if len(result) == 1:
            logger.info('クローリング済みの情報が見つかりました。')
            existing = result[0]

        if (existing is not None) and (not reload):
            logger.info('収集済みのためスキップします。')
            continue

        if card.card_no != '-':
            crawling_key = card.card_no
        elif card.card_no == card.password == '-':
            logger.warning('カードにはNOもパスワードも存在しないため、クローリングを実行できません。')
            continue
        else:
            crawling_key = card.password

        logger.info('クローラーによる情報取得を開始します。')
        try:
            text_values = crawler.get_text(crawling_key)
        except Exception as e:
            logger.warning('例外が発生しました。このカードのクローリングを中断します。')
            logger.warning(f'例外: {e}, {traceback.format_exc()}')
            continue
        logger.info('クローラーによる情報取得が完了しました。')

        if reload:
            existing.update(text_values)
        else:
            session.add(YGOCrawlingCardText(card, text_values))
        logger.info('収集したテキスト情報をDBに記録します。')
        session.commit()
        logger.info('DBへの記録が完了しました。')
        logger.info(f'カードに対するテキスト収集が完了しました。: ID: {card.id}, NO: {card.card_no}, 名前: {card.name}')


if __name__ == '__main__':
    fire.Fire(run)
