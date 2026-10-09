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


from itertools import combinations
from typing import TYPE_CHECKING


from pokerpy.constants import PREFLOP, FLOP, after_preflop_round_names
from pokerpy.logger import (
    get_logger,
    wrap_external_log,
    wrap_internal_log,
    wrap_middle_log,
)
from pokerpy.structures import Card, Hand, Player, Table


from .._betting_round._betting_round import BettingRound
from .._betting_round._gather_pot import gather_pot

from ._showdown import showdown

if TYPE_CHECKING:
    from ._hand_cycle import HandCycle


logger = get_logger()


def assign_hands(table: Table):

    "Assigns the hands to the players."

    for player in table.players:

        cards = player.cards + table.common_cards
    
        if len(cards) < 5:
            continue
        
        if len(cards) == 5:
            hand = Hand(cards)
        else:
            hand = max(Hand(combination) for combination in combinations(cards, 5))

        player.assign_hand(hand)


def display_cards_and_money(table: Table):

    "Displays info logs with the current status of cards and money."

    logger.info(wrap_internal_log())
    logger.info(f'Common cards: {"".join(str(c) for c in table.common_cards) if table.common_cards else None} | pot: {table.pot} | divided pot: {list(table.split_central_pot)}')

    max_name_length = max(len(player.name) for player in table.players)
    max_stack_length = max(len(str(player.stack)) for player in table.players)

    for player in table.players:
        logger.info(
            f"{'(F)' if player.is_folded else '   '} {player.name.ljust(max_name_length)} | "
            f"cards: {''.join(str(c) for c in player.cards) if player.cards else 'N/A'} | "
            f"stack: {str(player.stack).ljust(max_stack_length)} | "
            f"hand: {f'{str(player.hand)} {player.hand.category}' if player.hand is not None else 'N/A'}"
        )
    logger.info(wrap_internal_log())


def display_pot_indexes(table: Table):

    "Displays info logs with the current status of the split pot."

    logger.info(wrap_internal_log())

    for pot_index, pot in enumerate(table.split_central_pot):
        logger.info(f"{'Main pot' if pot_index == 0 else f'Side pot {pot_index}'} ({pot}):")
        for player in table.live_players:
            if player.pot_index >= pot_index:
                logger.info(f"  {player.name}: hand: {f'{str(player.hand)} {player.hand.category}' if player.hand is not None else 'N/A'}")

    logger.info(wrap_internal_log())


def ante_round(table: Table, *, ante: int):

    "Runs the round where all players place antes."

    logger.info(wrap_middle_log('placing antes'))

    logger.info(f'Ante size: {ante}')
    for player in table.players:
        amount = ante if player.stack > ante else player.stack
        player.decrease_stack(amount)
        player.increase_bet_level(amount)

    gather_pot(table)
    display_cards_and_money(table)
    logger.info(wrap_middle_log('antes placed', new_line=True))


def preflop(
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


def postflop(
    hand_cycle: "HandCycle",
    table: Table,
    round_name: str,
    open_fold_allowed: bool,
    raise_invalid_actions: bool,
):

    "Runs the betting round for the flop, turn or river"

    # Break before starting if only remains one player
    if len(table.live_players) == 1:
        return False

    logger.info(wrap_middle_log(f'starting {round_name}'))

    betting_round = BettingRound(
        name = round_name,
        table = table,
        open_fold_allowed = open_fold_allowed,
        raise_invalid_actions = raise_invalid_actions,
    )

    with betting_round:

        hand_cycle.set_current_betting_round(betting_round)

        # Deal three cards to table if round is flop and one if is turn or river

        if round_name == FLOP:
            hand_cycle.deal_common_cards(3)        
        else:
            hand_cycle.deal_common_cards(1)
        assign_hands(table)

        # Let players to play
        yield from betting_round.listen()

    hand_cycle.reset_current_betting_round()

    display_cards_and_money(table)
    logger.info(wrap_middle_log(f'ending {round_name}', new_line=True))

    return True


def run_listener(hand_cycle: "HandCycle"):

    "Starts the hand cycle generator that rotates the player turns."

    logger.info(wrap_external_log(f'starting hand cycle {hand_cycle.name}', new_line=True))

    hand_cycle.table.set_min_bet(hand_cycle.big_blind)

    if hand_cycle.ante:
        ante_round(hand_cycle.table, ante=hand_cycle.ante)

    yield from preflop(
        hand_cycle = hand_cycle,
        table = hand_cycle.table,
        small_blind = hand_cycle.small_blind,
        big_blind = hand_cycle.big_blind,
        extra_big_blind_players = hand_cycle.extra_big_blind_players,
        open_fold_allowed = hand_cycle.open_fold_allowed,
        raise_invalid_actions = hand_cycle.raise_invalid_actions,
    )

    for round_name in after_preflop_round_names:
        keep_playing = yield from postflop(
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