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
Defines the function that starts the hand cycle generator that rotates the player turns.
"""


from typing import TYPE_CHECKING


from pokerpy.constants import PREFLOP
from pokerpy.logger import logger, wrap_middle_log, wrap_internal_log


from .._betting_round._betting_round import BettingRound

from ._display_status import display_cards_and_money
from ._place_big_blind import place_big_blind
from ._place_extra_big_blinds import place_extra_big_blinds
from ._place_small_blind import place_small_blind
if TYPE_CHECKING:
    from ._hand_cycle import HandCycle


def pre_flop(hand_cycle: "HandCycle"):

    "Runs the pre-flop betting round."

    logger.info(wrap_middle_log(f'starting {PREFLOP}'))

    table = hand_cycle.table

    assert table.button_player is not None

    if table.big_blind:
        assert table.big_blind_player
        starting_player = table.get_next_player(table.big_blind_player)
    else:
        starting_player = table.get_next_player(table.button_player)
    table.set_starting_player(starting_player)

    betting_round = BettingRound(
        name = PREFLOP,
        table = table,
        open_fold_allowed = hand_cycle.open_fold_allowed,
        raise_invalid_actions = hand_cycle.raise_invalid_actions,
    )

    with betting_round:

        hand_cycle.set_betting_round(betting_round)

        logger.info(wrap_internal_log())

        optional_blind_eligible_players = list(table.actionable_players)

        if table.big_blind:

            assert table.big_blind_player

            if table.small_blind:
                assert table.small_blind_player
                if table.small_blind_player in optional_blind_eligible_players:
                    optional_blind_eligible_players.remove(table.small_blind_player)
                place_small_blind(table.small_blind, table.small_blind_player)

            if table.big_blind_player in optional_blind_eligible_players:
                optional_blind_eligible_players.remove(table.big_blind_player)
            place_big_blind(table.big_blind, table.big_blind_player)
 
            hand_cycle.mark_in_extra_big_blinds_phase()
            yield from place_extra_big_blinds(table.big_blind, optional_blind_eligible_players)
            hand_cycle.unmark_in_extra_big_blinds_phase()
 
            table.set_bet_level(table.big_blind)
            table.set_full_bet_level(table.big_blind)

        logger.info(f'TABLE CURRENT LEVEL: {table.bet_level}')
        logger.info(wrap_internal_log())

        hand_cycle.deal_cards_to_players(2)
        yield from betting_round.listen()

    hand_cycle.reset_betting_round()

    display_cards_and_money(table)
    logger.info(wrap_middle_log(f'ending {PREFLOP}', new_line=True))