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
        self._players = players

        # State variables
        self._active_players: list[Player] = []
        self._is_under_bet = False
    

    @property
    def players(self):
        return tuple(self._players)
    
    @property
    def active_players(self):
        return tuple(self._active_players)

    @property
    def is_under_bet(self):
        return self._is_under_bet


    def activate_all_players(self):

        """
        Make all players to be available to play.
        """

        self._active_players.clear()
        self._active_players.extend(self._players)


    def activate_player(self, player: Player):
        
        """
        Make a single player to become available to play.
        """

        if player not in self.active_players:
            self._active_players.append(player)


    def become_under_bet(self):

        """
        Makes the betting round to become under bet.
        """

        self._is_under_bet = True
    

    def fold_player(self, player: Player):

        """
        Removes a player from a hand cycle.
        """

        self._active_players.remove(player)


    def reset_betting_round_states(self):
        
        """
        Resets all state variables that are restricted to betting rounds.
        """

        self._is_under_bet = False


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
        winner = random.choice(self.active_players)
        print(f'{winner.name} wins!')