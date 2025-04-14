"""
Demo 0.1-C

This is a merge of demos 0.1-A and 0.1-B, displaying both situations where folding when there are
not previous bets is allowed or forbidden. The behaviour can be turned on/off in runtime by
modifiying an attribute in the Table instance.

Major changes have been introduced in PokerPy library to make possible this demo. Both Player and
Table classes were updated in order to manage state logic. Also, a BettingRound class was
introduced as a context manager that listens to each player action request.

The decision to use a context manager is the outcome of multiple refactoryings on this library. In
the very beginning I thought I would use asynchronous functions in order to pause 'dealer' actions
on the table and await for player actions. Eventually, I realized I was doing things the hard way,
and also making it harder for users. BettingRound context manager runs a generator object that
yields the player who has to act next. Execution is paused until that player chooses a valid
action. Once the generator ends by raising 'StopIteration', the context manager catches it and
exits. Probably a similar context manager will be introduced in order to run a full poker game.
"""


import sys
sys.path.insert(0, '.')


import random


import deprecated.v01 as v01


# Constants

betting_round_names = ['pre-flop', 'flop', 'turn', 'river']


# Test players

player_names = ['Andy', 'Boa', 'Coral', 'Dino']


# Playability

def cycle(table: v01.Table):

    if not table.fold_to_nothing:
        print('\n======================================================'  )
        print(  '=== STARTING CYCLE: folding only allowed UNDER BET ==='  )
        print(  '======================================================\n')
    
    else:
        print('\n=============================================='  )
        print(  '=== STARTING CYCLE: folding allowed ALWAYS ==='  )
        print(  '==============================================\n')

    # Make sure every player is active
    table.activate_all_players()

    for betting_round_name in betting_round_names:

        # Determine whether cycle should be stopped or not
        if len(table.active_players) == 1:
            break

        print(f'\n============ STARTING {betting_round_name.upper()} ============\n')

        # Run betting round
        with v01.BettingRound(name=betting_round_name, table=table) as betting_round:
            for player in betting_round:
                action = random.choice(v01.possible_actions)
                player.request(action)
        
        print(f'\n============ ENDING {betting_round_name.upper()} ============\n')
            
    if len(table.active_players) > 1:
        print(f'\n============ SHOWDOWN! ============\n')    
        table.showdown()
    else:
        print('\n============ NO SHOWDOWN... ============\n')
        winner = table.active_players[0]
        print(f'{winner.name} wins!')


def game():

    print('======================'  )
    print('=== STARTING TABLE ==='  )
    print('======================\n')

    print('\nStarting table and players...\n')
    players = [v01.Player(name) for name in player_names]
    table = v01.Table(players, fold_to_nothing=False)
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