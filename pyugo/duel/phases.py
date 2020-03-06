from enum import Enum

from typing import ClassVar

from pyugo.duel.callback import YGOCallbackBuilder, GetPlayer, GetTurnNo, IsFirstPlayer, CountDeck, \
    YGODefeatDeclarationCallback, MakeDraw
from pyugo.duel.player import YGOPlayer

from pyugo import duel_logger as logger


class YGOPhaseTypes(Enum):
    DRAW_PHASE = 'draw'
    STANDBY_PHASE = 'standby'
    MAIN1_PHASE = 'main1'
    BATTLE_PHASE = 'battle'
    MAIN2_PHASE = 'main2'
    END_PHASE = 'end'


class YGOPhaseBase(object):
    cb_builder: YGOCallbackBuilder
    phase_type: ClassVar[YGOPhaseTypes]

    def __init__(self, player: YGOPlayer, cb_builder: YGOCallbackBuilder):
        self.player = player
        self.cb_builder = cb_builder

    def proceed(self):
        """
        フェイズを処理する。
        """
        raise NotImplementedError()


class YGODrawPhase(YGOPhaseBase):
    phase_type: ClassVar[YGOPhaseTypes] = YGOPhaseTypes.DRAW_PHASE

    def proceed(self):
        logger.info(f'プレイヤー{self.player.player_no}のドローフェイズを開始')
        player = self.cb_builder.build_callback(GetPlayer)(self.player.player_no)
        turn_no = self.cb_builder.build_callback(GetTurnNo)(player)
        is_first_player = self.cb_builder.build_callback(IsFirstPlayer)(player)
        if (turn_no == 1) and is_first_player:
            logger.info(f'先行プレイヤーの第1ターンのドローフェイズをスキップ')
        deck_len = self.cb_builder.build_callback(CountDeck)(player)
        logger.info(f'プレイヤー{self.player.player_no}のデッキは残り{deck_len}枚')
        if deck_len == 0:
            logger.info(f'プレイヤー{self.player.player_no}はデッキからカードをドローできない')
            self.cb_builder.build_callback(YGODefeatDeclarationCallback)(self.player)
            return
        self.cb_builder.build_callback(MakeDraw)(player)
        logger.info(f'プレイヤー{self.player.player_no}のドローフェイズを終了')
