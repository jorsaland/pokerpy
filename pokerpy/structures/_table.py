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
Defines the class that represents a poker table.
"""


from pokerpy.constants import sorted_card_values_and_suits
from pokerpy.logger import get_logger
from pokerpy.validations import (
    validate_all_type_player,
    validate_card_in_deck,
    validate_int_positive,
    validate_int_positive_or_zero,
    validate_iterable_not_contains_card,
    validate_player_in_table,
    validate_not_empty_table,
    validate_type_card,
    validate_type_int,
    validate_type_list,
    validate_type_player,
)


from ._card import Card
from ._player import Player


logger = get_logger()


class Table:


    """
    Represents a poker table and the dealer in charge.
    """


    def __init__(
        self,
        players: list[Player],
        *,
        min_bet: int = 1,
        starting_player: (Player|None) = None,
        stopping_player: (Player|None) = None,
    ):

        validate_type_list(players)
        validate_all_type_player(players)
        validate_not_empty_table(players)

        validate_type_int(min_bet)
        validate_int_positive(min_bet)

        if starting_player is None:
            starting_player = players[0]
        validate_type_player(starting_player)
        validate_player_in_table(starting_player, players)

        if stopping_player is None:
            starting_player_index = players.index(starting_player)
            stopping_player = players[starting_player_index - 1]
        validate_type_player(stopping_player)
        validate_player_in_table(stopping_player, players)

        self._players = players
        self._min_bet = min_bet
        self._min_raise_increase = min_bet
        self._starting_player = starting_player
        self._stopping_player = stopping_player
        self._current_player = starting_player

        self._bet_level = 0
        self._full_bet_level = 0
        self._central_pot: list[int] = [0]

        self._deck: list[Card] = [Card(value, suit) for value, suit in sorted_card_values_and_suits]
        self._common_cards: list[Card] = []


    @property
    def deck(self):
        "Cards still available to be dealt."
        return tuple(self._deck)

    @property
    def common_cards(self):
        "Cards dealt as common to all players."
        return tuple(self._common_cards)

    @property
    def players(self):
        "Players sitting at the table, in their respective order."
        return tuple(self._players)

    @property
    def live_players(self):
        "Players still playing for the pot during a hand cycle."
        return tuple(player for player in self._players if not player.is_folded)

    @property
    def actionable_players(self):
        "Players still playing for the pot and not all-in during a hand cycle."
        return tuple(
            player for player in self._players if not player.is_folded and player.stack > 0
        )

    @property
    def bettor_players(self):
        "Players who have placed chips in front to gather into the pot."
        return tuple(player for player in self.players if player.bet_level > 0)

    @property
    def starting_player(self):
        """
        Player who acts first in the betting round. Defaults to the first player in the players
        list.
        """
        return self._starting_player

    @property
    def stopping_player(self):
        """
        Player who acts last in the betting round. This may be updated during the betting round,
        depending on the actions taken by other players. Defaults to the player before the starting
        player.
        """
        return self._stopping_player

    @property
    def current_player(self):
        "Player who is being awaited to play. Defaults to the starting player."
        return self._current_player

    @property
    def bet_level(self):
        """
        Largest amount of chips a player has placed in front during the current betting round,
        which other players must match in order to call.
        """
        return self._bet_level

    @property
    def full_bet_level(self):
        """
        Part of the chip level matching the last full bet or raise. It may be smaller than a full bet
        when a player goes all-in for less. In that case, other players can complete the full bet
        (in addition to folding, calling or raising).
        """
        return self._full_bet_level

    @property
    def min_bet(self):
        "Minimum amount to bet."
        return self._min_bet

    @property
    def min_raise_increase(self):
        "Minimum amount by which to increase the full chip level."
        return self._min_raise_increase

    @property
    def pot(self):
        "Total amount of chips being played for in the betting round."
        return sum(self._central_pot) + sum(player.bet_level for player in self._players)

    @property
    def central_pot(self):
        "Part of the pot that is already placed at the center of the table, split into main and side pots."
        return tuple(self._central_pot)


    # Methods related to cards


    def remove_card_from_deck(self, card: Card):

        "Removes a card from the deck property."

        validate_type_card(card)
        validate_card_in_deck(card, self.deck)

        self._deck.remove(card)


    def reset_deck(self):

        "Resets the deck property back to have all the cards."

        self._deck.clear()
        self._deck.extend(Card(value, suit) for value, suit in sorted_card_values_and_suits)


    def assign_common_card(self, card: Card):

        "Adds a card to the common_cards property."

        validate_type_card(card)
        validate_iterable_not_contains_card(card, self.common_cards)

        self._common_cards.append(card)


    def reset_common_cards(self):

        "Clears the common_cards property."

        self._common_cards.clear()


    # Methods related to money


    def set_min_bet(self, amount: int):

        "Sets the min_bet property."

        validate_type_int(amount)
        validate_int_positive(amount)

        self._min_bet = amount


    def set_min_raise_increase(self, amount: int):

        "Sets the min_raise_increase property."

        validate_type_int(amount)
        validate_int_positive(amount)

        self._min_raise_increase = amount


    def set_bet_level(self, amount: int):

        "Sets the chip_level property."

        validate_type_int(amount)
        validate_int_positive_or_zero(amount)

        self._bet_level = amount


    def set_full_bet_level(self, amount: int):

        "Sets the full_chip_level property."

        validate_type_int(amount)
        validate_int_positive_or_zero(amount)

        self._full_bet_level = amount


    def increase_central_pot(self, amount: int):

        "Adds an amount to the central_pot property."

        validate_type_int(amount)
        validate_int_positive_or_zero(amount)

        self._central_pot[-1] += amount


    def add_side_pot(self):

        "Adds a new side pot to the central_pot property."

        self._central_pot.append(0)


    def clear_central_pot(self):

        "Resets the central_pot property."

        self._central_pot.clear()
        self._central_pot.append(0)


    # Methods related to players setting


    def set_starting_player(self, player: Player):

        "Sets the starting_player property."

        validate_type_player(player)
        validate_player_in_table(player, self.players)

        self._starting_player = player
    

    def set_stopping_player(self, player: Player):

        "Sets the stopping_player property."

        validate_type_player(player)
        validate_player_in_table(player, self.players)

        self._stopping_player = player


    def set_current_player(self, player: Player):

        "Sets a player as the current player."

        validate_type_player(player)
        validate_player_in_table(player, self.players)

        self._current_player = player


    # Methods related to players iteration


    def get_next_player(self, reference_player: Player):

        "Retrieves the player next to a reference player."

        validate_type_player(reference_player)
        validate_player_in_table(reference_player, self.players)

        if reference_player == self.players[-1]:
            return self.players[0]

        reference_player_index = self.players.index(reference_player)
        return self.players[reference_player_index + 1]


    def get_previous_player(self, reference_player: Player):

        "Retrieves the player before a reference player."

        validate_type_player(reference_player)
        validate_player_in_table(reference_player, self.players)

        reference_player_index = self.players.index(reference_player)
        return self.players[reference_player_index - 1]


    def iter_players(self, starting_player: (Player|None) = None, reverse: bool = False):

        "Iterates over all the players."

        if starting_player is None:
            starting_player = self.starting_player

        validate_type_player(starting_player)
        validate_player_in_table(starting_player, self.players)

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