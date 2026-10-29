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


from pokerpy.logger import logger, wrap_internal_log, wrap_external_log
from pokerpy.messages import (
    msg_hand_cycle_was_not_completed,
    msg_overloaded_hand_cycle,
)
from pokerpy.structures import Player, Table
from pokerpy.validations import (
    validate_int_positive,
    validate_type_int,
    validate_type_str,
    validate_type_table,
)


from .._betting_round._betting_round import BettingRound
from ._run_listener import run_listener


class HandCycle:


    """
    Represents a Texas Hold'em hand cycle.
    """


    def __init__(
        self,
        name: str,
        table: Table,
        *,
        open_fold_allowed = False,
        raise_invalid_actions = False
    ):

        # Type validations
        validate_type_str(name)
        validate_type_table(table)

        # Fixed attributes
        self._listener: (Generator[Player]|None) = None
        self._name = name
        self._table = table
        self._open_fold_allowed = bool(open_fold_allowed)
        self._raise_invalid_actions = bool(raise_invalid_actions)

        # State attributes
        self._betting_round: (BettingRound|None) = None
        self._in_extra_big_blinds_phase = False
        self._is_completed = False


    @property
    def name(self):
        "Hand cycle's identifier, unique within the game."
        return self._name

    @property
    def table(self):
        "Table in which the hand cycle takes place."
        return self._table

    @property
    def betting_round(self):
        "Betting round taking place."
        return self._betting_round

    @property
    def in_extra_big_blinds_phase(self):
        "Whether the betting round is in the phase of placing extra big blinds"
        return self._in_extra_big_blinds_phase

    @property
    def is_completed(self):
        "Whether the betting round already ended."
        return self._is_completed

    @property
    def open_fold_allowed(self):
        "Whether folding is allowed when there is no bet or raise to respond to."
        return self._open_fold_allowed

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
            exception = RuntimeError(msg_overloaded_hand_cycle)
        self.close(exception)


    # Methods to control the listener


    def listen(self):

        "Starts and retrieves the generator object that listens for player actions."

        if self._listener is None:
            self.reset_hand_cycle_states(self.table)
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
            self.reset_betting_round()
            self.unmark_in_extra_big_blinds_phase()
            self.reset_hand_cycle_states(self.table)

        # Raise catched exceptions
        if exception is not None:
            raise exception

        # Validate the listener has ended
        if not self.is_completed:
            logger.critical(wrap_external_log('the hand cycle was closed before ending'))
            raise RuntimeError(msg_hand_cycle_was_not_completed)


    # Methods to deal cards

    
    def deal_cards_to_players(self, cards_count: int):

        "Deals cards to players in equal amounts."

        validate_type_int(cards_count)
        validate_int_positive(cards_count)

        for _ in range(cards_count):
            for player in self.table.live_players:
                card = secrets.choice(self.table.deck)
                self.table.remove_card_from_deck(card)
                player.assign_card(card)
                logger.info(f'Dealer deals card {card} to {player.name}.')

        logger.info(wrap_internal_log())


    def deal_common_cards(self, cards_count: int):

        "Deals common cards to table."

        validate_type_int(cards_count)
        validate_int_positive(cards_count)

        for _ in range(cards_count):
            card = secrets.choice(self.table.deck)
            self.table.remove_card_from_deck(card)
            self.table.assign_common_card(card)
        
        logger.info(f'Dealer deals common cards: {"".join(str(card) for card in self.table.common_cards[-cards_count:])}.')
        logger.info(wrap_internal_log())


    # Methods related to state


    def set_betting_round(self, betting_round: BettingRound):
        "Sets a betting round as the current one."
        self._betting_round = betting_round


    def reset_betting_round(self):
        "Resets current betting round."
        self._betting_round = None


    def mark_in_extra_big_blinds_phase(self):
        "Marks the hand cycle as in the phase of placing extra big blinds."
        self._in_extra_big_blinds_phase = True

    def unmark_in_extra_big_blinds_phase(self):
        "Unmarks the hand cycle as in the phase of placing extra big blinds."
        self._in_extra_big_blinds_phase = False


    @staticmethod
    def reset_hand_cycle_states(table: Table):

        "Resets the states for a table and its players to prepare them for a new betting round."

        validate_type_table(table)

        BettingRound.reset_betting_round_states(table)

        table.reset_deck()
        table.reset_common_cards()
        table.clear_central_pot()

        for player in table.players:
            player.reset_cards()
            player.clear_hand()
            player.reset_pot_index()
            player.unmark_is_folded()
            player.unmark_is_extra_blind()