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


"Defines the function that starts the hand cycle generator that rotates the player turns."


from typing import TYPE_CHECKING


from pokerpy.constants import after_preflop_round_names
from pokerpy.logger import logger, wrap_external_log, wrap_middle_log


from ._ante_round import ante_round
from ._display_status import display_pot_indexes
from ._pre_flop import pre_flop
from ._post_flop import post_flop
from ._showdown import showdown

if TYPE_CHECKING:
    from ._hand_cycle import HandCycle


def run_hand_cycle_listener(hand_cycle: "HandCycle"):

    "Starts the hand cycle generator that rotates the player turns."

    logger.info(wrap_external_log(f'starting hand cycle {hand_cycle.name}', new_line=True))

    hand_cycle.table.set_min_bet(hand_cycle.big_blind)

    if hand_cycle.ante:
        ante_round(hand_cycle.table, ante=hand_cycle.ante)

    yield from pre_flop(
        hand_cycle = hand_cycle,
        table = hand_cycle.table,
        small_blind = hand_cycle.small_blind,
        big_blind = hand_cycle.big_blind,
        extra_big_blind_players = hand_cycle.extra_big_blind_players,
        open_fold_allowed = hand_cycle.open_fold_allowed,
        raise_invalid_actions = hand_cycle.raise_invalid_actions,
    )

    for round_name in after_preflop_round_names:
        keep_playing = yield from post_flop(
            hand_cycle = hand_cycle,
            table = hand_cycle.table,
            round_name = round_name,
            open_fold_allowed = hand_cycle.open_fold_allowed,
            raise_invalid_actions = hand_cycle.raise_invalid_actions,
        )
        if not keep_playing:
            break

    if len(hand_cycle.table.live_players) > 1:
        logger.info(wrap_middle_log('showdown'))
        display_pot_indexes(hand_cycle.table)
        showdown(hand_cycle.table)
    else:
        logger.info(wrap_middle_log('no showdown'))
        display_pot_indexes(hand_cycle.table)
        showdown(hand_cycle.table)
    logger.info(wrap_middle_log(new_line=True))

    logger.info(wrap_external_log(f'ending hand cycle {hand_cycle.name}', new_line=True))