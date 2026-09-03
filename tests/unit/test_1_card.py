"""
Defines unit tests on Card class.
"""


import sys
sys.path.insert(0, '.')


from unittest import main, TestCase


from pokerpy import constants, messages, structures


class TestCardInstantiation(TestCase):


    "Runs unit tests on card instantiation."


    def test_value_type_errors(self):

        "Tests type error detection on field value."

        bad_values = (1, None)

        for bad_value in bad_values:

            with self.subTest(value=bad_value):
                with self.assertRaises(TypeError) as cm:
                    structures.Card(bad_value, constants.SPADES)
                self.assertEqual(cm.exception.args[0], messages.msg_not_str.format(type(bad_value).__name__))


    def test_suit_type_errors(self):

        "Tests type error detection on field suit."

        bad_suits = (1, None)

        for bad_suit in bad_suits:

            with self.subTest(suit=bad_suit):
                with self.assertRaises(TypeError) as cm:
                    structures.Card(constants.EIGHTS, bad_suit)
                self.assertEqual(cm.exception.args[0], messages.msg_not_str.format(type(bad_suit).__name__))


    def test_card_value_value_error(self):

        "Tests value error detection on card value."

        bad_values = (
            'aces', ## may be valid in the future
            'nines', ## may be valid in the future
            '10', ## may be valid in the future
            '1',
            '',
        )

        for bad_value in bad_values:

            with self.subTest(value=bad_value):
                with self.assertRaises(ValueError) as cm:
                    structures.Card(bad_value, constants.SPADES)
                self.assertEqual(cm.exception.args[0], messages.msg_invalid_card_value.format(', '.join(constants.sorted_card_values)))


    def test_card_suit_value_error(self):

        "Tests value error detection on card suit."

        bad_suits = (
            'spades', ## may be valid in the future
            'double_breasted',
            '',
        )

        for bad_suit in bad_suits:

            with self.subTest(suit=bad_suit):
                with self.assertRaises(ValueError) as cm:
                    structures.Card(constants.EIGHTS, bad_suit)
                self.assertEqual(cm.exception.args[0], messages.msg_invalid_card_suit.format(', '.join(constants.sorted_card_suits)))


    def test_joker_value_error(self):

        "Tests value error detection on joker card."

        joker = 'joker'

        with self.subTest('joker as value'):
            with self.assertRaises(ValueError) as cm:
                structures.Card(joker, constants.SPADES)
            self.assertEqual(cm.exception.args[0], messages.msg_wildcard)

        with self.subTest('joker as suit'):
            with self.assertRaises(ValueError) as cm:
                structures.Card(constants.ACES, 'joker')
            self.assertEqual(cm.exception.args[0], messages.msg_wildcard)


    def test_valid_instantiation(self):

        "Tests valid instantiation."

        for value, suit in constants.sorted_card_values_and_suits:

            card = structures.Card(value, suit)

            with self.subTest(card=str(card)):
                self.assertEqual(card.value, value)
                self.assertEqual(card.suit, suit)


    def test_value_uppercase_conversion(self):

        "Tests values are converted to uppercase."

        for value, suit in constants.sorted_card_values_and_suits:

            lowercase_value = value.lower()
            card = structures.Card(lowercase_value, suit)

            with self.subTest(value=lowercase_value, suit=suit):
                self.assertEqual(card.value, value)


    def test_suit_lowercase_conversion(self):

        "Tests suits are converted to lowercase."

        for value, suit in constants.sorted_card_values_and_suits:

            uppercase_suit = suit.upper()
            card = structures.Card(value, uppercase_suit)

            with self.subTest(value=value, suit=uppercase_suit):
                self.assertEqual(card.suit, suit)


class TestCardComparison(TestCase):


    "Runs unit tests on card comparison."


    def test_equal_and_not_equal_cards(self):

        "Tests cards are correctly compared equal or not equal."

        for value_1, suit_1 in constants.sorted_card_values_and_suits:

            for value_2, suit_2 in constants.sorted_card_values_and_suits:

                card_1 = structures.Card(value_1, suit_1)
                card_2 = structures.Card(value_2, suit_2)

                with self.subTest(card_1=str(card_1), card_2=str(card_2)):
                    if value_1 == value_2 and suit_1 == suit_2:
                        self.assertEqual(card_1, card_2)
                    else:
                        self.assertNotEqual(card_1, card_2)


class TestCardMethods(TestCase):


    "Runs unit tests on card methods."


    def test_get_deck_position_method(self):

        "Tests method get_deck_position."

        position = -1

        for value, suit in constants.sorted_card_values_and_suits:

            position += 1
            card = structures.Card(value, suit)

            with self.subTest(card=str(card), position=position):
                self.assertEqual(card.get_deck_position(), position)


if __name__ == '__main__':
    main()