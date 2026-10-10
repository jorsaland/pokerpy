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
from pokerpy.logger import logger, wrap_internal_log, wrap_middle_log
from pokerpy.structures import Player, Table


from .._betting_round._betting_round import BettingRound

from ._display_status import display_cards_and_money

if TYPE_CHECKING:
    from ._hand_cycle import HandCycle


def pre_flop(
    *,
    hand_cycle: "HandCycle",
    table: Table,
    small_blind: (int|None),
    big_blind: (int|None),
    extra_big_blind_players: tuple[Player],
    open_fold_allowed: bool,
    raise_invalid_actions: bool,
):

    "Runs the pre-flop betting round."

    logger.info(wrap_middle_log(f'starting {PREFLOP}'))

    if small_blind and big_blind:
        table.set_starting_player(table.players[2])
    elif big_blind:
        table.set_starting_player(table.players[1])
    else:
        table.set_starting_player(table.players[0])

    betting_round = BettingRound(
        name = PREFLOP,
        table = table,
        open_fold_allowed = open_fold_allowed,
        raise_invalid_actions = raise_invalid_actions,
    )

    with betting_round:

        hand_cycle.set_current_betting_round(betting_round)

        if small_blind:

            small_blind_player = table.players[0]

            if not small_blind_player.stack:
                logger.info(f"{small_blind_player.name} IS ALL-IN, CANNOT PLACE SMALL BLIND")
            if small_blind_player.stack:
                amount = small_blind if small_blind_player.stack > small_blind else small_blind_player.stack
                small_blind_player.decrease_stack(amount)
                small_blind_player.increase_bet_level(amount)
                logger.info(
                    f"{small_blind_player.name} PLACES SMALL BLIND {amount} "
                    f"({small_blind_player.name}'s bet level: {small_blind_player.bet_level} | stack: {small_blind_player.stack})"
                    ""
                )

        if big_blind:

            big_blind_player = table.players[1]

            if not big_blind_player.stack:
                logger.info(f"{big_blind_player.name} IS ALL-IN, CANNOT PLACE BIG BLIND")
            else:
                amount = big_blind if big_blind_player.stack > big_blind else big_blind_player.stack
                big_blind_player.decrease_stack(amount)
                big_blind_player.increase_bet_level(amount)
                logger.info(
                    f"{big_blind_player.name} PLACES BIG BLIND {amount} "
                    f"({big_blind_player.name}'s bet level: {big_blind_player.bet_level} | stack: {big_blind_player.stack})"
                )

            table.set_bet_level(big_blind)
            table.set_full_bet_level(big_blind)
            logger.info(f'TABLE CURRENT LEVEL: {table.bet_level}')

        for player in extra_big_blind_players:

            if player in table.players[:2]:
                continue

            amount = big_blind if player.stack > big_blind else player.stack
            player.decrease_stack(amount)
            player.increase_bet_level(amount)
            logger.info(
                f"{player.name} PLACES OPTIONAL BIG BLIND {amount} "
                f"({player.name}'s bet level: {player.bet_level} | stack: {player.stack})"
            )
            logger.info(f'TABLE CURRENT LEVEL: {table.bet_level}')
            logger.info(wrap_internal_log())

        hand_cycle.deal_cards_to_players(2)

        yield from betting_round.listen()

    hand_cycle.reset_current_betting_round()

    display_cards_and_money(table)
    logger.info(wrap_middle_log(f'ending {PREFLOP}', new_line=True))