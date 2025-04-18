"""
Defines the class that represents a betting round context manager.
"""


from collections.abc import Generator


from pokerpy.logger import get_logger
from pokerpy.messages import (
    betting_round_exiting_unended_round_message,
    betting_round_not_str_name_message,
    betting_round_not_table_instance_message,
    betting_round_not_starting_player_instance_message,
    betting_round_not_stopping_player_instance_message,
    betting_round_overloaded_round_message,
    betting_round_already_ended_round_message,
)
from pokerpy.structures import Player, Table


from ._alternate_players import alternate_players


logger = get_logger()


class BettingRound:


    """
    Represents a betting round context manager.
    """


    def __init__(
        self,
        name: str,
        table: Table,
        *,
        starting_player: (Player|None) = None,
        stopping_player: (Player|None) = None,
        ignore_invalid_actions = True
    ):

        # Validations

        if not isinstance(name, str):
            raise TypeError(betting_round_not_str_name_message.format(type(name).__name__))

        if not isinstance(table, Table):
            raise TypeError(betting_round_not_table_instance_message.format(type(table).__name__))

        if starting_player is None:
            starting_player = table.players[0]
        if not isinstance(starting_player, Player):
            raise TypeError(betting_round_not_starting_player_instance_message.format(type(starting_player).__name__))

        if stopping_player is None:
            stopping_player = table.players[-1]
        if not isinstance(stopping_player, Player):
            raise TypeError(betting_round_not_stopping_player_instance_message.format(type(stopping_player).__name__))

        # Fixed variables

        self._name = name
        self._table = table

        self._starting_player = starting_player
        self._initial_stopping_player = stopping_player
        self._ignore_invalid_actions = bool(ignore_invalid_actions)

        self._generator: (Generator[Player]|None) = None

        # State variables

        self._has_ended = False


    @property
    def name(self):
        return self._name
    
    @property
    def table(self):
        return self._table
    
    @property
    def starting_player(self):
        return self._starting_player

    @property
    def initial_stopping_player(self):
        return self._initial_stopping_player
    
    @property
    def generator(self):
        return self._generator
    
    @property
    def has_ended(self):
        return self._has_ended

    @property
    def ignore_invalid_actions(self):
        return self._ignore_invalid_actions
    

    def __enter__(self):
        self._generator = self.run()
        yield from self.generator
    
    
    def __exit__(self, exception_type: (type|None), exception: (BaseException|None), _):

        # Stopping before executing all parsed actions
        if exception_type is StopIteration:
            raise RuntimeError(betting_round_overloaded_round_message)
        
        # Raising unexpected exceptions
        if exception is not None:
            raise exception

        # End running iteration after last yield
        try:
            next(self.generator)
        except StopIteration:
            self._has_ended = True

        # Check generator has ended successfully
        if not self.has_ended:
            raise RuntimeError(betting_round_exiting_unended_round_message)


    def run(self):

        """
        Runs the betting round, letting players to alternate turns.
        """

        # Check betting round has not ended yet
        if self.has_ended:
            raise RuntimeError(betting_round_already_ended_round_message)
        
        # Prepare betting round before players start their actions
        self.table.set_stopping_player(self.initial_stopping_player)

        # Define state variables
        starting_player = self.starting_player
        round_must_stop = False
        lap_counter = 0
                
        # Extend betting round until the last aggressive action has been responded
        while not round_must_stop:

            # Add to lap counter
            lap_counter += 1

            # All players are itered but only active ones are allowed to act
            round_must_stop = yield from alternate_players(
                table = self.table,
                starting_player = starting_player,
                ignore_invalid_actions = self.ignore_invalid_actions
            )

            # After the first lap, reset the starting player as the first one on the list
            starting_player = self.table.players[0]
        
        # Move chips to the center of the table
        for player in self.table.players:
            self.table.add_to_central_pot(player.current_amount)

        # Mark betting round as ended
        self._has_ended = True