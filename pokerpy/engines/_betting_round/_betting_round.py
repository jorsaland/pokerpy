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
    msg_not_str,
    msg_not_table_instance,
    msg_betting_round_was_not_completed,
    msg_overloaded_betting_round_message,
)
from pokerpy.structures import Player, Table


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
        smallest_bet_amount: (int|None) = None,
        starting_player: (Player|None) = None,
        stopping_player: (Player|None) = None,
        open_fold_allowed = False,
        ignore_invalid_actions = True
    ):

        # Type validations

        if not isinstance(name, str):
            raise TypeError(msg_not_str.format(type(name).__name__))

        if not isinstance(table, Table):
            raise TypeError(msg_not_table_instance.format(type(table).__name__))

        # Fixed variables

        self._listener: (Generator[Player]|None) = None

        self._name = name
        self._table = table

        self.open_fold_allowed = open_fold_allowed # editable, hopefully boolean but not enforced
        self._ignore_invalid_actions = bool(ignore_invalid_actions)

        # State variables

        self._lap_counts = 0
        self._is_completed = False

        if smallest_bet_amount is not None:
            table.set_full_bet(smallest_bet_amount)

        if starting_player is not None:
            table.set_starting_player(starting_player)

        if stopping_player is None:
            stopping_player = table.get_previous_player(table.starting_player)
        table.set_stopping_player(stopping_player)


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
            self.reset_betting_round_states(self.table)
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
            self.reset_betting_round_states(self.table)

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
    

    # Methods to reset states


    @staticmethod
    def reset_betting_round_states(table: Table):

        """
        Resets the states for a table and its players to prepare them for a new betting round.
        """

        if not isinstance(table, Table):
            raise TypeError(msg_not_table_instance.format(type(table).__name__))

        table.set_full_raise_increase(table.full_bet)
        table.set_current_level(0)
        table.set_complete_current_level(0)
        table.set_stopping_player(table.get_previous_player(table.starting_player))

        for player in table.players:
            player.unset_as_played()
            player.reset_action()
            player.reset_current_amount()