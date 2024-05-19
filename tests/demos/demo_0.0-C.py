"""
Demo 0.0-C

The same poker cycle (hand) of previous 0.0 demos was simulated, importing classes and instances
defined within the library.
"""


import sys
sys.path.insert(0, '.')


from deprecated.v00 import Player, Table


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
    players = [Player(name) for name in player_names]
    table = Table(players)

    print('\n======================'  )
    print(  '=== STARTING CYCLE ==='  )
    print(  '======================\n')

    for betting_round in betting_rounds:

        print(f'\n=== STARTING {betting_round.upper()} ===\n')

        table.deal(betting_round)
        for player in table.players:
            player.play()
        
        print(f'\n=== ENDING {betting_round.upper()} ===\n')
    
    table.showdown()


# Run test

def main():
    cycle()

if __name__ == '__main__':
    main()