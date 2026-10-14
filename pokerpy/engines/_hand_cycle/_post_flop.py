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
Defines the function that runs the betting round for the flop, turn or river.
"""


from typing import TYPE_CHECKING


from pokerpy.constants import FLOP
from pokerpy.logger import logger, wrap_internal_log, wrap_middle_log
from pokerpy.structures import Table


from .._betting_round._betting_round import BettingRound

from ._assign_hand import assign_hand
from ._display_status import display_cards_and_money

if TYPE_CHECKING:
    from ._hand_cycle import HandCycle


def post_flop(hand_cycle: "HandCycle", round_name: str):

    """
    Runs the betting round for the flop, turn or river. Returns a boolean value indicating if the
    round should keep going or not.
    """

    table = hand_cycle.table

    assert table.button_player is not None
    assert len(table.live_players) > 1

    logger.info(wrap_middle_log(f'starting {round_name}'))

    starting_player = table.get_next_player(table.button_player)
    table.set_starting_player(starting_player)

    betting_round = BettingRound(
        name = round_name,
        table = table,
        open_fold_allowed = hand_cycle.open_fold_allowed,
        raise_invalid_actions = hand_cycle.raise_invalid_actions,
    )

    with betting_round:

        hand_cycle.set_betting_round(betting_round)

        logger.info(wrap_internal_log())

        # Deal three cards to table if round is flop and one if is turn or river

        if round_name == FLOP:
            hand_cycle.deal_common_cards(3)        
        else:
            hand_cycle.deal_common_cards(1)

        for player in table.players:
            assign_hand(player=player, common_cards=table.common_cards)

        # Let players to play
        yield from betting_round.listen()

    hand_cycle.reset_betting_round()

    display_cards_and_money(table)
    logger.info(wrap_middle_log(f'ending {round_name}', new_line=True))