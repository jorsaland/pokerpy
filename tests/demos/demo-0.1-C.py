"""
Demo 0.1-C

This is a merge of demos 0.1-A and 0.1-B, displaying both situations where folding is allowed and
forbidden when there are not previous bets in the betting round.

Major changes have were introduced in PokerPy in order to make possible this demo. A 'switch' that
turns on/off the feature that allows folding when there are no previous bets was included. This
makes it possible to use or stop using this feature in run time. Both Player and Table classes were
updated in order to manage state logic. Also, BettingRound class was introduced as a context manager
that runs a generator function that manages logic within betting rounds and listens to player
requests.

The decision to use a context manager is the outcome of multiple refactoryings on this library. In
the very beginning I thought I would use asynchronous functions in order to pause 'dealer' actions
on the table and await for player actions. Eventually, I realized I was doing things the hard way,
and also making it harder for users. A context manager can generate an iterator which lets the
table 'dealer' to modify the table as expected and get paused by yielding the player who acts next.
After that player takes an action, the current iteration continues and the next one starts. Once
the generator dies by raising 'StopIteration', the context manager is able to catch this exception
and do something with it. Probably a similar context manager will be introduced when developing the
logic for a full poker game.

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

    for betting_round_name in betting_round_names:

        # Determine whether cycle should be stopped or not
        if len(table.active_players) == 1:
            break

        print(f'\n============ STARTING {betting_round_name.upper()} ============\n')

        # Run betting round
        with pk.BettingRound(name=betting_round_name, table=table) as betting_round:
            for player in betting_round:
                action = random.choice(pk.possible_actions)
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