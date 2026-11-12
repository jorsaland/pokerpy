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


from abc import abstractmethod, ABC
from typing import get_args, Literal, TypedDict


from pokerpy.constants import possible_action_names
from pokerpy.structures import Card, Player


ActionName = Literal['check', "fold", "call", "bet", "raise"]
assert set(get_args(ActionName)) == set(possible_action_names)


class PlayerDict(TypedDict):
    name: str
    stack: int

class CardDict(TypedDict):
    value: str
    suit: str

class RangeDict(TypedDict):
    min: int
    max: int


class Await(ABC):

    "Base class that represents an await state."

    @abstractmethod
    def to_dict(self):
        "Serializes the state object to JSON format."
        return NotImplemented


class PlayerMixin:

    "Defines the method that serializes the player."

    player: Player

    def _build_player_dict(self):
        "Builds the player dict from an await state that has a player attribute."
        player_dict: PlayerDict = {'name': self.player.name, 'stack': self.player.stack}
        return player_dict


class RangesMixin:

    "Defines the method that serializes the ranges."

    ranges: dict[ActionName, range]

    def _build_ranges_dict(self):
        "Builds the ranges dict from an await state that has a ranges attribute."
        ranges_dict: dict[ActionName, RangeDict] = {
            action_name: {'min': action_range[0], 'max': action_range[-1]}
            for action_name, action_range in self.ranges.items()
        }
        return ranges_dict


class DeckMixin:

    "Defines the method that serializes the deck's available cards cards."

    deck: tuple[Card, ...]

    def _build_deck_list(self):
        "Builds the deck list from an await state that has a deck attribute."
        deck_list: list[CardDict] = [{'value': card.value, 'suit': card.suit} for card in self.deck]
        return deck_list