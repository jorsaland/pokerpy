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
Defines the class that represents a betting round context manager.
"""


from collections.abc import Generator


from pokerpy.logger import get_logger
from pokerpy.messages import (
    msg_not_all_player_instances,
    msg_not_int,
    msg_not_list,
    msg_not_player_instance,
    msg_not_positive_value,
    msg_not_str,
    msg_not_table_instance,
    msg_betting_round_was_not_completed,
    msg_overloaded_betting_round_message,
    msg_some_players_not_in_table,
)
from pokerpy.structures import Player, Table


from ._methods_to_affect_money import method_overwrite_smallest_raise_amount
from ._methods_to_affect_players import method_set_stopping_player
from ._methods_to_deal_cards import method_deal_cards_to_players, method_deal_common_cards
from ._run_listener import run_listener


logger = get_logger()


class BettingRound:


    """
    Represents a betting round context manager.
    """


    def __init__(
        self,
        name: str,
        table: Table,
        *,
        smallest_bet: int = 1,
        starting_player: (Player|None) = None,
        stopping_player: (Player|None) = None,
        open_fold_allowed = False,
        ignore_invalid_actions = True
    ):

        # Validations

        if not isinstance(name, str):
            raise TypeError(msg_not_str.format(type(name).__name__))

        if not isinstance(table, Table):
            raise TypeError(msg_not_table_instance.format(type(table).__name__))

        if not isinstance(smallest_bet, int):
            raise TypeError(msg_not_int.format(type(smallest_bet).__name__))
        if smallest_bet <= 0:
            raise ValueError(msg_not_positive_value.format(smallest_bet))

        if starting_player is None:
            starting_player = table.players[0]
        else:
            if not isinstance(starting_player, Player):
                raise TypeError(msg_not_player_instance.format(type(starting_player).__name__))

        if stopping_player is None:
            stopping_player = table.get_previous_player(starting_player)
        else:
            if not isinstance(stopping_player, Player):
                raise TypeError(msg_not_player_instance.format(type(stopping_player).__name__))

        # Fixed variables

        self._listener: (Generator[Player]|None) = None

        self._name = name
        self._table = table

        self._smallest_bet = smallest_bet
        self._starting_player = starting_player

        self.open_fold_allowed = open_fold_allowed # editable, hopefully boolean but not enforced
        self._ignore_invalid_actions = bool(ignore_invalid_actions)

        # State variables

        self._lap_counts = 0
        self._is_completed = False
        self._smallest_raise_amount = smallest_bet
        self._stopping_player = stopping_player


    @property
    def name(self):
        return self._name

    @property
    def table(self):
        return self._table

    @property
    def lap_counts(self):
        return self._lap_counts

    @property
    def starting_player(self):
        return self._starting_player

    @property
    def stopping_player(self):
        return self._stopping_player

    @property
    def smallest_bet(self):
        return self._smallest_bet

    @property
    def smallest_raise_amount(self):
        return self._smallest_raise_amount

    @property
    def is_completed(self):
        return self._is_completed

    @property
    def ignore_invalid_actions(self):
        return self._ignore_invalid_actions


    def __enter__(self):
        self.listen()
        return self


    def __exit__(self, exception_type: (type|None), exception: (BaseException|None), _):

        if exception_type is StopIteration:
            self._is_completed = True
            exception = RuntimeError(msg_overloaded_betting_round_message)

        self.close(exception)


    # Methods to control the listener


    def listen(self):

        """
        Starts and retrieves the generator object that listens for player actions.
        """

        if self._listener is None:
            self.table.reset_betting_round_states()
            self._listener = run_listener(self)
        return self._listener


    def close(self, exception: (BaseException|None) = None):

        """
        Runs the last step in the betting round.
        """

        # End running iteration after last yield
        try:
            if not self.is_completed:
                next(self.listen())
        except StopIteration:
            self._is_completed = True
        finally:
            self.table.reset_betting_round_states()

        # Raise catched exceptions
        if exception is not None:
            raise exception

        # Validate the listener has ended
        if not self.is_completed:
            logger.critical('====== THE BETTING ROUND WAS CLOSED BEFORE ENDING ======')
            raise RuntimeError(msg_betting_round_was_not_completed)


    # Methods to affect counter


    def increase_counter(self):

        """
        Registers a new lap.
        """

        self._lap_counts += 1


    # Methods to affect players


    def set_stopping_player(self, player: Player):

        """
        Marks the player before whom the betting round is closed.
        """

        return method_set_stopping_player(self, player)
    

    # Methods to affect money


    def overwrite_smallest_raise_amount(self, amount: int):

        """
        Overwrites the smallest amount expected to make a raise.
        """

        return method_overwrite_smallest_raise_amount(self, amount)
    

    # Methods to deal cards

    
    def deal_cards_to_players(self, cards_count: int):

        """
        Deals cards to players in equal amounts.
        """

        return method_deal_cards_to_players(self, cards_count)


    def deal_common_cards(self, cards_count: int):

        """
        Deals common cards to table.
        """

        return method_deal_common_cards(self, cards_count)