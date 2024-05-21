"""
Demo 0.3-A

Cards and hands have been added. This is the first demo where winner will no longer be chosen
randomly, but according to who has the best hand. A consequence of this is that current Table class
showdown method had to be removed in this demo (it chooses the winner randomly). Cards were
implemented directly on the library without modifying other dependencies. In Demo 0.3-B, Player and
Table classes (maybe BettingRound) will be modified to include cards and hands logic.

I would like to point that in my very beginnings, some years ago, I tried to develop a poker game
starting by cards as it seemed easier, but I did not find how to keep going when I had to face
playability. It is satisfying to see how postponing card logic until this point made it easier to
have a strong playability logic.
"""


import sys
sys.path.insert(0, '.')


from itertools import combinations
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

def figure_out_hand(cards: list[pk.Card]):
    if len(cards) < 5:
        return None
    if len(cards) == 5:
        return pk.Hand(cards)
    possible_hands = [pk.Hand(combination) for combination in combinations(cards, 5)]
    return max(possible_hands)

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
    hand_by_player_name: dict[str, pk.Hand] =  {}
    common_cards: list[pk.Card] = []

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
        with pk.BettingRound(name=betting_round_name, table=table) as betting_round:
            for player in betting_round:
                action = random.choice(pk.possible_actions)
                player.request(action)

        print(f'\n============ ENDING {betting_round_name.upper()} ============\n')

    # Display showdown
    if len(table.active_players) > 1:
        print(f'\n============ SHOWDOWN! ============\n')    
        print(f'Remaining players: {", ".join(p.name for p in table.active_players)}')
        winners: list[pk.Player] = []
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