import logging
from logging import StreamHandler
from sys import stdout
from unittest import TestCase

from pyugo import duel_logger
from pyugo.card.card import YGOCard
from pyugo.duel.deck import YGOPlayingDeck, YGOPlayingMainDeck, YGOPlayingExtraDeck
from pyugo.duel.duel import YGODuel
from pyugo.duel.player import YGOPlayer

logging.basicConfig(level=logging.DEBUG, stream=stdout)


class FirstTest(TestCase):
    def test(self):
        duel_logger.setLevel(logging.DEBUG)
        duel_logger.addHandler(StreamHandler(stream=stdout))
        deck1 = YGOPlayingDeck(YGOPlayingMainDeck([YGOCard() for _ in range(40)]),
                               YGOPlayingExtraDeck([YGOCard() for _ in range(15)]))
        deck2 = YGOPlayingDeck(YGOPlayingMainDeck([YGOCard() for _ in range(40)]),
                               YGOPlayingExtraDeck([YGOCard() for _ in range(15)]))
        player1 = YGOPlayer(deck1)
        player2 = YGOPlayer(deck2)
        duel = YGODuel(player1, player2)
        duel.standby()
        result = duel.start()
        print(result)
