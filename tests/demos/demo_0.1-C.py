"""
Demo 0.1-C

This is a merge of demos 0.1-A and 0.1-B, displaying both situations where folding is allowed and
forbidden when there are not previous bets in the betting round.

You may notice this demo fully imports PokerPy instead of importing variables separately. Probably,
this 'pk' abbreviation will be used in further tests and suggested in docs.
"""


import sys
sys.path.insert(0, '.')


import random


import pokerpy as pk


# Constants

betting_round_names = ['pre-flop', 'flop', 'turn', 'river']


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

    # Make sure every player is active
    table.activate_all_players()

    # Define state variables

    for betting_round_name in betting_round_names:

        # Determine whether cycle should be stopped or not
        if len(table.active_players) == 1:
            break

        print(f'\n=== STARTING {betting_round_name.upper()} ===\n')

        table.reset_betting_round_states()
        table.deal(betting_round_name)

        with pk.BettingRound(name=betting_round_name, table=table) as betting_round:
            for player in betting_round:

                # Let current player to play
                action = random.choice(pk.possible_actions)
                while not pk.action_is_valid(action=action, is_under_bet=table.is_under_bet):
                    print(f'<< INVALID ACTION: {action.upper()} >>')
                    action = random.choice(pk.possible_actions)
                print(f'{player.name} {action}s')

                # Determine whether round becomes under bet or not
                if action in pk.aggressive_actions:
                    table.is_under_bet = True
                
                # Determine whether the player becomes inactive or not
                if action == pk.ACTION_FOLD:
                    table.active_players.remove(player)
        
        print(f'\n=== ENDING {betting_round_name.upper()} ===\n')
    
    if len(table.active_players) > 1:
        table.showdown()
    else:
        print('\n=== NO SHOWDOWN... ===\n')
        winner = table.active_players[0]
        print(f'{winner.name} wins!')


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