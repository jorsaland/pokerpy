"""
Defines unit tests on Table class.
"""


import sys
sys.path.insert(0, '.')


from decimal import Decimal
from unittest import main, TestCase


from pokerpy import constants, messages, structures


class BaseTestCase(TestCase):


    "Base class for test cases that require a shared setup."


    def setUp(self):

        self.setup_players = [
            structures.Player('Andy', 1000),
            structures.Player('Boa', 1000),
            structures.Player('Coral', 1000),
            structures.Player('Dino', 1000),
            structures.Player('Epa', 1000),
            structures.Player('Fomi', 1000),
        ]

        self.Andy = self.setup_players[0]
        self.Boa = self.setup_players[1]
        self.Coral = self.setup_players[2]
        self.Dino = self.setup_players[3]
        self.Epa = self.setup_players[4]
        self.Fomi = self.setup_players[5]

        self.setup_full_deck = tuple(structures.Card(value, suit) for value, suit in constants.sorted_card_values_and_suits)


class TestTableInstantiation(BaseTestCase):


    "Runs unit tests on table instantiation."


    def test_whole_input_players_type_error(self):

        "Tests type error detection on the whole input of field players."

        players_tuple = (
            structures.Player('Andy', 1000),
            structures.Player('Boa', 1000),
        )
        bad_players_sets = (1, None, players_tuple)

        for bad_players_set in bad_players_sets:

            with self.subTest(players=bad_players_set):
                with self.assertRaises(TypeError) as context:
                    structures.Table(bad_players_set)
                self.assertEqual(context.exception.args[0], messages.msg_not_list.format(type(bad_players_set).__name__))


    def test_players_items_type_error(self):

        "Tests type error detection on one of the items of field players."

        bad_players_1 = [
            structures.Player('Andy', 1000),
            structures.Player('Boa', 1000),
            'Coral',
        ]

        bad_players_2 = [
            structures.Player('Andy', 1000),
            structures.Player('Boa', 1000),
            None,
        ]

        bad_players_3 = [1, 2, 3]

        for bad_player_list in (bad_players_1, bad_players_2, bad_players_3):

            with self.subTest(players=bad_player_list):
                with self.assertRaises(TypeError) as context:
                    structures.Table(bad_player_list)
                self.assertEqual(context.exception.args[0], messages.msg_not_all_player_instances)


    def test_full_bet_type_error(self):

        "Tests type error detection on field full_bet."

        bad_full_bet_amounts = ('1000', 1000.0, Decimal('1000'), None)

        for bad_full_bet_amount in bad_full_bet_amounts:

            with self.subTest(full_bet=bad_full_bet_amount):
                with self.assertRaises(TypeError) as context:
                    structures.Table(self.setup_players, min_bet=bad_full_bet_amount)
                self.assertEqual(context.exception.args[0], messages.msg_not_int.format(type(bad_full_bet_amount).__name__))


    def test_starting_player_type_error(self):

        "Tests type error detection on field starting_player."

        bad_starting_players = ('Dino', 1)

        for bad_starting_player in bad_starting_players:

            with self.subTest(starting_player=bad_starting_player):
                with self.assertRaises(TypeError) as context:
                    structures.Table(self.setup_players, starting_player=bad_starting_player)
                self.assertEqual(context.exception.args[0], messages.msg_not_player_instance.format(type(bad_starting_player).__name__))


    def test_stopping_player_type_error(self):

        "Tests type error detection on field stopping_player."

        bad_stopping_players = ('Dino', 1)

        for bad_stopping_player in bad_stopping_players:

            with self.subTest(stopping_player=bad_stopping_player):
                with self.assertRaises(TypeError) as context:
                    structures.Table(self.setup_players, stopping_player=bad_stopping_player)
                self.assertEqual(context.exception.args[0], messages.msg_not_player_instance.format(type(bad_stopping_player).__name__))


    def test_players_value_error(self):

        "Tests value error detection on field players."

        with self.subTest('empty table'):
            with self.assertRaises(ValueError) as context:
                structures.Table([])
            self.assertEqual(context.exception.args[0], messages.msg_no_players_in_table)


    def test_min_bet_value_error(self):

        "Tests value error detection on field min_bet."

        bad_min_bet = 0
        with self.subTest('zero minimum bet'):
            with self.assertRaises(ValueError) as context:
                structures.Table(self.setup_players, min_bet=bad_min_bet)
            self.assertEqual(context.exception.args[0], messages.msg_not_positive_value.format(bad_min_bet))

        bad_min_bet = -10
        with self.subTest('negative minimum bet'):
            with self.assertRaises(ValueError) as context:
                structures.Table(self.setup_players, min_bet=bad_min_bet)
            self.assertEqual(context.exception.args[0], messages.msg_not_positive_value.format(bad_min_bet))


    def test_starting_player_value_error(self):

        "Tests value error detection on field starting_player."

        player_not_in_table = structures.Player('Zero', 1000)
        with self.subTest('player not in table'):
            with self.assertRaises(ValueError) as context:
                structures.Table(self.setup_players, starting_player=player_not_in_table)
            self.assertEqual(context.exception.args[0], messages.msg_player_not_in_table.format(player_not_in_table.name))


    def test_stopping_player_value_error(self):

        "Tests value error detection on field stopping_player."

        player_not_in_table = structures.Player('Zero', 1000)
        with self.subTest('player not in table'):
            with self.assertRaises(ValueError) as context:
                structures.Table(self.setup_players, stopping_player=player_not_in_table)
            self.assertEqual(context.exception.args[0], messages.msg_player_not_in_table.format(player_not_in_table.name))


    def test_valid_input(self):

        "Tests valid input."

        table = structures.Table(self.setup_players)
        with self.subTest('simple instantiation'):
            self.assertTupleEqual(table.deck, self.setup_full_deck)
            self.assertTupleEqual(table.common_cards, ())
            self.assertTupleEqual(table.players, tuple(self.setup_players))
            self.assertTupleEqual(table.live_players, tuple(self.setup_players))
            self.assertTupleEqual(table.actionable_players, tuple(self.setup_players))
            self.assertEqual(table.starting_player, self.Andy)
            self.assertEqual(table.stopping_player, self.Fomi)
            self.assertEqual(table.current_player, self.Andy)
            self.assertEqual(table.bet_level, 0)
            self.assertEqual(table.full_bet_level, 0)
            self.assertEqual(table.min_bet, 1)
            self.assertEqual(table.min_raise_increase, 1)
            self.assertEqual(table.pot, 0)
            self.assertTupleEqual(table.central_pot, (0,))

        table = structures.Table(
            self.setup_players,
            min_bet = 10,
            starting_player = self.setup_players[1],
            stopping_player = self.setup_players[-2],
        )
        with self.subTest('complex instantiation'):
            self.assertTupleEqual(table.deck, self.setup_full_deck)
            self.assertTupleEqual(table.common_cards, ())
            self.assertTupleEqual(table.players, tuple(self.setup_players))
            self.assertTupleEqual(table.live_players, tuple(self.setup_players))
            self.assertTupleEqual(table.actionable_players, tuple(self.setup_players))
            self.assertEqual(table.starting_player, self.Boa)
            self.assertEqual(table.stopping_player, self.Epa)
            self.assertEqual(table.current_player, self.Boa)
            self.assertEqual(table.bet_level, 0)
            self.assertEqual(table.full_bet_level, 0)
            self.assertEqual(table.min_bet, 10)
            self.assertEqual(table.min_raise_increase, 10)
            self.assertTupleEqual(table.central_pot, (0,))
            self.assertEqual(table.pot, 0)


class TestTableCardMethodsAndAttributes(BaseTestCase):


    "Runs unit tests on player methods and attributes related to cards."


    def test_type_errors_in_card_related_methods(self):

        "Tests type error detection in methods related to cards."

        table = structures.Table(self.setup_players)

        methods = (
            table.remove_card_from_deck,
            table.assign_common_card,
        )

        bad_cards = (1, 'the_tower', None)

        for method in methods:

            for bad_card in bad_cards:

                with self.subTest(method=method.__name__, card=bad_card):
                    with self.assertRaises(TypeError) as context:
                        method(bad_card)
                    self.assertEqual(context.exception.args[0], messages.msg_not_card_instance.format(type(bad_card).__name__))


    def test_value_error_in_deck_related_methods(self):

        "Tests value error detection in methods related to the deck."

        table = structures.Table(self.setup_players)

        card_to_remove = structures.Card(constants.QUEENS, constants.CLUBS)

        table.remove_card_from_deck(card_to_remove)
        with self.subTest('card not in deck'):
            with self.assertRaises(ValueError) as context:
                table.remove_card_from_deck(card_to_remove)
            self.assertEqual(context.exception.args[0], messages.msg_card_not_in_deck)


    def test_value_error_in_common_cards_related_methods(self):

        "Tests value error detection in methods related to the common cards."

        table = structures.Table(self.setup_players)

        card_to_assign = structures.Card(constants.JACKS, constants.DIAMONDS)

        table.assign_common_card(card_to_assign)
        with self.subTest('card already assigned'):
            with self.assertRaises(ValueError) as context:
                table.assign_common_card(card_to_assign)
            self.assertEqual(context.exception.args[0], messages.msg_repeated_cards)


    def test_valid_input_in_deck_related_methods(self):

        "Tests valid input in methods related to the deck."

        table = structures.Table(self.setup_players)

        cards_to_remove = (
            structures.Card(constants.SEVENS, constants.CLUBS),
            structures.Card(constants.TENS, constants.DIAMONDS),
            structures.Card(constants.DEUCES, constants.SPADES),
        )

        with self.subTest('before card removal'):
            self.assertTupleEqual(table.deck, self.setup_full_deck)

        for i, card in enumerate(cards_to_remove):
            table.remove_card_from_deck(card)
            with self.subTest('removal', card=str(card)):
                self.assertTupleEqual(table.deck, tuple(c for c in self.setup_full_deck if c not in cards_to_remove[:i+1]))

        table.reset_deck()
        with self.subTest('after deck reset'):
            self.assertTupleEqual(table.deck, self.setup_full_deck)


    def test_valid_input_in_common_cards_related_methods(self):

        "Tests valid input in methods related to the common cards."

        table = structures.Table(self.setup_players)

        cards_to_assign = (
            structures.Card(constants.ACES, constants.SPADES),
            structures.Card(constants.DEUCES, constants.HEARTS),
            structures.Card(constants.THREES, constants.SPADES),
        )

        with self.subTest('before card assignment'):
            self.assertTupleEqual(table.common_cards, ())

        for i, card in enumerate(cards_to_assign):
            table.assign_common_card(card)
            with self.subTest('assignment', card=str(card)):
                self.assertTupleEqual(table.common_cards, cards_to_assign[:i+1])

        table.reset_common_cards()
        with self.subTest('after common cards reset'):
            self.assertTupleEqual(table.common_cards, ())


class TestTableMoneyMethodsAndAttributes(BaseTestCase):


    "Runs unit tests on player methods and attributes related to money."


    def test_type_errors_in_money_related_methods(self):

        "Tests type error detection in methods related to money."

        table = structures.Table(self.setup_players)

        methods = (
            table.set_min_bet,
            table.set_min_raise_increase,
            table.set_bet_level,
            table.set_full_bet_level,
        )

        bad_amounts = ('1000', 1000.0, Decimal('1000'), None)

        for method in methods:

            for bad_amount in bad_amounts:

                with self.subTest(method=method.__name__, amount=bad_amount):
                    with self.assertRaises(TypeError) as context:
                        method(bad_amount)
                    self.assertEqual(context.exception.args[0], messages.msg_not_int.format(type(bad_amount).__name__))


    def test_value_error_in_money_related_methods_allowing_only_positive_values(self):

        "Tests value error detection in methods related to money that allow only positive values."

        table = structures.Table(self.setup_players)

        methods = (
            table.set_min_bet,
            table.set_min_raise_increase,
        )

        for method in methods:

            bad_amount = 0
            with self.subTest('zero amount', method=method.__name__, amount=bad_amount):
                with self.assertRaises(ValueError) as context:
                    method(bad_amount)
                self.assertEqual(context.exception.args[0], messages.msg_not_positive_value.format(bad_amount))

            bad_amount = -10
            with self.subTest('negative amount', method=method.__name__, amount=bad_amount):
                with self.assertRaises(ValueError) as context:
                    method(bad_amount)
                self.assertEqual(context.exception.args[0], messages.msg_not_positive_value.format(bad_amount))


    def test_value_error_in_money_related_methods_allowing_only_non_negative_values(self):

        "Tests value error detection in methods related to money that allow only non-negative values."

        table = structures.Table(self.setup_players)

        methods = (
            table.set_bet_level,
            table.set_full_bet_level,
        )

        for method in methods:

            bad_amount = -10
            with self.subTest('negative amount', method=method.__name__, amount=bad_amount):
                with self.assertRaises(ValueError) as context:
                    method(bad_amount)
                self.assertEqual(context.exception.args[0], messages.msg_not_positive_or_zero_value.format(bad_amount))


    def test_valid_input_in_money_related_methods_that_set_properties(self):

        "Tests valid input detection in methods related to money that set properties."

        table = structures.Table(self.setup_players)

        setup = (
          # (initial_value, method,                        property_name)
            (1,             table.set_min_bet,            structures.Table.min_bet.fget.__name__),
            (1,             table.set_min_raise_increase, structures.Table.min_raise_increase.fget.__name__),
            (0,             table.set_bet_level,          structures.Table.bet_level.fget.__name__),
            (0,             table.set_full_bet_level,     structures.Table.full_bet_level.fget.__name__),
        )

        amounts = (50, 100, 150, 200)

        for initial_value, method, property_name in setup:

            with self.subTest('before assignment', property=property_name):
                self.assertEqual(getattr(table, property_name), initial_value)

            for amount in amounts:

                method(amount)
                with self.subTest('assignment', property=property_name, amount=amount):
                    self.assertEqual(getattr(table, property_name), amount)


class TestTablePotMethodsAndAttributes(BaseTestCase):


    "Runs unit tests on player methods and attributes related to the pot."


    def test_type_errors_in_pot_related_methods(self):

        "Tests type error detection in methods related to the pot."

        table = structures.Table(self.setup_players)

        bad_amounts = ('1000', 1000.0, Decimal('1000'), None)

        for bad_amount in bad_amounts:

            with self.subTest(amount=bad_amount):
                with self.assertRaises(TypeError) as context:
                    table.increase_central_pot(bad_amount)
                self.assertEqual(context.exception.args[0], messages.msg_not_int.format(type(bad_amount).__name__))


    def test_value_error_in_pot_related_methods(self):

        "Tests value error detection in methods related to the pot."

        table = structures.Table(self.setup_players)

        bad_amount = -10
        with self.subTest('negative amount', amount=bad_amount):
            with self.assertRaises(ValueError) as context:
                table.increase_central_pot(bad_amount)
            self.assertEqual(context.exception.args[0], messages.msg_not_positive_or_zero_value.format(bad_amount))


    def test_valid_input_in_pot_methods(self):

        "Tests valid input detection in methods related to the pot."

        table = structures.Table(self.setup_players)

        amounts = (50, 100, 150, 200)
        SIDE_POT_ITERATIONS = 5
        PLAYER_BET_LEVEL_INCREASE = 100

        expected_pot = 0
        expected_central_pot = (0,)
        with self.subTest('before increases and adding side pots', expected_pot=expected_pot, expected_central_pot=expected_central_pot):
            self.assertEqual(table.pot, 0)
            self.assertTupleEqual(table.central_pot, (0,))

        for i, amount in enumerate(amounts):
            table.increase_central_pot(amount)
            expected_central_pot = (sum(amounts[:i+1]),)
            expected_pot = sum(amounts[:i+1])
            with self.subTest('increase, before adding side pots', amount=amount, expected_pot=expected_pot, expected_central_pot=expected_central_pot):
                self.assertEqual(table.pot, expected_pot)
                self.assertTupleEqual(table.central_pot, expected_central_pot)

        for j in range(1, SIDE_POT_ITERATIONS):
            table.add_side_pot()
            for i, amount in enumerate(amounts):
                table.increase_central_pot(amount)
                expected_pot = (j*sum(amounts) + sum(amounts[:i+1]))
                expected_central_pot = tuple(sum(amounts) for _ in range(j)) + (sum(amounts[:i+1]),)
                with self.subTest('increase central pot and side pots', side_pot=j, amount=amount, expected_pot=expected_pot, expected_central_pot=expected_central_pot):
                    self.assertEqual(table.pot, expected_pot)
                    self.assertTupleEqual(table.central_pot, expected_central_pot)

        for i, player in enumerate(self.setup_players, start=1):
            player.increase_bet_level(PLAYER_BET_LEVEL_INCREASE)
            expected_pot = SIDE_POT_ITERATIONS*sum(amounts) + i*PLAYER_BET_LEVEL_INCREASE
            expected_central_pot = tuple(sum(amounts) for _ in range(SIDE_POT_ITERATIONS))
            with self.subTest('increase player bet level', player=player.name, expected_pot=expected_pot, expected_central_pot=expected_central_pot):
                self.assertEqual(table.pot, expected_pot)
                self.assertEqual(table.central_pot, expected_central_pot)

        table.clear_central_pot()
        for player in self.setup_players:
            player.decrease_bet_level(PLAYER_BET_LEVEL_INCREASE)
        expected_pot = 0
        expected_central_pot = (0,)
        with self.subTest('clear central pot', expected_pot=expected_pot, expected_side_pot=expected_central_pot):
            self.assertEqual(table.pot, expected_pot)
            self.assertTupleEqual(table.central_pot, expected_central_pot)


class TestTablePlayerMethods(BaseTestCase):


    "Runs unit tests on methods related to players."


    def test_type_errors_in_players_related_methods(self):

        "Tests type error detection in methods related to players."

        table = structures.Table(self.setup_players)

        methods = (
            table.set_starting_player,
            table.set_stopping_player,
            table.set_current_player,
            table.get_next_player,
            table.get_previous_player,
        )

        bad_players = (1, 'Andy', None)

        for method in methods:

            for bad_player in bad_players:

                with self.subTest(method=method.__name__, player=bad_player):
                    with self.assertRaises(TypeError) as context:
                        method(bad_player)
                    self.assertEqual(context.exception.args[0], messages.msg_not_player_instance.format(type(bad_player).__name__))


    def test_value_error_in_player_related_methods(self):

        "Tests value error detection in methods related to players."

        table = structures.Table(self.setup_players)

        player_not_in_table = structures.Player('Zero', 1000)

        methods = (
            table.set_starting_player,
            table.set_stopping_player,
            table.set_current_player,
            table.get_next_player,
            table.get_previous_player,
        )

        for method in methods:

            with self.subTest('player not in table', method=method.__name__):
                with self.assertRaises(ValueError) as context:
                    method(player_not_in_table)
                self.assertEqual(context.exception.args[0], messages.msg_player_not_in_table.format(player_not_in_table.name))


    def test_valid_input_in_player_related_methods_that_set_properties(self):

        "Tests valid input detection in methods related to players that set properties."

        table = structures.Table(self.setup_players)

        setup = (
          # (initial_value,          method,                    property_name)
            (self.setup_players[0],  table.set_starting_player, structures.Table.starting_player.fget.__name__),
            (self.setup_players[-1], table.set_stopping_player, structures.Table.stopping_player.fget.__name__),
            (self.setup_players[0],  table.set_current_player,  structures.Table.current_player.fget.__name__),
        )

        for initial_value, method, property_name in setup:

            with self.subTest('before assignment', property=property_name):
                self.assertEqual(getattr(table, property_name), initial_value)

            for player in self.setup_players:

                method(player)
                with self.subTest('assignment', property=property_name, player=player.name):
                    self.assertEqual(getattr(table, property_name), player)


    def test_valid_input_in_methods_that_retrieve_next_and_previous_players(self):

        "Tests valid input detection in methods that retrieve next and previous players."

        table = structures.Table(self.setup_players)

        for i, player in enumerate(self.setup_players):

            expected_previous_player = self.setup_players[i-1]
            if player == self.setup_players[-1]:
                expected_next_player = self.setup_players[0]
            else:
                expected_next_player = self.setup_players[i+1]

            with self.subTest('next player', current=player.name, expected=expected_next_player.name):
                self.assertEqual(table.get_next_player(player), expected_next_player)

            with self.subTest('previous player', current=player.name, expected=expected_previous_player.name):
                self.assertEqual(table.get_previous_player(player), expected_previous_player)

        # Single player table edge case

        player = structures.Player('Zero', 1000)
        single_player_table = structures.Table([player])

        with self.subTest('next player in single player table', current=player.name, expected=player.name):
            self.assertEqual(single_player_table.get_next_player(player), player)

        with self.subTest('previous player in single player table', current=player.name, expected=player.name):
            self.assertEqual(single_player_table.get_previous_player(player), player)


class TestTablePlayerArrayAttributesEvolution(BaseTestCase):


    "Runs unit tests on the evolution of attributes that hold player arrays."


    def test_players_attributes_when_all_fold(self):

        "Tests players arrays evolution when players fold."

        table = structures.Table(self.setup_players)

        with self.subTest('before folding'):
            self.assertTupleEqual(table.players, tuple(self.setup_players))
            self.assertTupleEqual(table.live_players, tuple(self.setup_players))
            self.assertTupleEqual(table.actionable_players, tuple(self.setup_players))
            self.assertTupleEqual(table.bettor_players, ())

        folded_players: list[structures.Player] = []
        for player in self.setup_players:

            player.mark_is_folded()
            folded_players.append(player)

            with self.subTest('folded', player=player.name):
                self.assertTupleEqual(table.players, tuple(self.setup_players))
                self.assertTupleEqual(table.live_players, tuple(p for p in self.setup_players if p not in folded_players))
                self.assertTupleEqual(table.actionable_players, tuple(p for p in self.setup_players if p not in folded_players))
                self.assertTupleEqual(table.bettor_players, ())


    def test_players_attributes_when_all_bet(self):

        "Tests player arrays evolution when players bet not going all-in."

        table = structures.Table(self.setup_players)

        with self.subTest('before betting'):
            self.assertTupleEqual(table.players, tuple(self.setup_players))
            self.assertTupleEqual(table.live_players, tuple(self.setup_players))
            self.assertTupleEqual(table.actionable_players, tuple(self.setup_players))
            self.assertTupleEqual(table.bettor_players, ())

        betting_players: list[structures.Player] = []
        for player in self.setup_players:

            player.decrease_stack(100)
            player.increase_bet_level(100)
            betting_players.append(player)

            with self.subTest('bet', player=player.name):
                self.assertTupleEqual(table.players, tuple(self.setup_players))
                self.assertTupleEqual(table.live_players, tuple(self.setup_players))
                self.assertTupleEqual(table.actionable_players, tuple(self.setup_players))
                self.assertTupleEqual(table.bettor_players, tuple(p for p in self.setup_players if p in betting_players))


    def test_players_attributes_when_all_bet_and_fold(self):

        "Tests player arrays evolution when players bet not going all-in, and also fold."

        table = structures.Table(self.setup_players)

        with self.subTest('before betting and folding'):
            self.assertTupleEqual(table.players, tuple(self.setup_players))
            self.assertTupleEqual(table.live_players, tuple(self.setup_players))
            self.assertTupleEqual(table.actionable_players, tuple(self.setup_players))
            self.assertTupleEqual(table.bettor_players, ())

        bettor_folded_players: list[structures.Player] = []
        for player in self.setup_players:

            player.decrease_stack(100)
            player.increase_bet_level(100)
            player.mark_is_folded()
            bettor_folded_players.append(player)

            with self.subTest('bet and fold', player=player.name):
                self.assertTupleEqual(table.players, tuple(self.setup_players))
                self.assertTupleEqual(table.live_players, tuple(p for p in self.setup_players if p not in bettor_folded_players))
                self.assertTupleEqual(table.actionable_players, tuple(p for p in self.setup_players if p not in bettor_folded_players))
                self.assertTupleEqual(table.bettor_players, tuple(p for p in self.setup_players if p in bettor_folded_players))


    def test_players_attributes_when_all_go_all_in(self):

        "Tests player arrays evolution when players go all-in."

        table = structures.Table(self.setup_players)

        with self.subTest('before going all-in'):
            self.assertTupleEqual(table.players, tuple(self.setup_players))
            self.assertTupleEqual(table.live_players, tuple(self.setup_players))
            self.assertTupleEqual(table.actionable_players, tuple(self.setup_players))
            self.assertTupleEqual(table.bettor_players, ())

        all_in_players: list[structures.Player] = []
        for player in self.setup_players:

            player.decrease_stack(1000)
            player.increase_bet_level(1000)
            all_in_players.append(player)

            with self.subTest('all-in', player=player.name):
                self.assertTupleEqual(table.players, tuple(self.setup_players))
                self.assertTupleEqual(table.live_players, tuple(self.setup_players))
                self.assertTupleEqual(table.actionable_players, tuple(p for p in self.setup_players if p not in all_in_players))
                self.assertTupleEqual(table.bettor_players, tuple(p for p in self.setup_players if p in all_in_players))


    def test_players_attributes_when_under_mixed_conditions(self):

        "Tests player arrays evolution when players do different things."

        table = structures.Table(self.setup_players)

        with self.subTest('before actions'):
            self.assertTupleEqual(table.players, tuple(self.setup_players))
            self.assertTupleEqual(table.live_players, tuple(self.setup_players))
            self.assertTupleEqual(table.actionable_players, tuple(self.setup_players))
            self.assertTupleEqual(table.bettor_players, ())

        for player in self.setup_players:

            if player in (self.Andy, self.Boa):
                player.decrease_stack(100)
                player.increase_bet_level(100)

            if player in (self.Coral, self.Dino):
                player.decrease_stack(1000)
                player.increase_bet_level(1000)

            if player in (self.Andy, self.Fomi):
                player.mark_is_folded()

        with self.subTest('after actions', player=player.name):
            self.assertTupleEqual(table.players, tuple(self.setup_players))
            self.assertTupleEqual(table.live_players, (self.Boa, self.Coral, self.Dino, self.Epa))
            self.assertTupleEqual(table.actionable_players, (self.Boa, self.Epa))
            self.assertTupleEqual(table.bettor_players, (self.Andy, self.Boa, self.Coral, self.Dino))


class TestTablePlayerIteration(BaseTestCase):


    "Runs unit tests on player iteration."


    def test_type_errors_in_players_related_methods(self):

        "Tests type error detection in iterator."

        table = structures.Table(self.setup_players)

        bad_players = (1, 'Andy')

        for bad_player in bad_players:

            with self.subTest(player=bad_player):
                with self.assertRaises(TypeError) as context:
                    table.iter_players(bad_player)
                self.assertEqual(context.exception.args[0], messages.msg_not_player_instance.format(type(bad_player).__name__))


    def test_value_error_in_player_related_methods(self):

        "Tests value error detection in iterator."

        table = structures.Table(self.setup_players)

        player_not_in_table = structures.Player('Zero', 1000)

        with self.subTest('player not in table'):
            with self.assertRaises(ValueError) as context:
                table.iter_players(player_not_in_table)
            self.assertEqual(context.exception.args[0], messages.msg_player_not_in_table.format(player_not_in_table.name))


    def test_forward_iteration_with_next_function(self):

        "Tests next function on generator, going forward."

        table = structures.Table(self.setup_players)

        generator = table.iter_players()
        for player in self.setup_players:
            with self.subTest('next on default starting player', expected_next=player.name):
                self.assertEqual(next(generator), player)
        with self.subTest('next on default starting player (stop iteration)'):
            with self.assertRaises(StopIteration) as context:
                next(generator)
            self.assertIsNone(context.exception.value)

        for i, starting_player in enumerate(self.setup_players):

            generator = table.iter_players(starting_player)
            for player in (*self.setup_players[i:], *self.setup_players[:i]):
                with self.subTest('next', starting=starting_player.name, expected_next=player.name):
                    self.assertEqual(next(generator), player)
            with self.subTest('next (stop iteration)', starting=starting_player):
                with self.assertRaises(StopIteration) as context:
                    next(generator)
                self.assertIsNone(context.exception.value)


    def test_backward_iteration_with_next_function(self):

        "Tests next function on generator, going backards."

        table = structures.Table(self.setup_players)

        generator = table.iter_players(reverse=True)
        for player in (self.setup_players[0], *self.setup_players[:0:-1]):
            with self.subTest('next on default starting player', expected_next=player.name):
                self.assertEqual(next(generator), player)
        with self.subTest('next on default starting player (stop iteration)'):
            with self.assertRaises(StopIteration) as context:
                next(generator)
            self.assertIsNone(context.exception.value)

        for i, starting_player in enumerate(self.setup_players):

            generator = table.iter_players(starting_player, reverse=True)
            for player in (*self.setup_players[i::-1], *self.setup_players[:i:-1]):
                with self.subTest('next', starting=starting_player.name, expected_next=player.name):
                    self.assertEqual(next(generator), player)
            with self.subTest('next (stop iteration)', starting=starting_player):
                with self.assertRaises(StopIteration) as context:
                    next(generator)
                self.assertIsNone(context.exception.value)


    def test_forward_iteration_with_for_loop(self):

        "Tests for loop on generator, going forward."

        table = structures.Table(self.setup_players)

        expected_iterable = self.setup_players
        actual_iterable = table.iter_players()
        for expected_player, actual_player in zip(expected_iterable, actual_iterable):
            with self.subTest('for loop on default starting player', expected_iter=expected_player.name):
                self.assertEqual(expected_player, actual_player)

        for i, starting_player in enumerate(self.setup_players):
            expected_iterable = (*self.setup_players[i:], *self.setup_players[:i])
            actual_iterable = table.iter_players(starting_player)
            for expected_player, actual_player in zip(expected_iterable, actual_iterable):
                with self.subTest('for loop', starting=starting_player.name, expected_iter=expected_player.name):
                    self.assertEqual(expected_player, actual_player)


    def test_backward_iteration_with_for_loop(self):

        "Tests for loop on generator, going backwards."

        table = structures.Table(self.setup_players)

        expected_iterable = (self.setup_players[0], *self.setup_players[:0:-1])
        actual_iterable = table.iter_players(reverse=True)
        for expected_player, actual_player in zip(expected_iterable, actual_iterable):
            with self.subTest('for loop on default starting player', expected_iter=expected_player.name):
                self.assertEqual(expected_player, actual_player)

        for i, starting_player in enumerate(self.setup_players):
            expected_iterable = (*self.setup_players[i::-1], *self.setup_players[:i:-1])
            actual_iterable = table.iter_players(starting_player, reverse=True)
            for expected_player, actual_player in zip(expected_iterable, actual_iterable):
                with self.subTest('for loop', starting=starting_player.name, expected_iter=expected_player.name):
                    self.assertEqual(expected_player, actual_player)


    def test_iteration_edge_cases(self):

        "Tests iterator under edge cases."

        player = structures.Player('Zero', 1000)
        table = structures.Table([player])

        generator = table.iter_players()
        with self.subTest('forward next on single player table', expected_next=player.name):
            self.assertEqual(next(generator), player)
        with self.subTest('forward next on single player table (stop iteration)'):
            with self.assertRaises(StopIteration) as context:
                next(generator)
            self.assertIsNone(context.exception.value)

        generator = table.iter_players(reverse=True)
        with self.subTest('backard next on single player table', expected_next=player.name):
            self.assertEqual(next(generator), player)
        with self.subTest('backard next on single player table (stop iteration)'):
            with self.assertRaises(StopIteration) as context:
                next(generator)
            self.assertIsNone(context.exception.value)

        for iterated_player in table.iter_players():
            with self.subTest('forward for loop on single player table', expected_iter=player.name):
                self.assertEqual(iterated_player, player)

        for iterated_player in table.iter_players(reverse=True):
            with self.subTest('backard for loop on single player table', expected_iter=player.name):
                self.assertEqual(iterated_player, player)


if __name__ == '__main__':
    main()