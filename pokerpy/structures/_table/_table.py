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
from pokerpy.messages import (
    msg_no_players_in_table,
    msg_not_all_player_instances,
    msg_not_int,
    msg_not_list,
    msg_not_player_instance,
    msg_not_positive_value,
    msg_player_not_in_table,
)


from ._methods_related_to_cards import (
    method_assign_common_card,
    method_reset_common_cards,
    method_remove_card_from_deck,
    method_reset_deck,
)
from ._methods_related_to_money import (
    method_increase_central_pot,
    method_set_bet_level,
    method_set_full_bet_level,
    method_set_min_bet,
    method_set_min_raise_increase,
)
from ._methods_related_to_players_setting import (
    method_set_current_player,
    method_set_starting_player,
    method_set_stopping_player,
)
from ._methods_related_to_players_iteration import (
    method_get_next_player,
    method_get_previous_active_player,
    method_get_previous_player,
    method_iter_players,
)
from .._card import Card
from .._player import Player


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

        # Type validations

        if not isinstance(players, list):
            raise TypeError(msg_not_list.format(type(players).__name__))
        if not all(isinstance(player, Player) for player in players):
            raise TypeError(msg_not_all_player_instances)
        
        if not isinstance(min_bet, int):
            raise TypeError(msg_not_int.format(type(min_bet).__name__))
        
        if starting_player is not None and not isinstance(starting_player, Player):
            raise TypeError(msg_not_player_instance.format(type(starting_player).__name__))

        if stopping_player is not None and not isinstance(stopping_player, Player):
            raise TypeError(msg_not_player_instance.format(type(stopping_player).__name__))

        # Value validations

        if not players:
            raise ValueError(msg_no_players_in_table)

        if min_bet <= 0:
            raise ValueError(msg_not_positive_value.format(min_bet))

        if starting_player is None:
            starting_player = players[0]
        if starting_player not in players:
            raise ValueError(msg_player_not_in_table.format(starting_player.name))

        if stopping_player is None:
            starting_player_index = players.index(starting_player)
            stopping_player = players[starting_player_index - 1]
        if stopping_player not in players:
            raise ValueError(msg_player_not_in_table.format(stopping_player.name))

        # Assign attributes

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
        return method_remove_card_from_deck(self, card)


    def reset_deck(self):
        "Resets the deck property back to have all the cards."
        return method_reset_deck(self)


    def assign_common_card(self, card: Card):
        "Adds a card to the common_cards property."
        return method_assign_common_card(self, card)


    def reset_common_cards(self):
        "Clears the common_cards property."
        return method_reset_common_cards(self)


    # Methods related to money


    def set_min_bet(self, amount: int):
        "Sets the min_bet property."
        return method_set_min_bet(self, amount)


    def set_min_raise_increase(self, amount: int):
        "Sets the min_raise_increase property."
        return method_set_min_raise_increase(self, amount)


    def set_bet_level(self, amount: int):
        "Sets the chip_level property."
        return method_set_bet_level(self, amount)


    def set_full_bet_level(self, amount: int):
        "Sets the full_chip_level property."
        return method_set_full_bet_level(self, amount)


    def increase_central_pot(self, amount: int):
        "Adds an amount to the central_pot property."
        return method_increase_central_pot(self, amount)


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
        return method_set_starting_player(self, player)
    

    def set_stopping_player(self, player: Player):
        "Sets the stopping_player property."
        return method_set_stopping_player(self, player)


    def set_current_player(self, player: Player):
        "Sets a player as the current player."
        return method_set_current_player(self, player)


    # Methods related to players iteration


    def get_next_player(self, reference_player: Player):
        "Retrieves the player next to a reference player."
        return method_get_next_player(self, reference_player)


    def get_previous_player(self, reference_player: Player):
        "Retrieves the player before a reference player."
        return method_get_previous_player(self, reference_player)


    def iter_players(self, starting_player: (Player|None) = None, reverse: bool = False):
        "Iterates over all the players."
        return method_iter_players(self, starting_player, reverse)


    def get_previous_active_player(self, reference_player: Player):
        "Retrieves the player before a reference player that is not either folded or all-in."
        return method_get_previous_active_player(self, reference_player)
