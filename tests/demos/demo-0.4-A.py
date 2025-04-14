"""
Demo 0.4-A

Action class has been added to PokerPy library, taking a name and an amount. Basic validations were
included, such as having to call the right amount or having to put more chips than call amount in
order to make a raise. There are some current limitations to be worked in further versions:
- No blinds/antes logic has been implemented nor minimum betting or raising amounts.
- Player stacks are infinite in order to avoid issues regarding all-in and side pots logic.

By now, the smallest 'chip' is the integer 1. Therefore, any amount bet must be a positive integer.
This will change in Demo 0.4-B.
"""


import sys
sys.path.insert(0, '.')


from itertools import combinations
import random


import deprecated.v04 as v04


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

def figure_out_hand(cards: list[v04.Card]):
    
    if len(cards) < 5:
        return None
    
    if len(cards) == 5:
        return v04.Hand(cards)
    
    possible_hands = [v04.Hand(combination) for combination in combinations(cards, 5)]
    return max(possible_hands)

def cycle(table: v04.Table):

    if not table.open_fold_allowed:
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
        print(f'Common cards: {"".join(str(c) for c in table.common_cards) if table.common_cards else None} | central pot: {table.central_pot}')
        for player in table.active_players:
            hand = figure_out_hand(player.cards + table.common_cards)
            if hand is not None:
                player.assign_hand(hand)
            print(f"{player.name}'s cards: {''.join(str(c) for c in player.cards)} | hand: {str(player.hand)}{f' ({player.hand.category})' if player.hand is not None else ''}")
        print('--------------------------------------------------\n')

        # Run betting round
        with v04.BettingRound(name=betting_round_name, table=table) as betting_round:
            for player in betting_round:
                amount_to_call = table.current_amount - player.current_amount
                if amount_to_call == 0:
                    if not table.open_fold_allowed:
                        action_name = random.choice([v04.ACTION_CHECK, v04.ACTION_BET])
                    else:
                        action_name = random.choice([v04.ACTION_CHECK, v04.ACTION_BET, v04.ACTION_FOLD])
                else:
                    action_name = random.choice([v04.ACTION_CALL, v04.ACTION_FOLD, v04.ACTION_RAISE])
                if action_name in [v04.ACTION_FOLD, v04.ACTION_CHECK]:
                    action_value = 0
                elif action_name == v04.ACTION_CALL:
                    action_value = amount_to_call
                elif action_name == v04.ACTION_RAISE:
                    action_value = random.randint(amount_to_call, amount_to_call + 100)
                elif action_name == v04. ACTION_BET:
                    action_value = random.randint(1, 100)
                else:
                    raise RuntimeError('we live in a society')
                action = v04.Action(action_name, action_value)
                player.request_action(action)

        print(f'\n============ ENDING {betting_round_name.upper()} ============\n')

    # Display showdown
    if len(table.active_players) > 1:
        print(f'\n============ SHOWDOWN! ============\n')    
        print('--------------------------------------------------')
        print(f'Common cards: {"".join(str(c) for c in table.common_cards)} | central pot: {table.central_pot}')
        for player in table.active_players:
            print(f"{player.name}'s cards: {''.join(str(c) for c in player.cards)} | hand: {str(player.hand)}{f' ({player.hand.category})' if player.hand is not None else ''}")
        print('--------------------------------------------------\n')
        table.showdown()

    # Display no showdown
    else:
        print('\n============ NO SHOWDOWN... ============\n')
        print('--------------------------------------------------')
        print(f'Common cards: {"".join(str(c) for c in table.common_cards)} | central pot: {table.central_pot}')
        for player in table.active_players:
            print(f"{player.name}'s cards: {''.join(str(c) for c in player.cards)} | hand: {str(player.hand)}{f' ({player.hand.category})' if player.hand is not None else ''}")
        print('--------------------------------------------------\n')
        table.no_showdown()
        
def game():

    print('======================'  )
    print('=== STARTING TABLE ==='  )
    print('======================\n')

    print('\nStarting table and players...\n')
    players = [v04.Player(name) for name in player_names]
    table = v04.Table(players, open_fold_allowed=False)
    cycle(table)
    input('\n\n--- ENTER ---\n')

    table.open_fold_allowed = True
    cycle(table)
    input('\n\n--- ENTER ---\n')


# Run test

def main():
    game()

if __name__ == '__main__':
    main()