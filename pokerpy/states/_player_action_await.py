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


from pokerpy.structures import Action, Player
from pokerpy.validations import validate_type_action


from ._awaiter_helpers import ActionName, Await, PlayerMixin, PlayerDict, RangeDict, RangesMixin


class PlayerActionAwaitDict(TypedDict):
    player: PlayerDict
    ranges: dict[ActionName, RangeDict]


class PlayerActionAwait(Await, PlayerMixin, RangesMixin):


    "Await object for a player turn."


    def __init__(self, *, player: Player, ranges: dict[ActionName, range]):

        self._player = player
        self._ranges = ranges

        self._requested_action: Action|None = None


    @property
    def player(self):
        "Player to be awaited."
        return self._player

    @property
    def ranges(self):
        "Available action ranges."
        return self._ranges

    @property
    def requested_action(self):
        "Action the player has requested in a betting round."
        return self._requested_action


    def to_dict(self):
        state_dict: PlayerActionAwaitDict = {
            'player': self._build_player_dict(),
            'ranges': self._build_ranges_dict()
        }
        return state_dict


    def request_action(self, action: Action):

        "Chooses an action to request."

        validate_type_action(action)
        self._requested_action = action