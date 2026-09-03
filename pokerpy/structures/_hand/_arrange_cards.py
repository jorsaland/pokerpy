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
Defines the function that arranges a list of cards from most to least repeated and from highest to lowest value.
"""


from collections.abc import Iterable
from typing import NewType


from pokerpy import constants
from pokerpy.validations import validate_iterable_5_cards_hand, validate_iterable_not_repeated_cards


from .._card import Card


HandTuple = NewType('HandTuple', tuple[Card])


def arrange_cards(cards: Iterable[Card]):

    """
    Arranges a list of cards from most to least repeated and from highest to lowest value.
    """

    cards = list(cards)

    # Validate input

    validate_iterable_5_cards_hand(cards)
    validate_iterable_not_repeated_cards(cards)

    # Sort from higher to lower value

    cards.sort(key=Card.get_deck_position, reverse=True)

    # Arrange cards in a special way if hand is a five-to-ace straight

    wrongly_sorted_five_to_ace = [
        constants.ACES,
        constants.FIVES,
        constants.FOURS,
        constants.THREES,
        constants.DEUCES,
    ]
    
    if [card.value for card in cards] == wrongly_sorted_five_to_ace: # special sorting case --> A5432 becomes 5432A
        cards.append(cards.pop(0))
        return HandTuple(tuple(cards))
    
    # Otherwise, arrange cards from most to least repeated value

    card_values = [card.value for card in cards]
    counts_by_value = {value: card_values.count(value) for value in card_values}

    cards.sort(reverse=True, key=(lambda card: counts_by_value[card.value]))
    return HandTuple(tuple(cards))