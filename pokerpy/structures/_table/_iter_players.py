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
Defines the method that iterates over all the players.
"""


from typing import TYPE_CHECKING


from pokerpy.validations import validate_type_player, validate_player_in_table


from .._player import Player
if TYPE_CHECKING:
    from ._table import Table


def iter_players_method(table: "Table", *, starting_player: (Player|None), reverse: bool):

    "Iterates over all the players."

    if starting_player is None:
        starting_player = table.starting_player

    validate_type_player(starting_player)
    validate_player_in_table(starting_player, table.players)

    if reverse:
        get_player = table.get_previous_player
    else:
        get_player = table.get_next_player

    def generator():
        yield starting_player
        next_player = get_player(starting_player)
        while next_player != starting_player:
            yield next_player
            next_player = get_player(next_player)
    
    return generator()