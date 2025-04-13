"""
Defines the class that represents a betting round context manager.
"""


from collections.abc import Generator


from pokerpy.messages import (
    betting_round_exiting_unended_round_message,
    betting_round_not_str_name_message,
    betting_round_not_table_instance_message,
    betting_round_not_stopping_player_instance_message,
    betting_round_not_dict_blind_bets_message,
    betting_round_overloaded_round_message,
    betting_round_already_ended_round_message,
)
from pokerpy.structures import Player, Table


from ._alternate_players import alternate_players


class BettingRound:


    """
    Represents a betting round context manager.
    """


    def __init__(
        self,
        name: str,
        table: Table,
        *,
        blind_bets: (dict[Player, int]|None) = None,
        initial_stopping_player: (Player|None) = None,
        ignore_invalid_actions = True
    ):

        # Validations

        if not isinstance(name, str):
            raise TypeError(betting_round_not_str_name_message.format(type(name).__name__))

        if not isinstance(table, Table):
            raise TypeError(betting_round_not_table_instance_message.format(type(table).__name__))

        if blind_bets is None:
            blind_bets = {}
        blind_bets_dict_is_valid = (
            isinstance(blind_bets,dict) and
            all(isinstance(key, Player) for key in blind_bets.keys()) and
            all(isinstance(value, int) for value in blind_bets.values())
        )
        if not blind_bets_dict_is_valid:
            raise TypeError(betting_round_not_dict_blind_bets_message)
        
        if initial_stopping_player is None:
            initial_stopping_player = table.players[-1]
        if not isinstance(initial_stopping_player, Player):
            raise TypeError(betting_round_not_stopping_player_instance_message)

        # Input variables

        self._name = name
        self._table = table
        self._blind_bets = blind_bets
        self._ignore_invalid_actions = bool(ignore_invalid_actions)
        self._initial_stopping_player = initial_stopping_player

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
    def initial_stopping_player(self):
        return self._initial_stopping_player
    
    @property
    def generator(self):
        return self._generator
    
    @property
    def has_ended(self):
        return self._has_ended
    
    @property
    def blind_bets(self):
        return self._blind_bets
    
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
        self.table.reset_betting_round_states()
        self.table.set_stopping_player(self.initial_stopping_player)
        
        # Define state variables
        round_must_stop = False
        lap_counter = 0

        # Put blind bets
        for player in self.table.players:
            if (blind_bet := self.blind_bets.get(player)) is not None:
                player.add_to_current_amount(blind_bet)
                
        # Extend betting round until the last aggressive action has been responded
        while not round_must_stop:

            # Add to lap counter
            lap_counter += 1

            # All players are itered but only active ones are allowed to act
            round_must_stop = yield from alternate_players(
                table = self.table,
                ignore_invalid_actions = self.ignore_invalid_actions
            )

            # If no player bets, the round must stop
            if self.table.stopping_player is None:
                round_must_stop = True
        
        # Move chips to the center of the table
        for player in self.table.players:
            self.table.add_to_central_pot(player.current_amount)

        # Mark betting round as ended
        self._has_ended = True