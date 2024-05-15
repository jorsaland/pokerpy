"""
DEMO 0.0-B

The same poker cycle (hand) of Demo 0.0-A was simulated, using classes and instances for a table
(including the dealer as part of the table) and multiple players. By now, the table must be
instantiated with all players. Again, the winner is chossen randomly.
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
    def play(self, betting_round: str):
        print(f'{self.name} plays {betting_round}')

class Table:
    def __init__(self, players: list[Player]):
        self.players = players
    def deal(self, betting_round: str):
        print(f'\n=== Dealer deals cards for {betting_round} ===\n')
    def respond(self, player: Player):
        print(f'Dealer responds to {player.name}\n')


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
            player.play(betting_round)
            table.respond(player)
    
    winner = random.choice(player_names)
    print(f'{winner} wins!')


# Run test

def main():
    cycle()

if __name__ == '__main__':
    main()