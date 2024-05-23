"""
Demo 0.0-A

First playability demo! A Texas Hold'em poker cycle (hand) is simulated by printing player actions
and dealer responses. The winner is chosen randomly. I tried to make this as abstract as possible.
This will hopefully be the base for further development.
"""


import random


# Constants

betting_rounds = ['pre-flop', 'flop', 'turn', 'river']


# Test players

player_names = ['Andy', 'Boa', 'Coral', 'Dino']


# Playability

def cycle():

    print('======================'  )
    print('=== STARTING TABLE ==='  )
    print('======================\n')

    print('\nStarting table and players...\n')

    print('\n======================')
    print(  '=== STARTING CYCLE ===')
    print(  '======================\n')

    for betting_round in betting_rounds:

        print(f'\n============ STARTING {betting_round.upper()} ============\n')

        print(f'Dealer deals cards for {betting_round}.\n')
        for player_name in player_names:
            print(f'{player_name} plays.')
        
        print(f'\n============ ENDING {betting_round.upper()} ============\n')

    print(f'\n============ SHOWDOWN! ============\n')
    winner = random.choice(player_names)
    print(f'{winner} wins!')


# Run test

def main():
    cycle()

if __name__ == '__main__':
    main()