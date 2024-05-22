"""
Defines the class that represents a poker table.
"""


import random
from typing import Iterable


from ._player import Player


class Table:


    """
    Represents a poker table and the dealer in charge.
    """


    def __init__(self, players: Iterable[Player]):

        # Input variables
        self.players = list(players)

        # State variables
        self.active_players: set[Player] = set()
        self.is_under_bet = False


    def activate_all_players(self):

        """
        Make all players to be available to play.
        """

        self.active_players.clear()
        self.active_players.update(self.players)


    def reset_betting_round_states(self):
        
        """
        Resets all state variables that are restricted to betting rounds.
        """

        self.is_under_bet = False


    def deal(self, betting_round: str):

        """
        Makes the dealer to deal the cards.
        """

        print(f'Dealer deals cards for {betting_round}.\n')


    def showdown(self):

        """
        Makes the dealer to determine who is the winner among remaining players.
        """

        print(f'Remaining players: {", ".join(p.name for p in self.active_players)}')
        winner = random.choice(list(self.active_players))
        print(f'{winner.name} wins!')