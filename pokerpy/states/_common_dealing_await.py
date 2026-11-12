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


from collections.abc import Iterable
from typing import TypedDict


from pokerpy.structures import Card
from pokerpy.validations import validate_all_type_card, validate_type_iterable


from ._awaiter_helpers import Await, CardDict, DeckMixin


class CommonDealingAwaitDict(TypedDict):
    count: int
    deck: list[CardDict]


class CommonDealingAwait(Await, DeckMixin):


    "Await object for common cards dealing."


    def __init__(self, *, count: int, deck: tuple[Card, ...]):

        self._count = count
        self._deck = deck

        self._dealt_cards: tuple[Card, ...] = ()


    @property
    def count(self):
        "Number of cards to be dealt."
        return self._count

    @property
    def deck(self):
        "Available cards in the deck."
        return self._deck

    @property
    def dealt_cards(self):
        "Cards dealt to the player."
        return self._dealt_cards


    def to_dict(self):

        "Serializes the state object to JSON format."

        state_dict: CommonDealingAwaitDict = {
            'count': self.count,
            'deck': self._build_deck_list(),
        }
        return state_dict


    def deal_cards(self, cards: Iterable[Card]):

        "Chooses an action to request."

        validate_type_iterable(cards)
        validate_all_type_card(cards)

        self._dealt_cards = tuple(cards)