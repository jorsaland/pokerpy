"""
Demo 0.3-A

Card and Hand classes have been added to PokerPy library as independent features. Player, Table and
BettingRound classes are not touched (they will be modified for Demo 0.3-B). When players reach the
showdown, the winner is no longer chosen randomly, but according to the best hand. Because of this,
current Table showdown method is not used in this demo (it chooses the winner randomly).

I would like to say that in the very beginnings of this project, a few years ago, I tried to
develop a poker game and thought cards should be developed first because they seemed easier.
However, I was not aware of what features cards needed to have besides a value and a suit. I made a
lot of stuff without a clear goal, only to find out out that playability was out of my reach. This
time I decided to make things different. Playability is the spinal cord of PokerPy since the very
beginning in version 0.0. Under this approach, it has become obvious what needs to be developed and
what can be ignored or left for later development versions.
"""


import sys
sys.path.insert(0, '.')


from itertools import combinations
import random


import deprecated.v02 as v02
import deprecated.v03 as v03


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

def figure_out_hand(cards: list[v03.Card]):
    
    if len(cards) < 5:
        return None
    
    if len(cards) == 5:
        return v03.Hand(cards)
    
    possible_hands = [v03.Hand(combination) for combination in combinations(cards, 5)]
    return max(possible_hands)

def cycle(table: v02.Table):

    if not table.fold_to_nothing:
        print('\n======================================================'  )
        print(  '=== STARTING CYCLE: folding only allowed UNDER BET ==='  )
        print(  '======================================================\n')
    
    else:
        print('\n=============================================='  )
        print(  '=== STARTING CYCLE: folding allowed ALWAYS ==='  )
        print(  '==============================================\n')

    # Get deck
    deck = [v03.Card(value, suit) for value, suit in v03.full_sorted_values_and_suits]

    # Determine card containers
    cards_by_player_name: dict[str, list[v03.Card]] = {player.name: [] for player in table.players}
    hand_by_player_name: dict[str, v03.Hand] =  {}
    common_cards: list[v03.Card] = []

    # Make sure every player is active
    table.activate_all_players()
    
    for betting_round_name in betting_round_names:

        # Determine whether cycle should be stopped or not
        if len(table.active_players) == 1:
            break

        print(f'\n============ STARTING {betting_round_name.upper()} ============\n')

        # Deal two cards to each player if round is pre-flop
        if betting_round_name == PREFLOP:
            for _ in range(2):
                for player in table.players:
                    card = random.choice(deck)
                    deck.remove(card)
                    cards_by_player_name[player.name].append(card)
        
        # Deal three cards to table if round is flop
        if betting_round_name == FLOP:
            for _ in range(3):
                card = random.choice(deck)
                deck.remove(card)
                common_cards.append(card)
        
        # Deal one card to table if round is turn or river
        if betting_round_name in (TURN, RIVER):
            card = random.choice(deck)
            deck.remove(card)
            common_cards.append(card)
        
        # Display player cards and hand
        print('--------------------------------------------------')
        print(f'Common cards: {"".join(str(c) for c in common_cards)}')
        for player in table.active_players:
            personal_cards = cards_by_player_name[player.name]
            hand = figure_out_hand(personal_cards + common_cards)
            hand_by_player_name[player.name] = hand
            print(f"{player.name}'s cards: {''.join(str(c) for c in personal_cards)} | hand: {str(hand)}{f' ({hand.category})' if hand is not None else ''}")
        print('--------------------------------------------------\n')

        # Run betting round
        with v02.BettingRound(name=betting_round_name, table=table) as betting_round:
            for player in betting_round:
                action = random.choice(v02.possible_actions)
                player.request(action)

        print(f'\n============ ENDING {betting_round_name.upper()} ============\n')

    # Display showdown
    if len(table.active_players) > 1:
        print(f'\n============ SHOWDOWN! ============\n')    
        print(f'Remaining players: {", ".join(p.name for p in table.active_players)}')
        winners: list[v02.Player] = []
        for player in table.active_players:
            player_is_unbeaten = True
            for oponent in table.active_players:
                if oponent.name == player.name:
                    continue
                if hand_by_player_name[oponent.name] > hand_by_player_name[player.name]:
                    player_is_unbeaten = False
                    break
            if player_is_unbeaten:
                winners.append(player)
        if len(winners) == 1:
            print(f'{winners[0].name} wins!')
        else:
            print(f'It is a tie! Winners: {", ".join([w.name for w in winners])}.')

    # Display no showdown
    else:
        print('\n============ NO SHOWDOWN... ============\n')
        winner = table.active_players[0]
        print(f'{winner.name} wins!')

    # Display cards and hands of remaining players
    print('\n--------------------------------------------------')
    print(f'Common cards: {"".join(str(c) for c in common_cards)}')
    for player in table.active_players:
        cards = cards_by_player_name[player.name]
        hand = hand_by_player_name[player.name]
        print(f"{player.name}'s cards: {''.join(str(c) for c in cards)} | hand: {str(hand)}{f' ({hand.category})' if hand is not None else ''}")
    print('--------------------------------------------------')

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
    input('\n\n--- ENTER ---\n')


# Run test

def main():
    game()

if __name__ == '__main__':
    main()