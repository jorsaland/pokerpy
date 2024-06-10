"""
Defines the class that represents a poker table.
"""


import secrets


from pokerpy.constants import full_sorted_values_and_suits
from pokerpy.messages import (
    table_negative_increase_message,
    table_not_atom_multiple_increase_message,
    table_not_int_cards_count_message,
    table_not_list_players_message,
    table_not_all_player_instances_message,
    table_not_player_instance_message,
    table_not_int_central_pot_message,
    table_not_int_current_amount_message,
    table_not_int_stack_atom_message,
    table_player_not_in_table_message,
    table_player_already_folded_message,
    table_stack_atom_not_more_than_zero_message,
)


from ._card import Card
from ._player import Player


class Table:


    """
    Represents a poker table and the dealer in charge.
    """


    def __init__(self, players: list[Player], *, stack_atom = 1):

        # Check input types
        if not isinstance(players, list):
            raise TypeError(table_not_list_players_message.format(type(players).__name__))
        if not all(isinstance(player, Player) for player in players):
            raise TypeError(table_not_all_player_instances_message)
        if not isinstance(stack_atom, int):
            raise TypeError(table_not_int_stack_atom_message.format(type(stack_atom).__name__))
        
        # Check input values
        if not stack_atom > 0:
            raise ValueError(table_stack_atom_not_more_than_zero_message.format(stack_atom))

        # Input variables
        self._players = players
        self._stack_atom = stack_atom

        # State variables
        self._active_players: list[Player] = []
        self._current_amount = 0
        self._last_aggressive_player: (Player|None) = None
        self._deck: list[Card] = [Card(value, suit) for value, suit in full_sorted_values_and_suits]
        self._common_cards: list[Card] = []
        self._central_pot = 0
    

    @property
    def players(self):
        return tuple(self._players)

    @property
    def stack_atom(self):
        return self._stack_atom

    @property
    def active_players(self):
        return tuple(self._active_players)

    @property
    def current_amount(self):
        return self._current_amount

    @property
    def last_aggressive_player(self):
        return self._last_aggressive_player
    
    @property
    def deck(self):
        return tuple(self._deck)
    
    @property
    def common_cards(self):
        return tuple(self._common_cards)

    @property
    def central_pot(self):
        return self._central_pot


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


    def add_to_current_amount(self, amount: int):

        """
        Increases the current chip amount that needs to be responded by players.
        """

        if not isinstance(amount, int):
            raise TypeError(table_not_int_current_amount_message.format(type(amount).__name__))

        if amount < 0:
            raise ValueError(table_negative_increase_message.format(amount))
        
        if not amount % self.stack_atom == 0:
            raise ValueError(table_not_atom_multiple_increase_message.format(self.stack_atom, amount))

        self._current_amount += amount


    def add_to_central_pot(self, amount: int):
        
        """
        Increases the pot in the center of the table by an amount.
        """

        if not isinstance(amount, int):
            raise TypeError(table_not_int_central_pot_message.format(type(amount).__name__))

        if amount < 0:
            raise ValueError(table_negative_increase_message.format(amount))

        if not amount % self.stack_atom == 0:
            raise ValueError(table_not_atom_multiple_increase_message.format(self.stack_atom, amount))

        self._central_pot += amount


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


    def set_last_aggressive_player(self, player: Player):

        """
        Marks a player as the last one to take an aggressive action.
        """

        if not isinstance(player, Player):
            raise TypeError(table_not_player_instance_message.format(type(player).__name__))

        if player not in self.players:
            raise ValueError(table_player_not_in_table_message.format(player.name))

        if player not in self.active_players:
            raise ValueError(table_player_already_folded_message.format(player.name))

        self._last_aggressive_player = player


    def reset_betting_round_states(self):
        
        """
        Resets all state variables that are restricted to betting rounds.
        """

        self._current_amount = 0
        self._last_aggressive_player = None

        for player in self.players:
            player.reset_betting_round_states()


    def deal_to_players(self, cards_count: int):

        """
        Deals cards to players in equal amounts.
        """

        if not isinstance(cards_count, int):
            raise TypeError(table_not_int_cards_count_message.format(type(cards_count).__name__))

        for _ in range(cards_count):
            for player in self.active_players:
                print(f'Dealer deals card to {player.name}.')
                card = secrets.choice(self.deck)
                self._deck.remove(card)
                player.deliver_card(card)


    def deal_common_cards(self, cards_count: int):

        """
        Deals common cards to table.
        """

        if not isinstance(cards_count, int):
            raise TypeError(table_not_int_cards_count_message.format(type(cards_count).__name__))

        print(f'Dealer deals common cards.')
        for _ in range(cards_count):
            card = secrets.choice(self.deck)
            self._deck.remove(card)
            self._common_cards.append(card)


    def no_showdown(self):

        """
        Makes the dealer to announce the winner when there is only one remaining player.
        """

        winner = self.active_players[0]
        print(f'{winner.name} wins {self.central_pot}!')


    def showdown(self):

        """
        Makes the dealer to determine who is the winner among remaining players.
        """

        print(f'Remaining players: {", ".join(p.name for p in self.active_players)}')

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
            print(f'{winners[0].name} wins {self.central_pot}!')
            return

        print(f'It is a tie! Winners: {", ".join([w.name for w in winners])}.')
        central_pot_atoms = self.central_pot // self.stack_atom ## remainder should always be zero
        profit_atoms_per_player = central_pot_atoms // len(winners)
        remainder_atoms = central_pot_atoms // self.stack_atom % len(winners)
        profit_atoms_by_player = {player: profit_atoms_per_player for player in winners}

        for player in winners:
            if remainder_atoms == 0:
                break
            profit_atoms_by_player[player] += 1
            remainder_atoms -= 1

        for player in winners:
            print(f'{player.name} wins {profit_atoms_by_player[player]}.')
        return