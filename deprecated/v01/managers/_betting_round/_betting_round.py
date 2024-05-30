"""
Defines the class that represents a betting round context manager.
"""


from collections.abc import Generator


from deprecated.v01.messages import (
    exiting_unended_betting_round_message,
    not_str_betting_round_name_message,
    not_table_instance_message,
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

        # Check input
        if not isinstance(name, str):
            raise TypeError(not_str_betting_round_name_message.format(type(name).__name__))
        if not isinstance(table, Table):
            raise TypeError(not_table_instance_message.format(type(table).__name__))

        # Input variables
        self._name = name
        self._table = table

        # State variables
        self._generator: (Generator[Player]|None) = None
        self._has_ended = False
    

    @property
    def name(self):
        return self._name
    
    @property
    def table(self):
        return self._table
    
    @property
    def generator(self):
        return self._generator
    
    @property
    def has_ended(self):
        return self._has_ended
    

    def __enter__(self):
        self._generator = self.run()
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
            self._has_ended = True

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
        
        # All players are itered but only active ones are allowed to act
        yield from alternate_players(self.table)

        # Mark betting round as ended
        self._has_ended = True