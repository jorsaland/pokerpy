"""
Demo 0.7-A

This demo is made from Demo 0.6-B. The new HandCycle class is used here to replicate the behaviour.
"""


import sys
sys.path.insert(0, '.')


import random


import pokerpy as pk


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

STACK_MIN_SIZE = BIG_BLIND + ANTE
STACK_MAX_SIZE = 10_000

player_names = ['Andy', 'Boa', 'Coral', 'Dino', 'Epa', 'Fomi']


def cycle(table: pk.Table, *, open_fold_allowed: bool = False):

    if not open_fold_allowed:
        print('\n======================================================'  )
        print(  '=== STARTING CYCLE: folding only allowed UNDER BET ==='  )
        print(  '======================================================\n')
    
    else:
        print('\n=============================================='  )
        print(  '=== STARTING CYCLE: folding allowed ALWAYS ==='  )
        print(  '==============================================\n')

    hand_cycle = pk.HandCycle(
        name = 'open-fold-allowed' if open_fold_allowed else 'open-fold-forbidden',
        table = table,
        ante = ANTE,
        small_blind = SMALL_BLIND,
        big_blind = BIG_BLIND,
        extra_big_blind_players = [player for player in table.players[2:] if random.randint(0, 1)],
        open_fold_allowed = open_fold_allowed,
    )

    with hand_cycle:

        for player in hand_cycle.listen():

            amount_to_full_call = table.bet_level - player.bet_level
            if amount_to_full_call == 0:
                print(f'To full bet: {hand_cycle.table.min_bet} | bet level: {player.bet_level}')
            else:
                print(f'To full call: {amount_to_full_call} | to full raise: {hand_cycle.table.full_bet_level + hand_cycle.table.min_raise_increase} | bet level: {player.bet_level}')

            assert hand_cycle.current_betting_round is not None
            range_by_action = hand_cycle.current_betting_round.get_action_ranges()
            action_name, amount_range = random.choice([
                (name, amount_range) for name, amount_range in range_by_action.items() if amount_range is not None
            ])
            if action_name == pk.ACTION_BET:
                action_amount = random.randint(table.pot//2, table.pot*2)
                if action_amount not in amount_range:
                    action_amount = amount_range[-1]
            elif action_name == pk.ACTION_RAISE:
                amount_to_call = range_by_action[pk.ACTION_CALL][0]
                smallest_amount = amount_to_call + hand_cycle.table.min_raise_increase
                action_amount = random.randint(smallest_amount, smallest_amount*3)
                if action_amount not in amount_range:
                    action_amount = amount_range[-1]
            else:
                action_amount = amount_range[0]
            player.request_action(pk.Action(category=action_name, amount=action_amount))


def main():

    # Cycle not allowing open fold
    table = pk.Table([pk.Player(name, stack=random.randint(STACK_MIN_SIZE + 1, STACK_MAX_SIZE)) for name in player_names])
    cycle(table)
    input('\n\n--- ENTER ---\n')

    # Cycle allowing open fold
    table = pk.Table([pk.Player(name, stack=random.randint(STACK_MIN_SIZE, STACK_MAX_SIZE)) for name in player_names])
    cycle(table, open_fold_allowed=True)
    input('\n\n--- ENTER ---\n')

if __name__ == '__main__':
    main()