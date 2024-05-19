"""
Demo 0.2-B

This demo does the same than Demo 0.2-A. The only difference is that logic implemented that demo
was migrated to PokerPy and imported in this demo.
"""


import sys
sys.path.insert(0, '.')


import random


import pokerpy as pk


# Constants

betting_round_names = ['pre-flop', 'flop', 'turn', 'river']


# Test players

player_names = ['Andy', 'Boa', 'Coral', 'Dino']


# Playability

def cycle(table: pk.Table):

    if pk.switches.ONLY_ALLOW_FOLDING_UNDER_BET:
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

        # Run betting round
        with pk.BettingRound(name=betting_round_name, table=table) as betting_round:
            for player in betting_round:
                action = random.choice(pk.possible_actions)
                player.request(action)
            
    if len(table.active_players) > 1:
        table.showdown()
    else:
        print('\n=== NO SHOWDOWN... ===\n')
        winner = table.active_players[0]
        print(f'{winner.name} wins!')


def game():

    print('======================'  )
    print('=== STARTING TABLE ==='  )
    print('======================\n')

    print('\nStarting table and players...\n')
    players = [pk.Player(name) for name in player_names]
    table = pk.Table(players)

    pk.switches.ONLY_ALLOW_FOLDING_UNDER_BET = True
    cycle(table)

    print()

    pk.switches.ONLY_ALLOW_FOLDING_UNDER_BET = False
    cycle(table)


# Run test

def main():
    game()

if __name__ == '__main__':
    main()