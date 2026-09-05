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
import secrets


from pokerpy.logger import get_logger
from pokerpy.messages import (
    msg_betting_round_was_not_completed,
    msg_overloaded_betting_round_message,
)
from pokerpy.structures import Player, Table
from pokerpy.validations import validate_type_int, validate_type_str, validate_type_table


from ._get_valid_actions import get_valid_actions
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
        raise_invalid_actions = False
    ):

        validate_type_str(name)
        validate_type_table(table)

        # Fixed variables
        self._listener: (Generator[Player]|None) = None
        self._name = name
        self._table = table
        self._open_fold_allowed = bool(open_fold_allowed)
        self._raise_invalid_actions = bool(raise_invalid_actions)

        # State variables
        self._lap_counts = 0
        self._is_completed = False

        if smallest_bet_amount is not None:
            table.set_min_bet(smallest_bet_amount)
            table.set_min_raise_increase(smallest_bet_amount)

        if starting_player is not None:
            table.set_starting_player(starting_player)

        if stopping_player is None:
            stopping_player = table.get_previous_player(table.starting_player)
        table.set_stopping_player(stopping_player)


    @property
    def name(self):
        "Betting round's identifier, unique within the hand cycle."
        return self._name

    @property
    def table(self):
        "Table in which the betting round takes place."
        return self._table

    @property
    def lap_counts(self):
        "Number of times the action passes through the starting player (even if folded or all-in)."
        return self._lap_counts

    @property
    def open_fold_allowed(self):
        "Whether folding is allowed when there is no bet or raise to respond to."
        return self._open_fold_allowed

    @open_fold_allowed.setter
    def open_fold_allowed(self, open_fold_allowed):
        self._open_fold_allowed = bool(open_fold_allowed)

    @property
    def is_completed(self):
        "Whether the betting round already ended."
        return self._is_completed

    @property
    def raise_invalid_actions(self):
        """
        Whether an exception should be raised when an invalid action is chosen, or the player
        should be prompted again.
        """
        return self._raise_invalid_actions


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

        "Starts and retrieves the generator object that listens for player actions."

        if self._listener is None:
            self.reset_betting_round_states(self.table)
            self._listener = run_listener(self)
        return self._listener


    def close(self, exception: (BaseException|None) = None):

        "Runs the last step in the betting round."

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


    # Methods to deal cards

    
    def deal_cards_to_players(self, cards_count: int):

        "Deals cards to players in equal amounts."

        validate_type_int(cards_count)

        for _ in range(cards_count):
            for player in self.table.live_players:
                card = secrets.choice(self.table.deck)
                self.table.remove_card_from_deck(card)
                player.assign_card(card)
                logger.info(f'Dealer deals card {card} to {player.name}.')


    def deal_common_cards(self, cards_count: int):

        "Deals common cards to table."

        validate_type_int(cards_count)

        for _ in range(cards_count):
            card = secrets.choice(self.table.deck)
            self.table.remove_card_from_deck(card)
            self.table.assign_common_card(card)
        
        logger.info(f'Dealer deals common cards: {"".join(str(card) for card in self.table.common_cards[-cards_count:])}.')
    

    # Methods related to state


    def get_action_ranges(self):

        "Retrieves the current player and its available actions"

        return get_valid_actions(
            player_stack = self.table.current_player.stack,
            player_bet_level = self.table.current_player.bet_level,
            player_has_played = self.table.current_player.has_played,
            bet_level = self.table.bet_level,
            full_bet_level = self.table.full_bet_level,
            min_bet = self.table.min_bet,
            min_raise_increase = self.table.min_raise_increase,
            is_last_actionable_player = (
                self.table.current_player in self.table.actionable_players
                and len(self.table.actionable_players) == 1
            ),
            open_fold_allowed = self.open_fold_allowed,
        )


    def increase_counter(self):

        "Registers a new lap."

        self._lap_counts += 1


    @staticmethod
    def reset_betting_round_states(table: Table):

        "Resets the states for a table and its players to prepare them for a new betting round."

        validate_type_table(table)

        table.set_min_raise_increase(table.min_bet)
        table.set_bet_level(0)
        table.set_full_bet_level(0)
        table.set_stopping_player(table.get_previous_player(table.starting_player))

        for player in table.players:
            player.unmark_has_played()
            player.clear_action()