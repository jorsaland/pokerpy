"""
Demo 0.1-A

Based on previous demos, betting round actions are added to the Texas Hold'em poker cycle (hand)
with random player actions. Some rules regarding actions are implemented:
- A betting round becomes 'under bet' if any player has taken an aggressive action (bet or raise).
- If a betting round is under bet, then players can only fold, call or raise.
- If a betting round is not under bet, then players can only bet or raise.*
- If a player folds, it becomes inactive for the rest of the cycle.
- If there is only one player active, then the cycle ends and that player wins.

By now, if the cycle reaches the showdown, the winner is chosen randomly among the remaining active
players. At this point, each betting round consists of exactly one action per active player, even
if there are aggressive actions.

Due to the implementation where 'Andy' always acts first, then he can only check or bet, but not
fold. Therefore, that player will never lose before the showdown.

Nothing has been modified in PokerPy library for this demo. Every new dependency has been added in
this script. This is intentional. The goal here is to detect what must be developed, before adding
it to the library. A consequence of this is that Table.showdown can no longer be used in this demo,
as it chooses winner among all players instead of remaining players (because folding had not been
introduced yet). For similar reasons, player.play is no longer being used in this demo. These and
other changes will be included in the library for Demo 0.1-C.
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

    print('\n======================================================'  )
    print(  '=== STARTING CYCLE: folding only allowed UNDER BET ==='  )
    print(  '======================================================\n')

    # Define state variables
    active_players = players.copy()
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
                print(f'--- only one active player ({active_players[0].name})... ending round')
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
            print(f'{player.name} {action}')

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
        winner = random.choice(active_players)
        print(f'{winner.name} wins!')
    else:
        print('\n============ NO SHOWDOWN... ============\n')
        winner = active_players[0]
        print(f'{winner.name} wins!')


# Run test

def main():
    cycle()

if __name__ == '__main__':
    main()