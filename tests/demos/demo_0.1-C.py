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

betting_rounds = ['pre-flop', 'flop', 'turn', 'river']

ACTION_CHECK = 'checks'
ACTION_FOLD = 'folds'
ACTION_CALL = 'calls'
ACTION_BET = 'bets'
ACTION_RAISE = 'raises'

aggressive_actions = [
    ACTION_BET,
    ACTION_RAISE
]

passive_actions = [
    ACTION_FOLD,
    ACTION_CHECK,
    ACTION_CALL
]

valid_actions_not_under_bet = [
    ACTION_CHECK,
    ACTION_BET,
]

valid_actions_under_bet = [
    ACTION_FOLD,
    ACTION_CALL,
    ACTION_RAISE,
]


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

    # Define state variables
    active_players = table.players.copy()
    round_is_under_bet = False

    for betting_round in betting_rounds:

        # Determine whether cycle should be stopped or not
        if len(active_players) == 1:
            break

        # Reset betting round restricted state variables
        round_is_under_bet = False

        print(f'\n=== STARTING {betting_round.upper()} ===\n')

        table.deal(betting_round)
        for player in table.players:

            # Determine whether betting round should be stopped or not
            if len(active_players) == 1:
                print(f'<< ONLY ONE ACTIVE PLAYER ({active_players[0].name.upper()})... ENDING ROUND >>')
                break

            # Determine whether player should be allowed to play or not
            if player not in active_players:
                print(f'<< {player.name.upper()} ALREADY FOLDED >>')
                continue

            # Let current player to play
            if round_is_under_bet:
                action = random.choice(valid_actions_under_bet)
            else:
                if pk.switches.ONLY_ALLOW_FOLDING_UNDER_BET:
                    action = random.choice(valid_actions_not_under_bet)
                else:
                    action = random.choice(valid_actions_not_under_bet + [ACTION_FOLD])
            print(f"{player.name} {action}")

            # Determine whether round becomes under bet or not
            if action in aggressive_actions:
                round_is_under_bet = True
            
            # Determine whether the player becomes inactive or not
            if action == ACTION_FOLD:
                active_players.remove(player)
        
        print(f'\n=== ENDING {betting_round.upper()} ===\n')
    
    if len(active_players) > 1:
        print(f'\n=== SHOWDOWN! ===\n')
        print(f'Remaining players: {", ".join(p.name for p in active_players)}')
        winner = random.choice(active_players)
        print(f'{winner.name} wins!')
    else:
        print('\n=== NO SHOWDOWN... ===\n')
        winner = active_players[0]
        print(f'{winner.name} wins!')


def game():

    print('\n======================'  )
    print(  '=== STARTING TABLE ==='  )
    print(  '======================\n')

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