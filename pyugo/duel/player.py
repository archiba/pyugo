from typing import Optional, List

from pyugo.card.card import YGOCard
from pyugo.duel.callback import YGOPlayerCallbackInterface
from pyugo.duel.deck import YGOPlayingDeck

from pyugo import duel_logger as logger


class YGOHand(object):
    cards: List[YGOCard]

    def __init__(self):
        self.cards = []

    def __len__(self) -> int:
        return len(self.cards)

    def add(self, card: YGOCard):
        self.cards.append(card)
        logger.debug(f'手札にカード{card}が加えられました。')
        logger.debug(f'現在の手札は{self}。')

    def consume(self, index: int) -> YGOCard:
        consumed_card = self.cards.pop(index)
        logger.debug(f'手札から{index}番目のカード{consumed_card}が無くなりました。')
        logger.debug(f'現在の手札は{self}。')
        return consumed_card


class YGOPlayer(YGOPlayerCallbackInterface):
    deck: YGOPlayingDeck
    hand: YGOHand
    enemy: Optional['YGOPlayer']
    turn_no: int = 0
    _is_first_player: bool = False
    life_point: int = 8000
    player_no: int

    def __init__(self, deck: YGOPlayingDeck):
        self.deck = deck
        self.hand = YGOHand()

    def set_player_no(self, player_no: int):
        self.player_no = player_no

    def set_is_first_player(self, is_first_player: bool):
        self._is_first_player = is_first_player

    def set_enemy(self, enemy: 'YGOPlayer'):
        self.enemy = enemy

    def increment_turn_no(self):
        self.turn_no += 1

    def _draw(self):
        self.hand.add(self.deck.main_deck.draw())

    def make_draw(self):
        """
        デッキの一番上からカードをドローする
        """
        logger.info(f'プレイヤー{self.player_no}はデッキの一番上から１枚カードをドロー')
        self._draw()

    def count_deck(self) -> int:
        return len(self.deck.main_deck)

    def get_enemy(self) -> 'YGOPlayerCallbackInterface':
        return self.enemy

    def get_turn_no(self) -> int:
        return self.turn_no

    def is_first_player(self) -> bool:
        return self._is_first_player