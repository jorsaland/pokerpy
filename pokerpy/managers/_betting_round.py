"""
Defines the class that represents a betting round context manager.
"""


from collections.abc import Generator


from pokerpy.constants import ACTION_FOLD, aggressive_actions
from pokerpy.messages import (
    exiting_unended_betting_round_message,
    overloaded_betting_round_message,
    starting_already_ended_betting_round_message,
)
from pokerpy.structures import Player, Table
from pokerpy.utils import action_is_valid


class BettingRound:


    """
    Represents a betting round context manager.
    """


    def __init__(self, *, name: str, table: Table):

        # Input variables
        self.name = name
        self.table = table

        # State variables
        self.generator: (Generator[Player]|None) = None
        self.has_ended = False
    
    def __enter__(self):
        self.generator = self.start()
        yield from self.generator
    
    def __exit__(self, exception_type: type, *_):
        if exception_type == StopIteration:
            is_overloaded = True
        else:
            is_overloaded = False
        self.end(is_overloaded)


    def start(self):

        """
        Inicia la ronda de apuestas, permitiendo que los jugadores alternen sus turnos.
        """

        # Check betting round has not ended yet
        if self.has_ended:
            raise RuntimeError(starting_already_ended_betting_round_message) 

        print(f'\n=== STARTING {self.name.upper()} ===\n')

        # Prepare betting round before players start their actions
        self.table.reset_betting_round_states()
        self.table.deal(self.name)
        
        # Define state variables
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
                    print(f'<< ONLY ONE ACTIVE PLAYER ({self.table.active_players[0].name.upper()})... ENDING ROUND >>\n')
                    round_must_stop = True
                    break
                if player == self.table.last_aggressive_player:
                    print(f'<< {player.name.upper()} TOOK THE LAST AGGRESSIVE ACTION... ENDING ROUND >>\n')
                    round_must_stop = True
                    break

                # Determine whether player should be allowed to play or not
                if player not in self.table.active_players:
                    print(f'<< {player.name.upper()} ALREADY FOLDED >>\n')
                    continue

                # Player keeps its turn until selects a valid action
                while True:

                    # Wait for player's action
                    print(f'Waiting for {player.name}...')
                    yield player

                    # Determine wheter action is valid or not
                    action = player.requested_action
                    if action is not None and action_is_valid(action=action, is_under_bet=self.table.is_under_bet):
                        action_print_message = f'--- {player.name} {action}s ---'.upper()
                        print('-' * len(action_print_message))
                        print(action_print_message)
                        print('-' * len(action_print_message) + '\n')
                        break
                    print(f'<< INVALID ACTION: {action.upper()} >>')
                
                # Set consequences of aggressive actions
                if action in aggressive_actions:
                    self.table.is_under_bet = True
                    self.table.last_aggressive_player = player

                # Determine whether the player becomes inactive or not
                if action == ACTION_FOLD:
                    self.table.active_players.remove(player)
            
            # If no player bets, the round must stop
            if self.table.last_aggressive_player is None:
                round_must_stop = True
        
        # Mark betting round as ended
        self.has_ended = True


    def end(self, is_overloaded: bool):

        """
        Finaliza la ronda de apuestas.
        """

        if is_overloaded:
            raise RuntimeError(overloaded_betting_round_message)

        try:
            next(self.generator)
        except StopIteration:
            self.has_ended = True

        if not self.has_ended:
            raise RuntimeError(exiting_unended_betting_round_message)

        print(f'=== ENDING {self.name.upper()} ===\n')