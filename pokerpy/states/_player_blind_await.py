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


"Defines the classes that represent await states."


from typing import TypedDict


from pokerpy.structures import Player


from ._awaiter_helpers import Await, PlayerDict, PlayerMixin


class PlayerBlindAwaitDict(TypedDict):
    player: PlayerDict
    place_blind: bool


class PlayerBlindAwait(Await, PlayerMixin):


    "Await object for a player optional blind phase."


    def __init__(self, *, player: Player, amount: int):

        self._player = player
        self._amount = amount

        self._placed_blind = False


    @property
    def placed_blind(self):
        "Whether the player has requested to place an extra blind."
        return self._placed_blind

    @property
    def player(self):
        "Player to be awaited."
        return self._player

    @property
    def amount(self):
        "Required blind amount."
        return self._amount


    def to_dict(self):

        "Serializes the state object to JSON format."

        state_dict: PlayerBlindAwaitDict = {
            'player': self._build_player_dict(),
            'amount': self.amount
        }
        return state_dict


    def place_blind(self):

        "Chooses to place a blind."

        self._placed_blind = True