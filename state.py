from player import Player
from card import Card


class GameState(object):
    def __init__(self, activePlayer, opponent):
        self.activePlayer = activePlayer
        self.opponent = opponent
    def __repr__(self):
        rep = str(self.activePlayer) + '|||' + str(self.opponent)
        return rep

    def swap(self):
        self.activePlayer, self.opponent = self.opponent, self.activePlayer