"""
Defines the class that represents a betting round context manager.
"""


from collections.abc import Generator


from pokerpy.logger import get_logger
from pokerpy.messages import (
    msg_not_all_player_instances,
    msg_not_int,
    msg_not_list,
    msg_not_player_instance,
    msg_not_positive_value,
    msg_not_str,
    msg_not_table_instance,
    msg_betting_round_did_not_end,
    msg_some_players_not_in_table,
)
from pokerpy.structures import Player, Table


from ._methods_to_affect_money import method_overwrite_smallest_rising_amount
from ._methods_to_affect_players import (
    method_activate_player,
    method_deactivate_player,
    method_set_stopping_player,
)
from ._methods_to_deal_cards import method_deal_cards_to_players, method_deal_common_cards
from ._run_listener import run_listener


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
        smallest_bet: int = 1,
        active_players: (list[Player]|None) = None,
        starting_player: (Player|None) = None,
        stopping_player: (Player|None) = None,
        open_fold_allowed = False,
        ignore_invalid_actions = True
    ):

        # Validations

        if not isinstance(name, str):
            raise TypeError(msg_not_str.format(type(name).__name__))

        if not isinstance(table, Table):
            raise TypeError(msg_not_table_instance.format(type(table).__name__))

        if not isinstance(smallest_bet, int):
            raise TypeError(msg_not_int.format(type(smallest_bet).__name__))
        if smallest_bet <= 0:
            raise ValueError(msg_not_positive_value.format(smallest_bet))

        if active_players is None:
            active_players = [player for player in table.players]
        else:
            if not isinstance(active_players, list):
                raise TypeError(msg_not_list.format(type(active_players).__name__))
            if not all(isinstance(player, Player) for player in active_players):
                raise TypeError(msg_not_all_player_instances)
            if not all(player in table.players for player in active_players):
                raise ValueError(msg_some_players_not_in_table)

        if starting_player is None:
            starting_player = table.players[0]
        else:
            if not isinstance(starting_player, Player):
                raise TypeError(msg_not_player_instance.format(type(starting_player).__name__))

        if stopping_player is None:
            stopping_player = table.players[-1]
        else:
            if not isinstance(stopping_player, Player):
                raise TypeError(msg_not_player_instance.format(type(stopping_player).__name__))

        # Fixed variables

        self._listener: (Generator[Player]|None) = None

        self._name = name
        self._table = table

        self._smallest_bet = smallest_bet

        self.open_fold_allowed = open_fold_allowed # editable, hopefully boolean but not enforced
        self._ignore_invalid_actions = bool(ignore_invalid_actions)

        # State variables

        self._has_ended = False

        self._smallest_rising_amount = smallest_bet

        self._active_players = active_players
        self._starting_player = starting_player
        self._stopping_player = stopping_player

    @property
    def name(self):
        return self._name

    @property
    def table(self):
        return self._table

    @property
    def active_players(self):
        return tuple(self._active_players)

    @property
    def starting_player(self):
        return self._starting_player

    @property
    def stopping_player(self):
        return self._stopping_player

    @property
    def smallest_bet(self):
        return self._smallest_bet

    @property
    def smallest_rising_amount(self):
        return self._smallest_rising_amount

    @property
    def has_ended(self):
        return self._has_ended

    @property
    def ignore_invalid_actions(self):
        return self._ignore_invalid_actions


    def __enter__(self):
        self.listen()
        return self


    def __exit__(self, exception_type: (type|None), exception: (BaseException|None), _):

        # Stopping before executing all parsed actions
        if exception_type is StopIteration:
            logger.critical('====== THE BETTING ROUND WAS STOPPED BEFORE ENDING ======')
            raise RuntimeError(msg_betting_round_did_not_end)

        # Raising unexpected exceptions
        if exception is not None:
            raise exception
        
        self.stop()


    # Methods to control the listener


    def listen(self):

        """
        Starts and retrieves the generator object that listens for player actions.
        """

        if self._listener is None:
            self._listener = run_listener(self)
        return self._listener


    def stop(self):

        """
        Runs the last step in 
        """

        # End running iteration after last yield
        try:
            next(self.listen())
        except StopIteration:
            self._has_ended = True

        # Check generator has ended successfully
        if not self.has_ended:
            raise RuntimeError(msg_betting_round_did_not_end)


    # Methods to affect players


    def activate_player(self, player: Player):
        
        """
        Make a single player to become available to play.
        """

        return method_activate_player(self, player)


    def deactivate_player(self, player: Player):

        """
        Removes a player from a hand cycle.
        """

        return method_deactivate_player(self, player)


    def set_stopping_player(self, player: Player):

        """
        Marks a player before whom the betting round is closed.
        """

        return method_set_stopping_player(self, player)
    

    # Methods to affect money


    def overwrite_smallest_rising_amount(self, amount: int):

        """
        Overwrites the smallest amount expected to make a raise.
        """

        return method_overwrite_smallest_rising_amount(self, amount)
    

    # Methods to deal cards

    
    def deal_cards_to_players(self, cards_count: int):

        """
        Deals cards to players in equal amounts.
        """

        return method_deal_cards_to_players(self, cards_count)


    def deal_common_cards(self, cards_count: int):

        """
        Deals common cards to table.
        """

        return method_deal_common_cards(self, cards_count)