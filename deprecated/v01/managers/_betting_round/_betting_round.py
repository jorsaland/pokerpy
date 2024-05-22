"""
Defines the class that represents a betting round context manager.
"""


from collections.abc import Generator


from deprecated.v01.messages import (
    exiting_unended_betting_round_message,
    overloaded_betting_round_message,
    starting_already_ended_betting_round_message,
)
from deprecated.v01.structures import Player, Table


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
        self.generator = self.start()
        yield from self.generator
    
    def __exit__(self, exception_type: (type|None), exception: BaseException, _):
        if exception_type is StopIteration:
            is_overloaded = True
        elif exception_type is None:
            is_overloaded = False
        else:
            raise exception
        self.end(is_overloaded)


    def start(self):

        """
        Starts the betting round, letting players to alternate turns.
        """

        # Check betting round has not ended yet
        if self.has_ended:
            raise RuntimeError(starting_already_ended_betting_round_message) 

        # Prepare betting round before players start their actions
        self.table.reset_betting_round_states()
        self.table.deal(self.name)
        
        # All players are itered but only active ones are allowed to act
        yield from alternate_players(self.table)

        # Mark betting round as ended
        self.has_ended = True


    def end(self, is_overloaded: bool):

        """
        Ends the betting round.
        """

        if is_overloaded:
            raise RuntimeError(overloaded_betting_round_message)

        try:
            next(self.generator)
        except StopIteration:
            self.has_ended = True

        if not self.has_ended:
            raise RuntimeError(exiting_unended_betting_round_message)