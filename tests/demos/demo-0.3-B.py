"""
Demo 0.3-B

This is an update of Demo 0.3-A. Player and Table classes now integrate card and hand related logic
that was developed in that demo.
"""


import sys
sys.path.insert(0, '.')


from itertools import combinations
import random


import deprecated.v03 as v03


betting_round_names = [
    (PREFLOP := 'pre-flop'),
    (FLOP := 'flop'),
    (TURN := 'turn'),
    (RIVER := 'river'),
]

player_names = ['Andy', 'Boa', 'Coral', 'Dino']


def figure_out_hand(cards: list[v03.Card]):
    
    if len(cards) < 5:
        return None
    
    if len(cards) == 5:
        return v03.Hand(cards)
    
    possible_hands = [v03.Hand(combination) for combination in combinations(cards, 5)]
    return max(possible_hands)


def cycle(table: v03.Table):

    if not table.fold_to_nothing:
        print('\n======================================================'  )
        print(  '=== STARTING CYCLE: folding only allowed UNDER BET ==='  )
        print(  '======================================================\n')
    
    else:
        print('\n=============================================='  )
        print(  '=== STARTING CYCLE: folding allowed ALWAYS ==='  )
        print(  '==============================================\n')

    # Make sure every player is active and has no cards
    table.reset_cycle_states()

    for betting_round_name in betting_round_names:

        # Determine whether cycle should be stopped or not
        if len(table.active_players) == 1:
            break

        print(f'\n============ STARTING {betting_round_name.upper()} ============\n')

        # Deal two cards to each player if round is pre-flop
        if betting_round_name == PREFLOP:
            table.deal_to_players(2)
        
        # Deal three cards to table if round is flop
        if betting_round_name == FLOP:
            table.deal_common_cards(3)
        
        # Deal one card to table if round is turn or river
        if betting_round_name in (TURN, RIVER):
            table.deal_common_cards(1)
        
        # Display player cards and hand
        print('\n--------------------------------------------------')
        print(f'Common cards: {"".join(str(c) for c in table.common_cards)}')
        for player in table.active_players:
            hand = figure_out_hand(player.cards + table.common_cards)
            if hand is not None:
                player.assign_hand(hand)
            print(f"{player.name}'s cards: {''.join(str(c) for c in player.cards)} | hand: {str(player.hand)}{f' ({player.hand.category})' if player.hand is not None else ''}")
        print('--------------------------------------------------\n')

        # Run betting round
        with v03.BettingRound(name=betting_round_name, table=table) as betting_round:
            for player in betting_round:
                action = random.choice(v03.possible_actions)
                player.request_action(action)

        print(f'\n============ ENDING {betting_round_name.upper()} ============\n')

    # Display showdown or not showdown

    if len(table.active_players) > 1:
        print(f'\n============ SHOWDOWN! ============\n')    
        table.showdown()

    else:
        print('\n============ NO SHOWDOWN... ============\n')
        table.no_showdown()
        
    # Display cards and hands of remaining players

    print('\n--------------------------------------------------')
    print(f'Common cards: {"".join(str(c) for c in table.common_cards)}')
    for player in table.active_players:
        print(f"{player.name}'s cards: {''.join(str(c) for c in player.cards)} | hand: {str(player.hand)}{f' ({player.hand.category})' if player.hand is not None else ''}")
    print('--------------------------------------------------')


def game():

    print('======================'  )
    print('=== STARTING TABLE ==='  )
    print('======================\n')

    # Prepare the table
    print('\nStarting table and players...\n')
    players = [v03.Player(name) for name in player_names]
    table = v03.Table(players, fold_to_nothing=False)

    # Cycle not allowing open fold
    cycle(table)
    input('\n\n--- ENTER ---\n')

    # Cycle allowing open fold
    table.fold_to_nothing = True
    cycle(table)
    input('\n\n--- ENTER ---\n')


def main():
    game()

if __name__ == '__main__':
    main()