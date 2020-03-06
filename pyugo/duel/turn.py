from typing import List

from pyugo.duel.callback import YGOCallbackBuilder
from pyugo.duel.phases import YGOPhaseBase, YGODrawPhase
from pyugo.duel.player import YGOPlayer
from pyugo import duel_logger as logger


class YGOTurn(object):
    cb_builder: YGOCallbackBuilder
    player: YGOPlayer
    phases: List[YGOPhaseBase]

    def __init__(self, player: YGOPlayer, cb_builder: YGOCallbackBuilder):
        self.player = player
        self.cb_builder = cb_builder
        self.phases = self.build_phases()

    def build_phases(self) -> List[YGOPhaseBase]:
        """
        ターンのフェイズ進行を生成
        :return: フェイズ進行
        """
        return [YGODrawPhase(self.player, self.cb_builder), ]

    def proceed(self):
        self.player.increment_turn_no()
        logger.info(f'プレイヤー{self.player.player_no}の第{self.player.turn_no}ターンを開始')
        for phase in self.phases:
            phase.proceed()
