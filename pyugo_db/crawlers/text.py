from bs4 import Tag

from pyugo_db import crawler_logger
from pyugo_db.crawlers.base import YGOCrawlerBase
from pyugo_db.settings import PYUGO_DB_TEXT_CRAWLING_ROOT_URL

logger = crawler_logger


class YGOCardTextCrawler(YGOCrawlerBase):
    def __init__(self):
        super().__init__()
        self.root_url = PYUGO_DB_TEXT_CRAWLING_ROOT_URL

    @staticmethod
    def skip_rb(root_elm):
        text = ''
        for elm in root_elm.children:
            if isinstance(elm, Tag) and (elm.name == 'rb'):
                text += ''.join([e for e in elm.children if isinstance(e, str)])
            elif isinstance(elm, str):
                text += elm
        return text

    @staticmethod
    def get_and_drop(dic, k):
        v = dic[k]
        del dic[k]
        return v

    @staticmethod
    def get_and_drop_assert1(dic, k):
        l = YGOCardTextCrawler.get_and_drop(dic, k)
        assert len(l) == 1
        return l[0]

    @staticmethod
    def get_and_drop_nullable(dic, k):
        l = YGOCardTextCrawler.get_and_drop(dic, k)
        if len(l) == 0:
            return '-'
        else:
            assert len(l) == 1
            return l[0]

    @staticmethod
    def check_and_drop(l: list, v):
        result = v in l
        if result:
            l.remove(v)
        return result

    def get_text(self, card_no: str):
        logger.info(f'カード{card_no}のテキストの取得を開始。')
        search_html = self.get_html(self.root_url + '/' + card_no)
        text_values = {}

        logger.info(f'カード{card_no}の名称・読みの解析を開始。')
        text_values['name'], text_values['kana'] = self._extract_name(search_html)
        logger.info(f'カード{card_no}の名称・読み: {text_values["name"]}({text_values["kana"]})')
        logger.info(f'カード{card_no}のテキスト以外の情報の解析を開始。')
        card_types = self._extract_card_type(search_html)
        logger.debug(f'カード{card_no}の情報: {card_types}')
        text_values.update(card_types)
        logger.info(f'カード{card_no}のテキストの解析を開始。')
        text_values['card_text'], text_values['pendulum_text'] = self._extract_texts(search_html,
                                                                                     text_values['is_pendulum'])
        logger.debug(f'カード{card_no}のテキスト: {text_values["card_text"]}')
        logger.debug(f'カード{card_no}のペンデュラム効果テキスト: {text_values["pendulum_text"]}')
        return text_values

    @staticmethod
    def _extract_name(html):
        card_attributes_elm = html.find('div', class_='card-table')
        card_name_elm = card_attributes_elm.find('span', class_='nowrap', attrs={'lang': 'ja'})
        japanese_card_name = ''.join([v if isinstance(v, str) else YGOCardTextCrawler.skip_rb(v)
                                      for v in card_name_elm.children])
        if card_attributes_elm.find('span', class_='nowrap', attrs={'lang': 'ja-Hrkt'}) is None:
            japanese_card_kana = japanese_card_name
        else:
            japanese_card_kana = card_attributes_elm.find('span', class_='nowrap', attrs={'lang': 'ja-Hrkt'}).text
        return japanese_card_name, japanese_card_kana

    @staticmethod
    def _extract_texts(html, is_pendulum):
        name_and_text = list(html.find('th', text='Japanese').parent.find_all('td'))

        assert len(name_and_text) in (2, 3)
        card_text = ''.join([v if isinstance(v, str) else YGOCardTextCrawler.skip_rb(v)
                             for v in name_and_text[1].children])
        pendulum_text = None
        if len(name_and_text) == 3:
            assert is_pendulum
            pendulum_text = ''.join([v if isinstance(v, str) else YGOCardTextCrawler.skip_rb(v)
                                     for v in name_and_text[2].children])
        return card_text, pendulum_text

    @staticmethod
    def _extract_card_type(html):
        # 種類
        card_type = None

        # 属性
        card_attr = None
        # 種族
        type_ = None

        # monster type
        ## 効果
        has_effect = False
        ## ペンデュラム
        is_pendulum = False

        # monster card types
        ## 融合
        is_fusion = False
        ## 儀式
        is_ritual = False
        ## シンクロ
        is_synchro = False
        ## エクシーズ
        is_xyz = False
        ## リンク
        is_link = False

        # monster subtypes
        ## チューナー
        is_tuner = False
        ## トゥーン
        is_toon = False
        ## ユニオン
        is_union = False
        ## スピリット
        is_spirit = False
        ## デュアル
        is_gemini = False

        # レベル
        level = None
        # ランク
        rank = None
        # リンクマーカー
        link_arrows = None
        # 攻撃力
        attack = None
        # 守備力
        defense = None
        # リンク
        link = None

        # property
        ## 通常魔法
        is_normal_spell = False
        ## 永続魔法
        is_continuous_spell = False
        ## フィールド魔法
        is_field_spell = False
        ## 速攻魔法
        is_quick_play_spell = False
        ## 装備魔法
        is_equip_spell = False
        ## 儀式魔法
        is_ritual_spell = False
        ## 通常トラップ
        is_normal_trap = False
        ## 永続トラップ
        is_continuous_trap = False
        ## 通常トラップ
        is_counter_trap = False

        # ステータス
        status = None

        card_attributes_elm = html.find('div', class_='card-table')
        info_table = card_attributes_elm.find('div', class_='infocolumn').find('table')
        info_rows = info_table.find_all('tr')

        info_label_values = {}
        for info_row in info_rows:
            if info_row.find('th') is None:
                continue

            info_labels = [e.text for e in info_row.find('th').find_all('a') if e.text != '']

            if len(info_labels) == 0:
                continue

            info_label = info_labels[0]
            info_values = [e.text for e in info_row.find('td').find_all('a') if e.text != '']

            info_label_values[info_label] = info_values
        dic = info_label_values
        card_type = YGOCardTextCrawler.get_and_drop_assert1(dic, 'Card type')

        if card_type == 'Spell':
            prop = YGOCardTextCrawler.get_and_drop_assert1(dic, 'Property')
            if prop == 'Normal':
                is_normal_spell = True
            elif prop == 'Continuous':
                is_continuous_spell = True
            elif prop == 'Field':
                is_field_spell = True
            elif prop == 'Equip':
                is_equip_spell = True
            elif prop == 'Quick-Play':
                is_quick_play_spell = True
            elif prop == 'Ritual':
                is_ritual_spell = True
            else:
                assert False, (card_type, prop)
        elif card_type == 'Trap':
            prop = YGOCardTextCrawler.get_and_drop_assert1(dic, 'Property')
            if prop == 'Normal':
                is_normal_trap = True
            elif prop == 'Continuous':
                is_continuous_trap = True
            elif prop == 'Counter':
                is_field_trap = True
            else:
                assert False, (card_type, prop)
        elif card_type == 'Monster':
            types = YGOCardTextCrawler.get_and_drop(dic, 'Types')
            type_ = types.pop(0)
            card_attr = YGOCardTextCrawler.get_and_drop_assert1(dic, 'Attribute')
            if YGOCardTextCrawler.check_and_drop(types, 'Effect'):
                has_effect = True
            if YGOCardTextCrawler.check_and_drop(types, 'Pendulum'):
                is_pendulum = True
            if YGOCardTextCrawler.check_and_drop(types, 'Fusion'):
                is_fusion = True
            if YGOCardTextCrawler.check_and_drop(types, 'Ritual'):
                is_ritual = True
            if YGOCardTextCrawler.check_and_drop(types, 'Synchro'):
                is_synchro = True
            if YGOCardTextCrawler.check_and_drop(types, 'Xyz'):
                is_xyz = True
            if YGOCardTextCrawler.check_and_drop(types, 'Link'):
                is_link = True
            if YGOCardTextCrawler.check_and_drop(types, 'Tuner'):
                is_tuner = True
            if YGOCardTextCrawler.check_and_drop(types, 'Union'):
                is_union = True
            if YGOCardTextCrawler.check_and_drop(types, 'Toon'):
                is_toon = True
            if YGOCardTextCrawler.check_and_drop(types, 'Spirit'):
                is_spirit = True
            if YGOCardTextCrawler.check_and_drop(types, 'Gemini'):
                is_gemini = True
            assert len(types) == 0, types

            if is_link:
                link_arrows = ','.join(YGOCardTextCrawler.get_and_drop(dic, 'Link Arrows'))
            elif is_xyz:
                rank = YGOCardTextCrawler.get_and_drop_assert1(dic, 'Rank')
            else:
                level = YGOCardTextCrawler.get_and_drop_assert1(dic, 'Level')

            if is_link:
                attack, link = YGOCardTextCrawler.get_and_drop(dic, 'ATK')
            else:
                attack, defense = YGOCardTextCrawler.get_and_drop(dic, 'ATK')

        password = YGOCardTextCrawler.get_and_drop_nullable(dic, 'Password')
        status_all: list = YGOCardTextCrawler.get_and_drop(dic, 'Status')
        try:
            ocg_idx = status_all.index('OCG')
            status = status_all[ocg_idx - 1]
        except:
            pass

        assert len(dic) == 0, dic
        return {
            'card_type': card_type,
            'card_attr': card_attr,
            'type_': type_,
            'has_effect': has_effect,
            'is_pendulum': is_pendulum,
            'is_fusion': is_fusion,
            'is_ritual': is_ritual,
            'is_synchro': is_synchro,
            'is_xyz': is_xyz,
            'is_link': is_link,
            'is_tuner': is_tuner,
            'is_toon': is_toon,
            'is_union': is_union,
            'is_spirit': is_spirit,
            'is_gemini': is_gemini,
            'level': level,
            'rank': rank,
            'link_arrows': link_arrows,
            'attack': attack,
            'defense': defense,
            'link': link,
            'is_normal_spell': is_normal_spell,
            'is_continuous_spell': is_continuous_spell,
            'is_field_spell': is_field_spell,
            'is_quick_play_spell': is_quick_play_spell,
            'is_equip_spell': is_equip_spell,
            'is_ritual_spell': is_ritual_spell,
            'is_normal_trap': is_normal_trap,
            'is_continuous_trap': is_continuous_trap,
            'is_counter_trap': is_counter_trap,
            'password': password,
            'status': status}
