"""
Defines the methods that affect player attributes.
"""


from typing import TYPE_CHECKING


from pokerpy.messages import (
    msg_not_player_instance,
    msg_player_is_inactive,
    msg_player_not_in_table,
)
from pokerpy.structures import Player


if TYPE_CHECKING:
    from ._betting_round import BettingRound


def method_activate_player(self: "BettingRound", player: Player):
    
    """
    Make a single player to become available to play.
    """

    if not isinstance(player, Player):
        raise TypeError(msg_not_player_instance.format(type(player).__name__))
    
    if player not in self.table.players:
        raise ValueError(msg_player_not_in_table.format(player.name))

    if player not in self.active_players:
        self._active_players.append(player)


def method_deactivate_player(self: "BettingRound", player: Player):

    """
    Removes a player from a hand cycle.
    """

    if not isinstance(player, Player):
        raise TypeError(msg_not_player_instance.format(type(player).__name__))
    
    if player not in self.table.players:
        raise ValueError(msg_player_not_in_table.format(player.name))

    if player not in self.active_players:
        raise ValueError(msg_player_is_inactive.format(player.name))

    self._active_players.remove(player)


def method_set_stopping_player(self: "BettingRound", player: Player):

    """
    Marks a player before whom the betting round is closed.
    """

    if not isinstance(player, Player):
        raise TypeError(msg_not_player_instance.format(type(player).__name__))

    if player not in self.table.players:
        raise ValueError(msg_player_not_in_table.format(player.name))

    self._stopping_player = player