"""
Demo 0.2-B

This is an update of Demo 0.2-A. The betting round logic developed in that demo has been migrated
to PokerPy library and imported here.
"""


import sys
sys.path.insert(0, '.')


import random


import deprecated.v02 as v02


# Constants

betting_round_names = ['pre-flop', 'flop', 'turn', 'river']


# Test players

player_names = ['Andy', 'Boa', 'Coral', 'Dino']


# Playability

def cycle(table: v02.Table):

    if not table.fold_to_nothing:
        print('\n======================================================'  )
        print(  '=== STARTING CYCLE: folding only allowed UNDER BET ==='  )
        print(  '======================================================\n')
    
    else:
        print('\n=============================================='  )
        print(  '=== STARTING CYCLE: folding allowed ALWAYS ==='  )
        print(  '==============================================\n')

    # Make sure every player is active
    table.activate_all_players()

    for betting_round_name in betting_round_names:

        # Determine whether cycle should be stopped or not
        if len(table.active_players) == 1:
            break

        print(f'\n============ STARTING {betting_round_name.upper()} ============\n')

        # Run betting round
        with v02.BettingRound(name=betting_round_name, table=table) as betting_round:
            for player in betting_round:
                action = random.choice(v02.possible_actions)
                player.request(action)

        print(f'\n============ ENDING {betting_round_name.upper()} ============\n')

    if len(table.active_players) > 1:
        print(f'\n============ SHOWDOWN! ============\n')    
        table.showdown()
    else:
        print('\n============ NO SHOWDOWN... ============\n')
        winner = table.active_players[0]
        print(f'{winner.name} wins!')


def game():

    print('======================'  )
    print('=== STARTING TABLE ==='  )
    print('======================\n')

    print('\nStarting table and players...\n')
    players = [v02.Player(name) for name in player_names]
    table = v02.Table(players, fold_to_nothing=False)
    cycle(table)

    input('\n\n--- ENTER ---\n')

    table.fold_to_nothing = True
    cycle(table)


# Run test

def main():
    game()

if __name__ == '__main__':
    main()