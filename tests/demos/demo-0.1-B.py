"""
Demo 0.1-B

This demo is pretty much the same as Demo 0.1-A except for the fact that folding is allowed when
the betting round is not under bet. Even though this is a small change, there is an important
consequence. In Demo 0.1-A, the first player 'Andy' could never fold because he was always the
first one to act, so he was never under bet. Therefore, he could lose only in the showdown. Now, it
is possible that other players win if the end before reaching the showdown.

For Demo 0.1-C, this library will implement a 'switch' that makes it possible to fold or not when
the round is not under bet. This switch may be on or off at different times of the game, according
to implementation needs.

"""


import sys
sys.path.insert(0, '.')


import random


from deprecated.v00 import Player, Table


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
    ACTION_FOLD,
]

valid_actions_under_bet = [
    ACTION_FOLD,
    ACTION_CALL,
    ACTION_RAISE,
]


# Test players

player_names = ['Andy', 'Boa', 'Coral', 'Dino']


# Playability

def cycle():

    print('======================'  )
    print('=== STARTING TABLE ==='  )
    print('======================\n')

    print('\nStarting table and players...\n')
    players = [Player(name) for name in player_names]
    table = Table(players)

    print('\n=============================================='  )
    print(  '=== STARTING CYCLE: folding allowed ALWAYS ==='  )
    print(  '==============================================\n')

    # Define state variables
    active_players = set(players)
    round_is_under_bet = False

    for betting_round in betting_rounds:

        # Determine whether cycle should be stopped or not
        if len(active_players) == 1:
            break

        # Reset betting round restricted state variables
        round_is_under_bet = False

        print(f'\n============ STARTING {betting_round.upper()} ============\n')

        table.deal(betting_round)
        for player in table.players:

            # Determine whether betting round should be stopped or not
            if len(active_players) == 1:
                print(f'--- only one active player ({list(active_players)[0].name})... ending round')
                break

            # Determine whether player should be allowed to play or not
            if player not in active_players:
                print(f'--- {player.name} already folded')
                continue

            # Let current player to play
            if round_is_under_bet:
                action = random.choice(valid_actions_under_bet)
            else:
                action = random.choice(valid_actions_not_under_bet)
            print(f"{player.name} {action}")

            # Determine whether round becomes under bet or not
            if action in aggressive_actions:
                round_is_under_bet = True
            
            # Determine whether the player becomes inactive or not
            if action == ACTION_FOLD:
                active_players.remove(player)
        
        print(f'\n============ ENDING {betting_round.upper()} ============\n')
    
    if len(active_players) > 1:
        print(f'\n============ SHOWDOWN! ============\n')    
        print(f'Remaining players: {", ".join(p.name for p in active_players)}')
        winner = random.choice(list(active_players))
        print(f'{winner.name} wins!')
    else:
        print('\n============ NO SHOWDOWN... ============\n')
        winner = list(active_players)[0]
        print(f'{winner.name} wins!')


# Run test

def main():
    cycle()

if __name__ == '__main__':
    main()