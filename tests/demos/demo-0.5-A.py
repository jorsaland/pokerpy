"""
Demo 0.5-A

This demo is based on Demo 0.4-A. There are no differences on the mechanics. However, the parameter
'last_aggressive_player' was replaced by 'stopping_player', with some logic changes. These changes
do not intend to modify the mechanics, but to prepare them for blind bet logic. Along with the unit
tests, this demo was introduced to make sure everything is still in place.
"""


import sys
sys.path.insert(0, '.')


from itertools import combinations
import random


import pokerpy as pk


betting_round_names = [
    (PREFLOP := 'pre-flop'),
    (FLOP := 'flop'),
    (TURN := 'turn'),
    (RIVER := 'river'),
]

player_names = ['Andy', 'Boa', 'Coral', 'Dino']


def figure_out_hand(cards: list[pk.Card]):
    
    if len(cards) < 5:
        return None
    
    if len(cards) == 5:
        return pk.Hand(cards)
    
    possible_hands = [pk.Hand(combination) for combination in combinations(cards, 5)]
    return max(possible_hands)


def cycle(table: pk.Table):

    if not table.open_fold_allowed:
        print('\n======================================================'  )
        print(  '=== STARTING CYCLE: folding only allowed UNDER BET ==='  )
        print(  '======================================================\n')
    
    else:
        print('\n=============================================='  )
        print(  '=== STARTING CYCLE: folding allowed ALWAYS ==='  )
        print(  '==============================================\n')

    for betting_round_name in betting_round_names:

        # Break before starting if only remains one player
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
        with pk.BettingRound(name=betting_round_name, table=table) as betting_round:
            table.reset_betting_round_states()
            for player in betting_round:
                amount_to_call = table.current_amount - player.current_amount
                if amount_to_call == 0:
                    if not table.open_fold_allowed:
                        action_name = random.choice([pk.ACTION_CHECK, pk.ACTION_BET])
                    else:
                        action_name = random.choice([pk.ACTION_CHECK, pk.ACTION_BET, pk.ACTION_FOLD])
                else:
                    action_name = random.choice([pk.ACTION_CALL, pk.ACTION_FOLD, pk.ACTION_RAISE])
                if action_name in [pk.ACTION_FOLD, pk.ACTION_CHECK]:
                    action_value = 0
                elif action_name == pk.ACTION_CALL:
                    action_value = amount_to_call
                elif action_name == pk.ACTION_RAISE:
                    action_value = random.randint(amount_to_call, amount_to_call + 100)
                elif action_name == pk. ACTION_BET:
                    action_value = random.randint(1, 100)
                else:
                    raise RuntimeError('we live in a society')
                action = pk.Action(action_name, action_value)
                player.request_action(action)

        print(f'\n============ ENDING {betting_round_name.upper()} ============\n')

    # Display showdown or not showdown

    if len(table.active_players) > 1:
        print(f'\n============ SHOWDOWN! ============\n')    
        print('--------------------------------------------------')
        print(f'Common cards: {"".join(str(c) for c in table.common_cards)} | central pot: {table.central_pot}')
        for player in table.active_players:
            print(f"{player.name}'s cards: {''.join(str(c) for c in player.cards)} | hand: {str(player.hand)}{f' ({player.hand.category})' if player.hand is not None else ''}")
        print('--------------------------------------------------\n')
        table.showdown()

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

    # Prepare the table
    print('\nStarting table and players...\n')
    players = [pk.Player(name) for name in player_names]
    table = pk.Table(players, open_fold_allowed=False)

    # Cycle not allowing open fold
    table.reset_cycle_states()
    cycle(table)
    input('\n\n--- ENTER ---\n')

    # Cycle allowing open fold
    table.open_fold_allowed = True
    table.reset_cycle_states()
    cycle(table)
    input('\n\n--- ENTER ---\n')


def main():
    game()

if __name__ == '__main__':
    main()