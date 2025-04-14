"""
Demo 0.0-B

This is an update of Demo 0.0-A that implements Player and Table classes. The dealer is considered
to be part of the table.
"""


import random


# Constants

betting_rounds = ['pre-flop', 'flop', 'turn', 'river']


# Test players

player_names = ['Andy', 'Boa', 'Coral', 'Dino']


# Dealer and player classes

class Player:
    def __init__(self, name: str):
        self.name = name
    def play(self):
        print(f'{self.name} plays.')

class Table:
    def __init__(self, players: list[Player]):
        self.players = players
    def deal(self, betting_round: str):
        print(f'Dealer deals cards for {betting_round}.\n')
    def showdown(self):
        winner = random.choice(self.players)
        print(f'{winner.name} wins!')


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

        print(f'\n============ STARTING {betting_round.upper()} ============\n')

        table.deal(betting_round)
        for player in table.players:
            player.play()
        
        print(f'\n============ ENDING {betting_round.upper()} ============\n')

    print(f'\n============ SHOWDOWN! ============\n')
    table.showdown()
    input('\n\n--- ENTER ---\n')


# Run test

def main():
    cycle()

if __name__ == '__main__':
    main()