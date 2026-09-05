"""
Defines unit tests on Player class.
"""


import sys
sys.path.insert(0, '.')


from decimal import Decimal
from unittest import main, TestCase


from pokerpy import constants, messages, structures


class TestPlayerInstantiation(TestCase):


    "Runs unit tests on player instantiation."


    def test_name_type_errors(self):

        "Tests type error detection on field name."

        bad_names = (1, None)

        for bad_name in bad_names:

            with self.subTest(name=bad_name):
                with self.assertRaises(TypeError) as context:
                    structures.Player(name=bad_name, stack=1000)
                self.assertEqual(context.exception.args[0], messages.msg_not_str.format(type(bad_name).__name__))


    def test_stack_type_errors(self):

        "Tests type error detection on field stack."

        bad_stacks = ('1000', 1000.0, Decimal('1000'), None)

        for bad_stack in bad_stacks:

            with self.subTest(stack=bad_stack):
                with self.assertRaises(TypeError) as context:
                    structures.Player(name='Andy', stack=bad_stack)
                self.assertEqual(context.exception.args[0], messages.msg_not_int.format(type(bad_stack).__name__))


    def test_valid_player_instantiation(self):

        "Tests valid player instantiation."

        player = structures.Player('Andy', 1000)
        self.assertEqual(player.name, 'Andy')
        self.assertEqual(player.cards, ())
        self.assertIsNone(player.hand)
        self.assertIsNone(player.requested_action)
        self.assertEqual(player.stack, 1000)
        self.assertEqual(player.bet_level, 0)
        self.assertEqual(player.pot_index, 0)
        self.assertFalse(player.is_folded)
        self.assertFalse(player.has_played)


class TestPlayerActionMethods(TestCase):


    "Runs unit tests on player methods related to the requested action."


    def test_action_methods_type_errors(self):

        "Tests type error detection in methods related to the requested action."

        player = structures.Player('Andy', stack=1000)

        bad_actions = (1, 'drink', None)

        for bad_action in bad_actions:

            with self.subTest(action=bad_action):
                with self.assertRaises(TypeError) as context:
                    player.request_action(bad_action)
                self.assertEqual(context.exception.args[0], messages.msg_not_action_instance.format(type(bad_action).__name__))


    def test_action_methods_valid_input(self):

        "Tests valid input in methods related to requested action."

        actions = (
            structures.Action(constants.ACTION_FOLD, 0),
            structures.Action(constants.ACTION_CHECK, 0),
            structures.Action(constants.ACTION_CALL, 100),
            structures.Action(constants.ACTION_BET, 100),
            structures.Action(constants.ACTION_RAISE, 100),
        )

        for action in actions:
            player = structures.Player('Andy', 1000)
            with self.subTest('before request', action=str(action)):
                self.assertIsNone(player.requested_action)
            player.request_action(action)
            with self.subTest('after request', action=str(action)):
                self.assertEqual(player.requested_action, action)
            player.clear_action()
            with self.subTest('after clear', action=str(action)):
                self.assertIsNone(player.requested_action)


class TestPlayerCardMethods(TestCase):


    "Runs unit tests on player methods related to the cards."


    def test_card_methods_type_errors(self):

        "Tests type error detection in methods related to the cards."

        player = structures.Player('Andy', stack=1000)

        bad_cards = (1, 'the_tower', None)

        for bad_card in bad_cards:

            with self.subTest(card=bad_card):
                with self.assertRaises(TypeError) as context:
                    player.assign_card(bad_card)
                self.assertEqual(context.exception.args[0], messages.msg_not_card_instance.format(type(bad_card).__name__))


    def test_card_methods_value_errors(self):

        "Tests value error detection in methods related to the cards."

        player = structures.Player('Andy', stack=1000)        
        player.assign_card(structures.Card(constants.ACES, constants.SPADES))

        with self.subTest('repeated card'):
            with self.assertRaises(ValueError) as context:
                player.assign_card(structures.Card(constants.ACES, constants.SPADES))
            self.assertEqual(context.exception.args[0], messages.msg_repeated_cards)


    def test_card_methods_valid_input(self):

        "Tests valid input in methods related to the cards."

        cards = (
            structures.Card(constants.ACES, constants.SPADES),
            structures.Card(constants.ACES, constants.CLUBS),
            structures.Card(constants.SEVENS, constants.CLUBS),
        )

        player = structures.Player('Andy', 1000)

        with self.subTest('before card assignment'):
            self.assertTupleEqual(player.cards, ())

        for i, card in enumerate(cards):
            player.assign_card(card)
            with self.subTest('assignment', card=str(card)):
                self.assertTupleEqual(player.cards, cards[:i+1])

        player.reset_cards()
        with self.subTest('after card reset'):
            self.assertTupleEqual(player.cards, ())


class TestPlayerHandMethods(TestCase):


    "Runs unit tests on player methods related to the hand."


    def test_card_methods_type_errors(self):

        "Tests type error detection in methods related to the hand."

        player = structures.Player('Andy', stack=1000)
        cards = (
            king_of_spades := structures.Card(constants.KINGS, constants.SPADES),
            structures.Card(constants.KINGS, constants.HEARTS),
            structures.Card(constants.KINGS, constants.DIAMONDS),
            structures.Card(constants.KINGS, constants.CLUBS),
            structures.Card(constants.ACES, constants.DIAMONDS),
        )

        bad_hands = (1, 'left_hand', king_of_spades, cards, None)

        for bad_hand in bad_hands:

            with self.subTest(hand=bad_hand):
                with self.assertRaises(TypeError) as context:
                    player.assign_hand(bad_hand)
                self.assertEqual(context.exception.args[0], messages.msg_not_hand_instance.format(type(bad_hand).__name__))


    def test_hand_methods_valid_input(self):

        "Tests valid input in methods related to the hand."

        royal_flush = structures.Hand((
            structures.Card(constants.ACES, constants.SPADES),
            structures.Card(constants.KINGS, constants.SPADES),
            structures.Card(constants.QUEENS, constants.SPADES),
            structures.Card(constants.JACKS, constants.SPADES),
            structures.Card(constants.TENS, constants.SPADES),
        ))

        four_of_a_kind = structures.Hand((
            structures.Card(constants.KINGS, constants.SPADES),
            structures.Card(constants.KINGS, constants.HEARTS),
            structures.Card(constants.KINGS, constants.DIAMONDS),
            structures.Card(constants.KINGS, constants.CLUBS),
            structures.Card(constants.ACES, constants.DIAMONDS),
        ))

        for hand in (royal_flush, four_of_a_kind):
            player = structures.Player('Andy', 1000)
            with self.subTest('before assignment', hand=str(hand)):
                self.assertIsNone(player.hand)
            player.assign_hand(hand)
            with self.subTest('after assignment', hand=str(hand)):
                self.assertEqual(player.hand, hand)
            player.clear_hand()
            with self.subTest('after clear', hand=str(hand)):
                self.assertIsNone(player.hand)


class TestPlayerBetLevelMethods(TestCase):


    "Runs unit tests on player methods related to the bet level."


    def test_bet_level_methods_type_errors(self):

        "Tests type error detection in methods related to the bet level."

        player = structures.Player('Andy', stack=1000)

        bad_amounts = ('300', 300.0, Decimal('300'), None)

        for bad_amount in bad_amounts:

            with self.subTest('increase', amount=bad_amount):
                with self.assertRaises(TypeError) as context:
                    player.increase_bet_level(bad_amount)
                self.assertEqual(context.exception.args[0], messages.msg_not_int.format(type(bad_amount).__name__))

            with self.subTest('decrease', amount=bad_amount):
                with self.assertRaises(TypeError) as context:
                    player.decrease_bet_level(bad_amount)
                self.assertEqual(context.exception.args[0], messages.msg_not_int.format(type(bad_amount).__name__))


    def test_bet_level_methods_value_errors(self):

        "Tests value error detection in methods related to the bet level."

        player = structures.Player('Andy', stack=1000)        

        bad_amount = -100
        with self.subTest('negative increase amount', amount=bad_amount):
            with self.assertRaises(ValueError) as context:
                player.increase_bet_level(bad_amount)
            self.assertEqual(context.exception.args[0], messages.msg_not_positive_or_zero_value.format(bad_amount))

        bad_amount = -100
        with self.subTest('negative decrease amount', amount=bad_amount):
            with self.assertRaises(ValueError) as context:
                player.decrease_bet_level(bad_amount)
            self.assertEqual(context.exception.args[0], messages.msg_not_positive_or_zero_value.format(bad_amount))

        bad_amount = 1
        with self.subTest('decrease amount larger than bet level', amount=bad_amount):
            with self.assertRaises(ValueError) as context:
                player.decrease_bet_level(bad_amount)
            self.assertEqual(context.exception.args[0], messages.msg_amount_larger_than_bet_level.format(bad_amount, 0))


    def test_bet_level_methods_valid_input(self):

        "Tests valid input in methods related to the bet level."

        amounts = (50, 100, 150, 200)

        player = structures.Player('Andy', 1000)

        with self.subTest('before amount increase'):
            self.assertEqual(player.bet_level, 0)

        for i, amount in enumerate(amounts):
            player.increase_bet_level(amount)
            with self.subTest('increase', amount=amount):
                self.assertEqual(player.bet_level, sum(amounts[:i+1]))

        for i, amount in enumerate(amounts):
            player.decrease_bet_level(amount)
            with self.subTest('decrease', amount=amount):
                self.assertEqual(player.bet_level, sum(amounts[i+1:]))


class TestPlayerStackMethods(TestCase):


    "Runs unit tests on player methods related to the stack."


    def test_stack_methods_type_errors(self):

        "Tests type error detection in methods related to the stack."

        player = structures.Player('Andy', stack=1000)

        bad_amounts = ('300', 300.0, Decimal('300'), None)

        for bad_amount in bad_amounts:

            with self.subTest('increase', amount=bad_amount):
                with self.assertRaises(TypeError) as context:
                    player.increase_stack(bad_amount)
                self.assertEqual(context.exception.args[0], messages.msg_not_int.format(type(bad_amount).__name__))

            with self.subTest('decrease', amount=bad_amount):
                with self.assertRaises(TypeError) as context:
                    player.decrease_stack(bad_amount)
                self.assertEqual(context.exception.args[0], messages.msg_not_int.format(type(bad_amount).__name__))


    def test_stack_methods_value_errors(self):

        "Tests value error detection in methods related to the stack."

        stack = 1000
        player = structures.Player('Andy', stack=stack)        

        bad_amount = -100
        with self.subTest('negative increase amount', amount=bad_amount):
            with self.assertRaises(ValueError) as context:
                player.increase_stack(bad_amount)
            self.assertEqual(context.exception.args[0], messages.msg_not_positive_or_zero_value.format(bad_amount))

        bad_amount = -100
        with self.subTest('negative decrease amount', amount=bad_amount):
            with self.assertRaises(ValueError) as context:
                player.decrease_stack(bad_amount)
            self.assertEqual(context.exception.args[0], messages.msg_not_positive_or_zero_value.format(bad_amount))

        bad_amount = 1001
        with self.subTest('decrease amount larger than stack', amount=bad_amount):
            with self.assertRaises(ValueError) as context:
                player.decrease_stack(bad_amount)
            self.assertEqual(context.exception.args[0], messages.msg_amount_larger_than_stack.format(bad_amount, stack))


    def test_stack_methods_valid_input(self):

        "Tests valid input in methods related to the stack."

        amounts = (50, 100, 150, 200)

        initial_stack = 1000
        player = structures.Player('Andy', initial_stack)

        with self.subTest('before stack increase'):
            self.assertEqual(player.stack, initial_stack)

        for i, amount in enumerate(amounts):
            player.increase_stack(amount)
            with self.subTest('increase', amount=amount):
                self.assertEqual(player.stack, (initial_stack + sum(amounts[:i+1])))

        for i, amount in enumerate(amounts):
            player.decrease_stack(amount)
            with self.subTest('decrease', amount=amount):
                self.assertEqual(player.stack, (initial_stack + sum(amounts[i+1:])))


class TestPlayerPotIndexMethods(TestCase):


    "Runs unit tests on player methods related to the pot index."


    def test_pot_participation_methods_valid_input(self):

        "Tests valid input in methods related to the pot participation."

        player = structures.Player('Andy', 1000)

        with self.subTest('before pot index increase'):
            self.assertEqual(player.pot_index, 0)

        for i in range(1, 6):
            player.increase_pot_index()
            with self.subTest('increase', count=i):
                self.assertEqual(player.pot_index, i)

        player.reset_pot_index()
        with self.subTest('after pot index clear'):
            self.assertEqual(player.pot_index, 0)


class TestPlayerBooleanMethods(TestCase):


    "Runs unit tests on player methods related to boolean attributes."


    def test_is_folded(self):

        "Tests status update in attribute is_folded."

        player = structures.Player('Andy', 1000)

        self.assertFalse(player.is_folded)
        player.mark_is_folded()
        self.assertTrue(player.is_folded)
        player.unmark_is_folded()
        self.assertFalse(player.is_folded)


    def test_has_played(self):

        "Tests status update in attribute has_played."

        player = structures.Player('Andy', 1000)

        self.assertFalse(player.has_played)
        player.mark_has_played()
        self.assertTrue(player.has_played)
        player.unmark_has_played()
        self.assertFalse(player.has_played)


if __name__ == '__main__':
    main()