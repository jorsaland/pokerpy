"""
Demo 0.5-B

This demo is based on Demo 0.5-A. Now, in the pre-flop, the first player places a single blind bet.
The second player has two options: folding or rising. If all players take passive actions, the
first player still has the chance to check or bet (rising its own blind bet). In the following
betting rounds (flop, turn and river), the mechanics are as in Demo 0.5-A.
"""


import sys
sys.path.insert(0, '.')


from itertools import combinations
import random


import pokerpy as pk


PREFLOP = 'pre-flop'
after_preflop_round_names = [
    (FLOP := 'flop'),
    (TURN := 'turn'),
    (RIVER := 'river'),
]

BLIND_BET = 10

player_names = ['Andy', 'Boa', 'Coral', 'Dino']


def display_cards_and_money(table: pk.Table):
    print('\n--------------------------------------------------')
    print(f'Common cards: {"".join(str(c) for c in table.common_cards) if table.common_cards else None} | central pot: {table.central_pot}')
    for player in table.active_players:
        hand = figure_out_hand(player.cards + table.common_cards)
        if hand is not None:
            player.assign_hand(hand)
        print(f"{player.name}'s cards: {''.join(str(c) for c in player.cards) if player.cards else None} | hand: {str(player.hand)}{f' ({player.hand.category})' if player.hand is not None else ''}")
    print('--------------------------------------------------\n')


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

    # Run pre-flop

    print(f'\n============ STARTING {PREFLOP.upper()} ============\n')

    betting_round_instance = pk.BettingRound(
        name = PREFLOP,
        table = table,
        starting_player = table.players[1],
        stopping_player = table.players[0],
    )

    with betting_round_instance as betting_round:

        # Reset betting round states regarding to table and players
        table.reset_betting_round_states()

        # Place blind bet
        blind_bet_player = table.players[0]
        blind_bet_player.add_to_current_amount(BLIND_BET)
        table.add_to_current_amount(BLIND_BET)
        print(f"{blind_bet_player.name} PLACES BLIND BET {BLIND_BET} ({blind_bet_player.name}'s current amount: {blind_bet_player.current_amount})")
        print(f'TABLE CURRENT AMOUNT: {table.current_amount}\n')

        # Deal pre-flop
        table.deal_to_players(2)
        display_cards_and_money(table)

        # Let players to play
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
                action = pk.Action(action_name, 0)
            elif action_name == pk.ACTION_CALL:
                action = pk.Action(action_name, amount_to_call)
            elif action_name == pk. ACTION_BET:
                action = pk.Action(action_name, random.randint(BLIND_BET, BLIND_BET*5))
            elif action_name == pk.ACTION_RAISE:
                smallest_amount = amount_to_call + table.smallest_rising_amount
                action_value = random.randint(smallest_amount, smallest_amount*3)
                action = pk.Action(action_name, action_value)
            else:
                raise RuntimeError('we live in a society')
            player.request_action(action)

    print(f'\n============ ENDING {PREFLOP.upper()} ============\n')

    # Run flop, turn and river

    for betting_round_name in after_preflop_round_names:

        # Break before starting if only remains one player
        if len(table.active_players) == 1:
            break

        print(f'\n============ STARTING {betting_round_name.upper()} ============\n')

        with pk.BettingRound(name=betting_round_name, table=table) as betting_round:

            # Reset betting round states regarding to table and players
            table.reset_betting_round_states()

            # Deal three cards to table if round is flop and one if is turn or river
            if betting_round_name == FLOP:
                table.deal_common_cards(3)        
            else:
                table.deal_common_cards(1)
            display_cards_and_money(table)

            # Let players to play
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
                    action = pk.Action(action_name, 0)
                elif action_name == pk.ACTION_CALL:
                    action = pk.Action(action_name, amount_to_call)
                elif action_name == pk. ACTION_BET:
                    action = pk.Action(action_name, random.randint(table.central_pot//2, table.central_pot*2))
                elif action_name == pk.ACTION_RAISE:
                    smallest_amount = amount_to_call + table.smallest_rising_amount
                    action_value = random.randint(smallest_amount, smallest_amount*3)
                    action = pk.Action(action_name, action_value)
                else:
                    raise RuntimeError('we live in a society')
                player.request_action(action)

        print(f'\n============ ENDING {betting_round_name.upper()} ============\n')

    # Display showdown or not showdown

    if len(table.active_players) > 1:
        print(f'\n============ SHOWDOWN! ============\n')
        display_cards_and_money(table)
        table.showdown()

    else:
        print('\n============ NO SHOWDOWN... ============\n')
        display_cards_and_money(table)
        table.no_showdown()


def game():

    print('======================'  )
    print('=== STARTING TABLE ==='  )
    print('======================\n')

    # Prepare the table
    print('\nStarting table and players...\n')
    players = [pk.Player(name) for name in player_names]
    table = pk.Table(players, open_fold_allowed=False, smallest_bet=BLIND_BET)

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