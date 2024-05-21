"""
Demo 0.2-A

Now betting rounds are made to last until the last aggressive action has been responded. If all
players check, then the round ends. Because chip logic has not been developed yet, this new feature
implies that, in theory, a betting round could last forever. It also implies that now nothing
guarantees that the first player 'Andy' will always reach the showdown as it happened in previous
demos.

In order not to touch BettingRound class, a new class was defined here (UpdatedBettingRound). This
class inherits from BettingRound and overrides start method in order to add logic in the right
places.
"""


import sys
sys.path.insert(0, '.')


import random


import deprecated.v01 as v01


# Constants

betting_round_names = ['pre-flop', 'flop', 'turn', 'river']


# Test players

player_names = ['Andy', 'Boa', 'Coral', 'Dino']


# Updates

class UpdatedBettingRound(v01.BettingRound):
    def start(self):
        # Prepare betting round before players start their actions
        self.table.reset_betting_round_states()
        self.table.deal(self.name)
        # Define state variables
        last_aggressive_player: (v01.Player|None) = None
        round_must_stop = False
        lap_counter = 0
        # Extend betting round until the last aggressive action has been responded
        while not round_must_stop:
            # Add to lap counter
            lap_counter += 1
            # All players are itered but only active ones are allowed to act
            for player in self.table.players:
                # Determine whether betting round should be stopped or not
                if len(self.table.active_players) == 1:
                    print(f'--- only one active player ({self.table.active_players[0].name})... ending round\n')
                    round_must_stop = True
                    break
                if player == last_aggressive_player:
                    print(f'--- {player.name} took the last aggressive action... ending round\n')
                    round_must_stop = True
                    break
                # Determine whether player should be allowed to play or not
                if player not in self.table.active_players:
                    print(f'--- {player.name} already folded\n')
                    continue
                # Player keeps its turn until selects a valid action
                while True:
                    # Wait for player's action
                    print(f'Waiting for {player.name}...')
                    yield player
                    # Determine wheter action is valid or not
                    action = player.requested_action
                    if action is not None and v01.action_is_valid(action=action, is_under_bet=self.table.is_under_bet):
                        print(f'>>> {player.name} {action}s <<<\n'.upper())
                        break
                    print(f'--- invalid action: {action}')
                # Determine consequences of aggressive actions
                if action in v01.aggressive_actions:
                    self.table.is_under_bet = True
                    last_aggressive_player = player
                # Determine whether the player becomes inactive or not
                if action == v01.ACTION_FOLD:
                    self.table.active_players.remove(player)
            # If no player bets, the round must stop
            if last_aggressive_player is None:
                round_must_stop = True


# Playability

def cycle(table: v01.Table):

    if v01.switches.ONLY_ALLOW_FOLDING_UNDER_BET:
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
        with UpdatedBettingRound(name=betting_round_name, table=table) as betting_round:
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
    table = v01.Table(players)

    v01.switches.ONLY_ALLOW_FOLDING_UNDER_BET = True
    cycle(table)

    print()

    v01.switches.ONLY_ALLOW_FOLDING_UNDER_BET = False
    cycle(table)


# Run test

def main():
    game()

if __name__ == '__main__':
    main()