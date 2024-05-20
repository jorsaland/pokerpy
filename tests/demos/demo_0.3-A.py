"""
Demo 0.3-A

...
"""


import sys
sys.path.insert(0, '.')


import random


import pokerpy as pk


# Constants

betting_round_names = [
    (PREFLOP := 'pre-flop'),
    (FLOP := 'flop'),
    (TURN := 'turn'),
    (RIVER := 'river'),
]


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

    # Shuffle cards
    deck = [pk.Card(value, suit) for value in pk.sorted_card_values for suit in pk.sorted_card_suits]

    # Determine card containers
    cards_by_player_name: dict[str, list[pk.Card]] = {player.name: [] for player in table.players}
    common_cards: list[pk.Card] = []

    # Make sure every player is active
    table.activate_all_players()

    for betting_round_name in betting_round_names:

        # Determine whether cycle should be stopped or not
        if len(table.active_players) == 1:
            break

        # Deal two cards to each player if round is pre-flop
        if betting_round_name == PREFLOP:
            for _ in range(2):
                for player in table.players:
                    random.shuffle(deck)
                    cards_by_player_name[player.name].append(deck.pop())
        
        # Deal three cards to table if round is flop
        if betting_round_name == FLOP:
            for _ in range(3):
                random.shuffle(deck)
                common_cards.append(deck.pop())
        
        # Deal one card to table if round is turn or river
        if betting_round_name in (TURN, RIVER):
            random.shuffle(deck)
            common_cards.append(deck.pop())
        
        # Display player cards
        for player in table.active_players:
            cards = cards_by_player_name[player.name]
            print(f"{player.name}'s cards: {''.join(str(c) for c in cards)}")

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

    print()
    for player in table.active_players:
        cards = cards_by_player_name[player.name]
        print(f"{player.name}'s cards: {''.join(str(c) for c in cards)}")
    print(f'Common cards: {"".join(str(c) for c in common_cards)}')

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