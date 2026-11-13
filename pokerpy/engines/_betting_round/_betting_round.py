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


from pokerpy.logger import logger, wrap_external_log
from pokerpy.messages import (
    msg_betting_round_was_not_completed,
    msg_missing_action,
    msg_overloaded_betting_round,
)
from pokerpy.structures import Table
from pokerpy.validations import validate_type_str, validate_type_table


from ._run_listener import run_listener


class BettingRound:


    """
    Represents a betting round context manager.
    """


    def __init__(self, name: str, table: Table, *, open_fold_allowed=False):

        validate_type_str(name)
        validate_type_table(table)

        self._listener = None
        self._name = name
        self._table = table
        self._open_fold_allowed = bool(open_fold_allowed)

        self._lap_counts = 0
        self._is_completed = False
        self._is_closed = False


    def __enter__(self):

        self.listen()
        return self


    def __exit__(self, exception_type: (type|None), exception_value: (BaseException|None), _):

        if exception_type is None:
            self.close()
            return

        # Closes the listener generator on the abort path. If an exception is raised on the
        # caller's side (for example in a state method such as deal_cards), the generator stays
        # suspended at yield and its nested with blocks do not unwind. Their cleanup would then run
        # at garbage collection or interpreter shutdown, when imports no longer work, producing a
        # misleading "ImportError: sys.meta_path is None" that hides the real error. Generator's
        # method close() throws GeneratorExit through every `yield from`, so the cleanup runs here,
        # deterministically. It is a harmless if the generator has already finished.
        self._listener.close()
        self._teardown()

        if exception_type is StopIteration:
            raise RuntimeError(msg_overloaded_betting_round) from exception_value


    def _increase_counter(self):
        "Registers a new lap."
        self._lap_counts += 1

    def _mark_is_completed(self):
        "Mark round as completed."
        self._is_completed = True

    def _teardown(self):
        "Cleans up the betting round."
        self.reset_betting_round_states(self.table)
        self._is_closed = True


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
    def is_completed(self):
        "Whether the betting round generator reached the end."
        return self._is_completed

    @property
    def is_closed(self):
        "Whether the betting round was closed."
        return self._is_closed

    @property
    def open_fold_allowed(self):
        "Whether folding is allowed when there is no bet or raise to respond to."
        return self._open_fold_allowed


    def listen(self):

        "Starts and retrieves the generator object that listens for player actions."

        if self._listener is None:
            self.reset_betting_round_states(self.table)
            self._listener = run_listener(self)

        return self._listener


    def close(self):

        "Runs the last step in the betting round."

        if self.is_closed:
            return

        try:
            if not self.is_completed:
                next(self.listen())
        except StopIteration:
            pass
        except RuntimeError as exception:
            if exception.args[0] == msg_missing_action:
                raise RuntimeError(msg_betting_round_was_not_completed) # closure after skipping parsing prefers this message
            raise exception
        finally:
            self._teardown()

        if not self.is_completed:
            logger.critical(wrap_external_log('the betting round was closed before ending'))
            raise RuntimeError(msg_betting_round_was_not_completed)


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
