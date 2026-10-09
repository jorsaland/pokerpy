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
from pokerpy.logger import get_logger
from pokerpy.structures import Card, Hand, Player, Table


from .._betting_round._betting_round import BettingRound
from .._betting_round._gather_pot import gather_pot

from ._showdown import showdown

if TYPE_CHECKING:
    from ._hand_cycle import HandCycle


logger = get_logger()


def figure_out_hand(cards: list[Card]):
    
    if len(cards) < 5:
        return None
    
    if len(cards) == 5:
        return Hand(cards)
    
    possible_hands = [Hand(combination) for combination in combinations(cards, 5)]
    return max(possible_hands)


def display_cards_and_money(table: Table):
    print('\n--------------------------------------------------')
    print(f'Common cards: {"".join(str(c) for c in table.common_cards) if table.common_cards else None} | pot: {table.pot} | divided pot: {list(table.split_central_pot)}')
    for player in table.live_players:
        hand = figure_out_hand(player.cards + table.common_cards)
        if hand is not None:
            player.assign_hand(hand)
        print(
            f"{player.name}'s cards: {''.join(str(c) for c in player.cards) if player.cards else None} | "
            f"hand: {f'{str(player.hand)} ({player.hand.category})' if player.hand is not None else None} | "
            f"stack: {player.stack} | bet level: {player.bet_level}"
        )
    print('--------------------------------------------------\n')


def ante_round(table: Table, *, ante: int):

    print(f'\n============ PLACING ANTES ============\n')

    print(f'Ante size: {ante}')
    for player in table.players:
        amount = ante if player.stack > ante else player.stack
        player.decrease_stack(amount)
        player.increase_bet_level(amount)

    gather_pot(table)
    display_cards_and_money(table)
    print(f'\n============ ANTES PLACED ============\n')


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

    print(f'\n============ STARTING {PREFLOP.upper()} ============\n')

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
                print(f"{small_blind_player.name} IS ALL-IN, CANNOT PLACE SMALL BLIND\n")
            if small_blind_player.stack:
                amount = small_blind if small_blind_player.stack > small_blind else small_blind_player.stack
                small_blind_player.decrease_stack(amount)
                small_blind_player.increase_bet_level(amount)
                print(
                    f"{small_blind_player.name} PLACES SMALL BLIND {amount} "
                    f"({small_blind_player.name}'s bet level: {small_blind_player.bet_level} | stack: {small_blind_player.stack})"
                    "\n"
                )

        if big_blind:

            big_blind_player = table.players[1]

            if not big_blind_player.stack:
                print(f"{big_blind_player.name} IS ALL-IN, CANNOT PLACE BIG BLIND\n")
            else:
                amount = big_blind if big_blind_player.stack > big_blind else big_blind_player.stack
                big_blind_player.decrease_stack(amount)
                big_blind_player.increase_bet_level(amount)
                print(
                    f"{big_blind_player.name} PLACES BIG BLIND {amount} "
                    f"({big_blind_player.name}'s bet level: {big_blind_player.bet_level} | stack: {big_blind_player.stack})\n"
                )

            table.set_bet_level(big_blind)
            table.set_full_bet_level(big_blind)
            print(f'TABLE CURRENT LEVEL: {table.bet_level}\n')

        for player in extra_big_blind_players:

            if player in table.players[:2]:
                continue

            amount = big_blind if player.stack > big_blind else player.stack
            player.decrease_stack(amount)
            player.increase_bet_level(amount)
            print(
                f"{player.name} PLACES BIG BLIND {amount} TO ENTER THE GAME WITHOUT WAITING "
                f"({player.name}'s bet level: {player.bet_level} | stack: {player.stack})"
            )
            print(f'TABLE CURRENT LEVEL: {table.bet_level}\n')

        betting_round.deal_cards_to_players(2)
        yield from betting_round.listen()

    hand_cycle.reset_current_betting_round()

    display_cards_and_money(table)
    print(f'\n============ ENDING {PREFLOP.upper()} ============\n')


def postflop(
    hand_cycle: "HandCycle",
    table: Table,
    round_name: str,
    open_fold_allowed: bool,
    raise_invalid_actions: bool,
):

    # Break before starting if only remains one player
    if len(table.live_players) == 1:
        return False

    print(f'\n============ STARTING {round_name.upper()} ============\n')

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
            betting_round.deal_common_cards(3)        
        else:
            betting_round.deal_common_cards(1)

        # Let players to play
        yield from betting_round.listen()

    hand_cycle.reset_current_betting_round()

    display_cards_and_money(table)
    print(f'\n============ ENDING {round_name.upper()} ============\n')

    return True


def run_listener(hand_cycle: "HandCycle"):

    """
    Starts the hand cycle generator that rotates the player turns.
    """

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
        print(f'\n============ SHOWDOWN! ============\n')
        showdown(hand_cycle.table)
    else:
        print('\n============ NO SHOWDOWN... ============\n')
        showdown(hand_cycle.table)