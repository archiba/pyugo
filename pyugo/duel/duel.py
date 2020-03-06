from typing import Dict

from pyugo.duel.callback import YGOCallbackBuilder, YGODuelCallbackInterface, YGOPlayerCallbackInterface, IsFinished, \
    GetPlayer
from pyugo.duel.field import YGOField
from pyugo.duel.player import YGOPlayer
from pyugo.duel.turn import YGOTurn

from pyugo import duel_logger as logger


class YGODuel(YGODuelCallbackInterface):
    cb_builder: YGOCallbackBuilder
    player1: YGOPlayer
    player2: YGOPlayer
    players: Dict[int, YGOPlayer]
    next_player_no: int = 0
    field: YGOField
    won_player_no: int = 0

    def __init__(self, player1: YGOPlayer, player2: YGOPlayer):
        logger.info('デュエルを生成中')
        self.cb_builder = YGOCallbackBuilder(duel=self)
        self.player1 = player1
        self.player2 = player2
        self.players = {1: self.player1, 2: self.player2}
        logger.info('デュエルフィールドを生成中')
        self.field = self._build_field()

    def _build_field(self) -> YGOField:
        """
        デュエル用フィールドの生成
        :return: フィールド
        """
        return YGOField()

    def standby(self):
        """
        デュエルの準備を行う。

        - プレイヤーの設定
        - 挨拶
        - 先行・後攻の決定
        - デッキのシャッフル

        """
        logger.info('デュエルの準備中')
        self.player1.player_no = 1
        self.player1.enemy = self.player2
        self.player2.player_no = 2
        self.player2.enemy = self.player1
        logger.info('先行・後攻の決定中')
        self.next_player_no = self._decide_first_player()
        logger.info(f'先行はプレイヤー{self.next_player_no}')

    def _decide_first_player(self):
        """
        先行プレイヤーを決定
        :return: 先行プレイヤー番号
        """
        return 1

    def get_player(self, player_no: int) -> YGOPlayer:
        """
        プレイヤー番号からプレイヤーを返す
        :param player_no: プレイヤー番号
        :return: プレイヤー
        """
        return self.players[player_no]

    def is_finished(self) -> bool:
        """
        デュエルが終了しているかチェック
        :return: 終了しているかどうか
        """
        return self.won_player_no != 0

    def finish(self, won_player: YGOPlayer):
        """
        デュエルの勝利宣言
        :param won_player: 勝利したプレイヤー
        """
        logger.info(f'デュエルが終了しました。')
        self.won_player_no = won_player.player_no
        logger.info(f'勝者はプレイヤー{self.won_player_no}')

    def _cycle_player_no(self):
        """
        ターンプレイヤーを変更する
        """
        if self.next_player_no == 1:
            self.next_player_no = 2
        self.next_player_no = 1

    def _build_turn(self, player: YGOPlayer):
        """
        ターンの生成
        :param player: ターンプレイヤー
        :return: ターン
        """
        return YGOTurn(player, self.cb_builder)

    def start(self) -> int:
        """
        デュエルのループ処理と、戦闘終了条件の管理。

        :return: 勝利プレイヤー番号
        """
        while not self.cb_builder.build_callback(IsFinished)():
            logger.info('ターンを開始')
            player = self.cb_builder.build_callback(GetPlayer)(self.next_player_no)
            logger.info(f'ターンプレイヤーはプレイヤー{self.next_player_no}')
            logger.info('ターンの生成中')
            turn = self._build_turn(player)
            logger.info('ターンの処理を開始')
            turn.proceed()
            logger.info('ターンの処理を終了')
            logger.info('ターンプレイヤーの変更中')
            self._cycle_player_no()
            logger.info(f'次のターンプレイヤーはプレイヤー{self.next_player_no}')
            logger.info('ターンを終了')
        return self.won_player_no
