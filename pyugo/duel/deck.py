import random
from typing import List, ClassVar

from pyugo.card.card import YGOCard


class YGOPlayingMainDeck(object):
    cards: List[YGOCard]
    random_state: ClassVar[random.Random] = random.Random(0)

    @classmethod
    def set_random_state(cls, random_state: random.Random):
        """
        乱数生成器をセット
        :param random_state: 乱数生成器
        """
        cls.random_state = random_state

    def __init__(self, cards: List[YGOCard]):
        self.cards = cards

    def shuffle(self):
        """
        デッキをシャッフルする
        """
        self.cards = self.__class__.random_state.shuffle(self.cards)

    def __len__(self) -> int:
        """
        デッキの残り枚数を返す
        :return: 残り枚数
        """
        return len(self.cards)

    def draw(self) -> YGOCard:
        """
        デッキの一番上からカードを一枚ドローする。
        同時にデッキは一枚減る。

        :return: ドローしたカード。
        """
        return self.cards.pop(0)

    def add(self, card: YGOCard):
        """
        カードをデッキに加える。
        自動的にシャッフルする。

        :param card: 加えるカード
        """
        self.cards.append(card)
        self.shuffle()


class YGOPlayingExtraDeck(object):
    cards: List[YGOCard]

    def __init__(self, cards: List[YGOCard]):
        self.cards = cards


class YGOPlayingDeck(object):
    main_deck: YGOPlayingMainDeck
    extra_deck: YGOPlayingExtraDeck

    def __init__(self, main_deck: YGOPlayingMainDeck, extra_deck: YGOPlayingExtraDeck):
        self.main_deck = main_deck
        self.extra_deck = extra_deck
