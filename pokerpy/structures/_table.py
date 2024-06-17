"""
Defines the class that represents a poker table.
"""


import random


from pokerpy.messages import (
    not_list_players_message,
    not_all_player_instances_message,
    not_player_instance_message,
    player_not_in_table_message,
    player_already_folded_message,
)


from ._player import Player


class Table:


    """
    Represents a poker table and the dealer in charge.
    """


    def __init__(self, players: list[Player], *, fold_to_nothing = False):

        # Check input
        if not isinstance(players, list):
            raise TypeError(not_list_players_message.format(type(players).__name__))
        if not all(isinstance(player, Player) for player in players):
            raise TypeError(not_all_player_instances_message)

        # Input variables
        self._players = players
        self.fold_to_nothing = fold_to_nothing

        # State variables
        self._active_players: list[Player] = []
        self._is_under_bet = False
        self._last_aggressive_player: (Player|None) = None
    

    @property
    def players(self):
        return tuple(self._players)
    
    @property
    def active_players(self):
        return tuple(self._active_players)

    @property
    def is_under_bet(self):
        return self._is_under_bet

    @property
    def last_aggressive_player(self):
        return self._last_aggressive_player


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

        if not isinstance(player, Player):
            raise TypeError(not_player_instance_message.format(type(player).__name__))
        
        if player not in self.players:
            raise ValueError(player_not_in_table_message.format(player.name))

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

        if not isinstance(player, Player):
            raise TypeError(not_player_instance_message.format(type(player).__name__))
        
        if player not in self.players:
            raise ValueError(player_not_in_table_message.format(player.name))

        if player not in self.active_players:
            raise ValueError(player_already_folded_message.format(player.name))

        self._active_players.remove(player)


    def set_last_aggressive_player(self, player: Player):

        """
        Marks a player as the last one to take an aggressive action.
        """

        if not isinstance(player, Player):
            raise TypeError(not_player_instance_message.format(type(player).__name__))

        if player not in self.players:
            raise ValueError(player_not_in_table_message.format(player.name))

        if player not in self.active_players:
            raise ValueError(player_already_folded_message.format(player.name))

        self._last_aggressive_player = player


    def reset_betting_round_states(self):
        
        """
        Resets all state variables that are restricted to betting rounds.
        """

        self._is_under_bet = False
        self._last_aggressive_player = None


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