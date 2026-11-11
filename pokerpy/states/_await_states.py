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
from typing import Literal, TypedDict


from pokerpy.structures import Action, Card, Player
from pokerpy.validations import (
    validate_type_action,
    validate_type_iterable,
    validate_all_type_card,
    validate_iterable_not_repeated_cards,
)


ActionName = Literal['check', "fold", "call", "bet", "raise"]


class PlayerDict(TypedDict):
    name: str
    stack: int

class CardDict(TypedDict):
    value: str
    suit: str

class RangeDict(TypedDict):
    min: int
    max: int


class PlayerTurnAwaitDict(TypedDict):
    player: PlayerDict
    ranges: dict[ActionName, RangeDict]


class PlayerBlindAwaitDict(TypedDict):
    player: PlayerDict
    place_blind: bool


class PlayerCardsDealAwaitDict(TypedDict):
    player: PlayerDict
    count: int
    deck: list[CardDict]


class Await:
    "Base class that represents an await state."
    pass


class PlayerBlindAwait(Await):


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

        player_dict: PlayerDict = {'name': self.player.name, 'stack': self.player.stack}

        state_dict: PlayerBlindAwaitDict = {
            'player': player_dict,
            'amount': self.amount
        }
        return state_dict


    def place_blind(self):

        "Chooses to place a blind."

        self._placed_blind = True


class PlayerActionAwait(Await):


    "Await object for a player turn."


    def __init__(self, *, player: Player, ranges: dict[ActionName, RangeDict]):

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

        "Serializes the state object to JSON format."

        player_dict: PlayerDict = {'name': self.player.name, 'stack': self.player.stack}
        ranges_dict: dict[ActionName, RangeDict] = {action_name: {'min': action_range[0], 'max': action_range[-1]} for action_name, action_range in self.ranges.items()}

        state_dict: PlayerTurnAwaitDict = {
            'player': player_dict,
            'ranges': ranges_dict
        }
        return state_dict


    def request_action(self, action: Action):

        "Chooses an action to request."

        validate_type_action(action)
        self._requested_action = action


class PlayerCardsDealAwait(Await):


    "Await object for player cards dealing."


    def __init__(self, *, player: Player, count: int, deck: tuple[Card, ...]):

        self._player = player
        self._count = count
        self._deck = deck

        self._dealt_cards: tuple[Card, ...] = ()


    @property
    def player(self):
        "Player to be awaited."
        return self._player

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

        player_dict: PlayerDict = {'name': self.player.name, 'stack': self.player.stack}
        card_dicts: list[CardDict] = [{'value': card.value, 'suit': card.suit} for card in self.deck]

        state_dict: PlayerCardsDealAwaitDict = {
            'player': player_dict,
            'count': self.count,
            'deck': card_dicts,
        }
        return state_dict


    def deal_cards(self, cards: Iterable[Card]):

        "Chooses an action to request."

        validate_type_iterable(cards)
        validate_all_type_card(cards)

        self._dealt_cards = tuple(cards)


class CommonCardsDealAwait(Await):


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

        card_dicts: list[CardDict] = [{'value': card.value, 'suit': card.suit} for card in self.deck]

        state_dict: PlayerCardsDealAwaitDict = {
            'count': self.count,
            'deck': card_dicts,
        }
        return state_dict


    def deal_cards(self, cards: Iterable[Card]):

        "Chooses an action to request."

        validate_type_iterable(cards)
        validate_all_type_card(cards)

        self._dealt_cards = tuple(cards)