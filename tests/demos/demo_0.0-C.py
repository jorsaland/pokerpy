"""
DEMO 0.0-C

The same poker cycle (hand) of previous 0.0 demos was simulated, importing classes and instances
defined within the library.
"""


import sys
sys.path.insert(0, '.')


import random


from pokerpy import Player, Table


# Constants

betting_rounds = ['pre-flop', 'flop', 'turn', 'river']


# Test players

player_names = ['Andy', 'Boa', 'Coral', 'Dino']


# Playability

def cycle():

    print('======================')
    print('=== STARTING TABLE ===')
    print('======================\n')

    print('creating table and players...\n')
    players = [Player(name) for name in player_names]
    table = Table(players)

    print('======================')
    print('=== STARTING CYCLE ===')
    print('======================\n')

    for betting_round in betting_rounds:

        table.deal(betting_round)

        for player in table.players:
            player.play()
            table.respond(player)
    
    table.showdown()
    winner = random.choice(player_names)
    print(f'{winner} wins!')


# Run test

def main():
    cycle()

if __name__ == '__main__':
    main()