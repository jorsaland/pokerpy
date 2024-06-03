"""
Demo 0.4-A

...
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
        with pk.BettingRound(name=betting_round_name, table=table) as betting_round:
            for player in betting_round:
                action_name = random.choice(pk.possible_action_names)
                if action_name in [pk.ACTION_FOLD, pk.ACTION_CHECK]:
                    action_value = 0
                else:
                    action_value = random.randint(1, 100)
                action = pk.Action(action_name, action_value)
                player.request_action(action)

        print(f'\n============ ENDING {betting_round_name.upper()} ============\n')

    # Display showdown
    if len(table.active_players) > 1:
        print(f'\n============ SHOWDOWN! ============\n')    
        table.showdown()

    # Display no showdown
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