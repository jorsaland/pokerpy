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


def method_set_current_player(self: "Table", player: Player):

    if not isinstance(player, Player):
        raise TypeError(msg_not_player_instance.format(type(player).__name__))

    if player not in self.players:
        raise ValueError(msg_player_not_in_table.format(player.name))

    self._current_player = player