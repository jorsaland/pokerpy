"""
Defines the class that represents a poker table.
"""


import secrets


from pokerpy.constants import full_sorted_values_and_suits
from pokerpy.logger import get_logger
from pokerpy.messages import (
    table_increase_not_multiple_of_smallest_chip_message,
    table_not_int_cards_count_message,
    table_not_list_players_message,
    table_not_all_player_instances_message,
    table_not_player_instance_message,
    table_not_int_central_pot_message,
    table_not_int_current_amount_message,
    table_not_int_smallest_rising_amount_message,
    table_not_int_smallest_chip_message,
    table_player_not_in_table_message,
    table_player_already_folded_message,
    table_not_positive_smallest_chip_message,
    table_sra_not_multiple_of_smallest_chip_message,
    table_not_int_smallest_bet_message,
    table_smallest_bet_not_multiple_of_smallest_chip_message,
)


from ._card import Card
from ._player import Player


logger = get_logger()


class Table:


    """
    Represents a poker table and the dealer in charge.
    """


    def __init__(
        self,
        players: list[Player],
        *,
        smallest_chip: int = 1,
        smallest_bet: int = None,
        open_fold_allowed = False,
    ):

        # Validations

        if not isinstance(players, list):
            raise TypeError(table_not_list_players_message.format(type(players).__name__))
        if not all(isinstance(player, Player) for player in players):
            raise TypeError(table_not_all_player_instances_message)

        if not isinstance(smallest_chip, int):
            raise TypeError(table_not_int_smallest_chip_message.format(type(smallest_chip).__name__))
        if not smallest_chip > 0:
            raise ValueError(table_not_positive_smallest_chip_message.format(smallest_chip))

        if smallest_bet is None:
            smallest_bet = smallest_chip
        if not isinstance(smallest_bet, int):
            raise TypeError(table_not_int_smallest_bet_message.format(type(smallest_bet).__name__))
        if not (smallest_bet > 0 and smallest_bet % smallest_chip == 0):
            raise ValueError(table_smallest_bet_not_multiple_of_smallest_chip_message.format(smallest_chip, smallest_bet))

        # Fixed variables

        self._players = players
        self._smallest_chip = smallest_chip
        self._smallest_bet = smallest_bet
        self.open_fold_allowed = open_fold_allowed # editable, hopefully boolean but not enforced

        # State variables

        self._active_players: list[Player] = []
        self._smallest_rising_amount = smallest_bet
        self._current_amount = 0
        self._stopping_player: (Player|None) = None
        self._deck: list[Card] = [Card(value, suit) for value, suit in full_sorted_values_and_suits]
        self._common_cards: list[Card] = []
        self._central_pot = 0
    

    @property
    def players(self):
        return tuple(self._players)

    @property
    def active_players(self):
        return tuple(self._active_players)

    @property
    def smallest_chip(self):
        return self._smallest_chip
    
    @property
    def smallest_bet(self):
        assert self._smallest_bet % self._smallest_chip == 0 ## should never fail, except for direct manipulation of private attributes
        return self._smallest_bet
    
    @property
    def smallest_rising_amount(self):
        assert self._smallest_rising_amount % self._smallest_chip == 0 ## should never fail, except for direct manipulation of private attributes
        return self._smallest_rising_amount

    @property
    def current_amount(self):
        assert self._current_amount % self._smallest_chip == 0 ## should never fail, except for direct manipulation of private attributes
        return self._current_amount

    @property
    def stopping_player(self):
        return self._stopping_player
    
    @property
    def deck(self):
        return tuple(self._deck)
    
    @property
    def common_cards(self):
        return tuple(self._common_cards)

    @property
    def central_pot(self):
        assert self._central_pot % self._smallest_chip == 0 ## should never fail, except for direct manipulation of private attributes
        return self._central_pot


    # Methods to affect players behaviour


    def activate_player(self, player: Player):
        
        """
        Make a single player to become available to play.
        """

        if not isinstance(player, Player):
            raise TypeError(table_not_player_instance_message.format(type(player).__name__))
        
        if player not in self.players:
            raise ValueError(table_player_not_in_table_message.format(player.name))

        if player not in self.active_players:
            self._active_players.append(player)


    def fold_player(self, player: Player):

        """
        Removes a player from a hand cycle.
        """

        if not isinstance(player, Player):
            raise TypeError(table_not_player_instance_message.format(type(player).__name__))
        
        if player not in self.players:
            raise ValueError(table_player_not_in_table_message.format(player.name))

        if player not in self.active_players:
            raise ValueError(table_player_already_folded_message.format(player.name))

        self._active_players.remove(player)


    def set_stopping_player(self, player: Player):

        """
        Marks a player before whom the betting round is closed.
        """

        if not isinstance(player, Player):
            raise TypeError(table_not_player_instance_message.format(type(player).__name__))

        if player not in self.players:
            raise ValueError(table_player_not_in_table_message.format(player.name))

        self._stopping_player = player


    # Methods to deal cards


    def deal_to_players(self, cards_count: int):

        """
        Deals cards to players in equal amounts.
        """

        if not isinstance(cards_count, int):
            raise TypeError(table_not_int_cards_count_message.format(type(cards_count).__name__))

        for _ in range(cards_count):
            for player in self.active_players:
                card = secrets.choice(self.deck)
                logger.info(f'Dealer deals card {card} to {player.name}.')
                self._deck.remove(card)
                player.deal_card(card)


    def deal_common_cards(self, cards_count: int):

        """
        Deals common cards to table.
        """

        if not isinstance(cards_count, int):
            raise TypeError(table_not_int_cards_count_message.format(type(cards_count).__name__))

        for _ in range(cards_count):
            card = secrets.choice(self.deck)
            self._deck.remove(card)
            self._common_cards.append(card)
        logger.info(f'Dealer deals common cards.')


    # Methods to affect current amount to be responded and central pot


    def add_to_current_amount(self, amount: int):

        """
        Increases the current chip amount that needs to be responded by players.
        """

        if not isinstance(amount, int):
            raise TypeError(table_not_int_current_amount_message.format(type(amount).__name__))
        
        if not (amount >= 0 and amount % self.smallest_chip == 0):
            raise ValueError(table_increase_not_multiple_of_smallest_chip_message.format(self.smallest_chip, amount))

        self._current_amount += amount


    def overwrite_smallest_rising_amount(self, amount: int):

        """
        Overwrites the smallest amount expected to make a raise.
        """

        if not isinstance(amount, int):
            raise TypeError(table_not_int_smallest_rising_amount_message.format(type(amount).__name__))
        
        if not (amount > 0 and amount % self.smallest_chip == 0):
            raise ValueError(table_sra_not_multiple_of_smallest_chip_message.format(self.smallest_chip, amount))

        self._smallest_rising_amount = amount


    def add_to_central_pot(self, amount: int):
        
        """
        Increases the pot in the center of the table by an amount.
        """

        if not isinstance(amount, int):
            raise TypeError(table_not_int_central_pot_message.format(type(amount).__name__))

        if not (amount >= 0 and amount % self.smallest_chip == 0):
            raise ValueError(table_increase_not_multiple_of_smallest_chip_message.format(self.smallest_chip, amount))

        self._central_pot += amount


    # Methods to determine winner(s)


    def no_showdown(self):

        """
        Makes the dealer to announce the winner when there is only one remaining player.
        """

        winner = self.active_players[0]
        logger.info(f'{winner.name} wins {self.central_pot}!')


    def showdown(self):

        """
        Makes the dealer to determine who is the winner among remaining players.
        """

        logger.info(f'Remaining players: {", ".join(p.name for p in self.active_players)}')

        winners: list[Player] = []
        for player in self.active_players:

            player_is_unbeaten = True
            for oponent in self.active_players:
                if oponent.name == player.name:
                    continue
                if oponent.hand > player.hand:
                    player_is_unbeaten = False
                    break

            if player_is_unbeaten:
                winners.append(player)

        if len(winners) == 1:
            logger.info(f'{winners[0].name} wins {self.central_pot}!')
            return

        logger.info(f'It is a tie! Winners: {", ".join([w.name for w in winners])}.')
        central_pot_atoms = self.central_pot // self.smallest_chip ## remainder should always be zero
        profit_atoms_per_player = central_pot_atoms // len(winners)
        remainder_atoms = central_pot_atoms // self.smallest_chip % len(winners)
        profit_atoms_by_player = {player: profit_atoms_per_player for player in winners}

        for player in winners:
            if remainder_atoms == 0:
                break
            profit_atoms_by_player[player] += 1
            remainder_atoms -= 1

        for player in winners:
            logger.info(f'{player.name} wins {profit_atoms_by_player[player]}.')
        return


    # Methods to reset managers


    def reset_betting_round_states(self):
        
        """
        Resets all state variables that are restricted to betting rounds.
        """

        self._current_amount = 0
        self._smallest_rising_amount = self.smallest_bet
        self._stopping_player = None

        for player in self.players:
            player.reset_betting_round_states()


    def reset_cycle_states(self):

        """
        Resets all state variables that are restricted to cycles.
        """

        # Reset betting_round_states
        self.reset_betting_round_states()

        # Reset players
        self._active_players.clear()
        self._active_players.extend(self._players)

        # Reset deck
        self._deck.clear()
        self._deck.extend(Card(value, suit) for value, suit in full_sorted_values_and_suits)

        # Reset pot
        self._central_pot = 0

        # Reset common and player cards
        self._common_cards.clear()
        for player in self.players:
            player.reset_cycle_states()