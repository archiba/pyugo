from typing import Type


class YGOPlayerCallbackInterface(object):
    def make_draw(self):
        raise NotImplementedError()

    def count_deck(self) -> int:
        raise NotImplementedError()

    def get_enemy(self) -> 'YGOPlayerCallbackInterface':
        raise NotImplementedError()

    def get_turn_no(self) -> int:
        raise NotImplementedError()

    def is_first_player(self) -> bool:
        raise NotImplementedError()


class YGODuelCallbackInterface(object):
    def get_player(self, player_no: int) -> YGOPlayerCallbackInterface:
        raise NotImplementedError()

    def finish(self, won_player: YGOPlayerCallbackInterface):
        raise NotImplementedError()

    def is_finished(self) -> bool:
        raise NotImplementedError()


D = YGODuelCallbackInterface
P = YGOPlayerCallbackInterface


class YGODuelCallback(object):
    duel: D

    def __init__(self, duel: D):
        self.duel = duel

    def __call__(self, *args, **kwargs):
        raise NotImplementedError()


class YGOCallbackBuilder(object):
    def __init__(self, duel: D):
        self.duel = duel

    def build_callback(self, callback_type: Type[YGODuelCallback]) -> YGODuelCallback:
        return callback_type(self.duel)


def skip_when(callback: YGODuelCallback):
    def skip_when_true(func):
        def wrapper(*args, **kwargs):
            if callback():
                return
            return func(*args, **kwargs)

        return wrapper

    return skip_when_true


class YGOGetPlayerCallback(YGODuelCallback):
    def __call__(self, player_no: int) -> P:
        return self.duel.get_player(player_no)


class YGOGetEnemyCallback(YGODuelCallback):
    def __call__(self, player_no: int) -> P:
        return self.duel.get_player(player_no).get_enemy()


class YGODefeatDeclarationCallback(YGODuelCallback):

    def __call__(self, player: P):
        self.duel.finish(player.get_enemy())


class YGOVictoryDeclarationCallback(YGODuelCallback):

    def __call__(self, player: P):
        self.duel.finish(player)


class YGOIsFinishedCallback(YGODuelCallback):
    def __call__(self) -> bool:
        return self.duel.is_finished()


class YGOGetTurnNoCallback(YGODuelCallback):
    def __call__(self, player: P) -> int:
        return player.get_turn_no()


class YGOIsFirstPlayerCallback(YGODuelCallback):
    def __call__(self, player: P) -> bool:
        return player.is_first_player()


class YGOCoundDeckCallback(YGODuelCallback):
    def __call__(self, player: P) -> int:
        return player.count_deck()


class YGOMakeDrawCallback(YGODuelCallback):
    def __call__(self, player: P) -> int:
        return player.make_draw()


GetPlayer = YGOGetPlayerCallback
GetEnemy = YGOGetEnemyCallback
Defeat = YGODefeatDeclarationCallback
Victory = YGOVictoryDeclarationCallback
IsFinished = YGOIsFinishedCallback
GetTurnNo = YGOGetTurnNoCallback
IsFirstPlayer = YGOIsFirstPlayerCallback
CountDeck = YGOCoundDeckCallback
MakeDraw = YGOMakeDrawCallback
