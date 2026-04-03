# Copyright 2026 Andrés Saldarriaga Jordan (jorsaland)

# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at

#     http://www.apache.org/licenses/LICENSE-2.0

# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.


"""
Defines the methods related to players.
"""


from typing import TYPE_CHECKING


from pokerpy.messages import msg_not_player_instance, msg_player_not_in_table


from .._player import Player
if TYPE_CHECKING:
    from ._table import Table


def method_set_starting_player(self: "Table", player: Player):

    if not isinstance(player, Player):
        raise TypeError(msg_not_player_instance.format(type(player).__name__))

    if player not in self.players:
        raise ValueError(msg_player_not_in_table.format(player.name))

    self._starting_player = player


def method_set_stopping_player(self: "Table", player: Player):

    if not isinstance(player, Player):
        raise TypeError(msg_not_player_instance.format(type(player).__name__))

    if player not in self.players:
        raise ValueError(msg_player_not_in_table.format(player.name))

    self._stopping_player = player


def method_get_next_player(self: "Table", reference_player: Player):

    if reference_player not in self.players:
        raise ValueError(msg_player_not_in_table.format(reference_player.name))

    if reference_player == self.players[-1]:
        return self.players[0]

    reference_player_index = self.players.index(reference_player)
    return self.players[reference_player_index + 1]


def method_get_previous_player(self: "Table", reference_player: Player):

    if not isinstance(reference_player, Player):
        raise TypeError(msg_not_player_instance.format(type(reference_player).__name__))

    if reference_player not in self.players:
        raise ValueError(msg_player_not_in_table.format(reference_player.name))

    reference_player_index = self.players.index(reference_player)
    return self.players[reference_player_index - 1]


def method_iter_players(self: "Table", starting_player: (Player|None) = None, reverse: bool = False):

    if starting_player is None:
        starting_player = self.starting_player

    if not isinstance(starting_player, Player):
        raise TypeError(msg_not_player_instance.format(type(starting_player).__name__))

    if starting_player not in self.players:
        raise ValueError(msg_player_not_in_table.format(starting_player.name))

    if reverse:
        get_player = self.get_previous_player
    else:
        get_player = self.get_next_player

    def generator():
        yield starting_player
        next_player = get_player(starting_player)
        while next_player != starting_player:
            yield next_player
            next_player = get_player(next_player)
    
    return generator()


def method_get_previous_active_player(self: "Table", reference_player: Player):

    # This method exists to set the stopping player to the previous active player when the current
    # player takes an aggressive action (bet or raise), in order to avoid iterating over players
    # who are already folded or all-in. It should be used carefully in other contexts.

    if not isinstance(reference_player, Player):
        raise TypeError(msg_not_player_instance.format(type(reference_player).__name__))

    if reference_player not in self.players:
        raise ValueError(msg_player_not_in_table.format(reference_player.name))

    for player in self.iter_players(self.get_previous_player(reference_player), reverse=True):
        if player in self.active_players:
            return player