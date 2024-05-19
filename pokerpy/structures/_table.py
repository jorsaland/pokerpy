"""
Defines the class that represents a poker table.
"""


import random


from ._player import Player


class Table:


    """
    Represents a poker table and the dealer in charge.
    """


    def __init__(self, players: list[Player]):

        # Input variables
        self.players = players

        # State variables
        self.active_players: list[Player] = []
        self.is_under_bet = False
        self.last_aggressive_player: (Player|None) = None


    def activate_all_players(self):

        """
        Make all players to be available to play.
        """

        self.active_players.clear()
        self.active_players.extend(self.players)


    def reset_betting_round_states(self):
        
        """
        Resets all state variables that are restricted to betting rounds.
        """

        self.is_under_bet = False
        self.last_aggressive_player = None


    def deal(self, betting_round: str):

        """
        Makes the dealer to deal the cards.
        """

        print(f'Dealer deals cards for {betting_round}.\n')


    def showdown(self):

        """
        Makes the dealer to determine who is the winner among remaining players.
        """

        print(f'\n=== SHOWDOWN! ===\n')

        print(f'Remaining players: {", ".join(p.name for p in self.active_players)}')
        winner = random.choice(self.active_players)
        print(f'{winner.name} wins!')