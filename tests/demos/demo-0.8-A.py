"""
Demo 0.8-A

This demo is made from Demo 0.7-E. Engines now yield state objects instead of player objects and
all decisions are handled through them.
"""


import sys
sys.path.insert(0, '.')


import random


import pokerpy as pk
from pokerpy.logger import logger, wrap_external_log


# Constants

PREFLOP = 'pre-flop'
after_preflop_round_names = [
    (FLOP := 'flop'),
    (TURN := 'turn'),
    (RIVER := 'river'),
]

ANTE = 1
SMALL_BLIND = 5
BIG_BLIND = 10

STACK_MIN_SIZE = BIG_BLIND + ANTE + 1
STACK_MAX_SIZE = 10_000

player_names = ['Andy', 'Boa', 'Coral', 'Dani', 'Epa', 'Fomi']


def game(table: pk.Table, *, open_fold_allowed: bool = False):

    table.set_ante(ANTE)
    table.set_small_blind(SMALL_BLIND)
    table.set_big_blind(BIG_BLIND)

    table.set_button_player(table.players[-1])
    table.set_small_blind_player(table.players[0])
    table.set_big_blind_player(table.players[1])

    n = 0
    while len(table.actionable_players) > 1:

        n += 1

        assert table.small_blind
        assert table.big_blind
        assert table.small_blind_player
        assert table.big_blind_player

        previous_small_blind_player = table.small_blind_player
        previous_big_blind_player = table.big_blind_player

        big_blind_player = table.get_next_player(previous_big_blind_player)
        for await_state in table.iter_players(starting_player=big_blind_player):
            if await_state.stack == 0:
                continue
            if len(table.actionable_players) == 2:
                table.set_button_player(previous_big_blind_player)
            else:
                table.set_button_player(previous_small_blind_player)
            table.set_small_blind_player(previous_big_blind_player)
            table.set_big_blind_player(await_state)
            break

        hand_cycle = pk.HandCycle(
            name = f'hand {n}',
            table = table,
            open_fold_allowed = open_fold_allowed,
        )

        logger.info(wrap_external_log(f'starting hand cycle {hand_cycle.name}', new_line=True))

        with hand_cycle:

            for await_state in hand_cycle.listen():

                if hand_cycle.in_extra_big_blinds_phase:
                    assert isinstance(await_state, pk.PlayerBlindAwait)
                    if random.randint(0, 1):
                        await_state.place_blind()
                    continue

                assert isinstance(await_state, pk.PlayerActionAwait)

                amount_to_full_call = table.bet_level - await_state.player.bet_level
                if amount_to_full_call == 0:
                    logger.info(f'To full bet: {hand_cycle.table.min_bet} | bet level: {await_state.player.bet_level}')
                else:
                    logger.info(f'To full call: {amount_to_full_call} | to full raise: {hand_cycle.table.full_bet_level + hand_cycle.table.min_raise_increase} | bet level: {await_state.player.bet_level}')

                assert hand_cycle.betting_round is not None
                action_name, amount_range = random.choice([
                    (name, amount_range) for name, amount_range in await_state.ranges.items() if amount_range is not None
                ])
                if action_name == pk.ACTION_BET:
                    action_amount = random.randint(table.pot//2, table.pot*2)
                    if action_amount not in amount_range:
                        action_amount = amount_range[-1]
                elif action_name == pk.ACTION_RAISE:
                    amount_to_call = await_state.ranges[pk.ACTION_CALL][0]
                    smallest_amount = amount_to_call + hand_cycle.table.min_raise_increase
                    action_amount = random.randint(smallest_amount, smallest_amount*3)
                    if action_amount not in amount_range:
                        action_amount = amount_range[-1]
                else:
                    action_amount = amount_range[0]
                await_state.request_action(pk.Action(category=action_name, amount=action_amount))

        logger.info(wrap_external_log(f'ending hand cycle {hand_cycle.name}', new_line=True))
        input('\n\n--- ENTER ---\n')

def main():
    table = pk.Table([pk.Player(name, stack=random.randint(STACK_MIN_SIZE, STACK_MAX_SIZE)) for name in player_names])
    game(table)


if __name__ == '__main__':
    main()