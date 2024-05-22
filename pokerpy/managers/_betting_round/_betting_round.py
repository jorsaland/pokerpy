"""
Defines the class that represents a betting round context manager.
"""


from collections.abc import Generator


from pokerpy.messages import (
    exiting_unended_betting_round_message,
    overloaded_betting_round_message,
    starting_already_ended_betting_round_message,
)
from pokerpy.structures import Player, Table


from ._alternate_players import alternate_players


class BettingRound:


    """
    Represents a betting round context manager.
    """


    def __init__(self, name: str, table: Table):

        # Input variables
        self.name = name
        self.table = table

        # State variables
        self.generator: (Generator[Player]|None) = None
        self.has_ended = False
    
    
    def __enter__(self):
        self.generator = self.run()
        yield from self.generator
    
    
    def __exit__(self, exception_type: (type|None), exception: BaseException, _):

        # Stopping before executing all parsed actions
        if exception_type is StopIteration:
            raise RuntimeError(overloaded_betting_round_message)
        
        # Raising unexpected exceptions
        if exception_type is not None:
            raise exception

        # End running iteration after last yield
        try:
            next(self.generator)
        except StopIteration:
            self.has_ended = True

        # Check generator has ended successfully
        if not self.has_ended:
            raise RuntimeError(exiting_unended_betting_round_message)


    def run(self):

        """
        Runs the betting round, letting players to alternate turns.
        """

        # Check betting round has not ended yet
        if self.has_ended:
            raise RuntimeError(starting_already_ended_betting_round_message) 

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
            round_must_stop = yield from alternate_players(self.table)

            # If no player bets, the round must stop
            if self.table.last_aggressive_player is None:
                round_must_stop = True
        
        # Mark betting round as ended
        self.has_ended = True