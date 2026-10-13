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
from pokerpy.logger import logger, wrap_middle_log


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
    extra_big_blind_players = list(hand_cycle.extra_big_blind_players)

    if hand_cycle.big_blind:
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
        if hand_cycle.small_blind:
            place_small_blind(
                table = table,
                extra_big_blind_players = extra_big_blind_players,
                small_blind = hand_cycle.small_blind,
            )
        if hand_cycle.big_blind:
            place_big_blind(
                table = table,
                extra_big_blind_players = extra_big_blind_players,
                big_blind = hand_cycle.big_blind,
            )
            place_extra_big_blinds(
                table = table,
                extra_big_blind_players = extra_big_blind_players,
                big_blind = hand_cycle.big_blind,
            )
        hand_cycle.deal_cards_to_players(2)
        yield from betting_round.listen()

    hand_cycle.reset_betting_round()

    display_cards_and_money(table)
    logger.info(wrap_middle_log(f'ending {PREFLOP}', new_line=True))