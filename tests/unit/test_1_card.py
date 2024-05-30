"""
Defines unit tests on Card class.
"""


import sys
sys.path.insert(0, '.')


from unittest import main, TestCase


from pokerpy import constants, messages, structures


class TestCard(TestCase):


    """
    Runs unit tests on Card class.
    """


    def test_instantiation(self):


        """
        Runs test cases to check if cards stantiation works as expected.
        """


        # Resources

        invalid_card_value_full_message = messages.card_invalid_value_message.format(', '.join(constants.sorted_card_values))
        invalid_card_suit_full_message = messages.card_invalid_suit_message.format(', '.join(constants.sorted_card_suits))


        # The complete deck
        
        structures.Card('A', 's')
        structures.Card('A', 'h')
        structures.Card('A', 'd')
        structures.Card('A', 'c')
        structures.Card('K', 's')
        structures.Card('K', 'h')
        structures.Card('K', 'd')
        structures.Card('K', 'c')
        structures.Card('Q', 's')
        structures.Card('Q', 'h')
        structures.Card('Q', 'd')
        structures.Card('Q', 'c')
        structures.Card('J', 's')
        structures.Card('J', 'h')
        structures.Card('J', 'd')
        structures.Card('J', 'c')
        structures.Card('T', 's')
        structures.Card('T', 'h')
        structures.Card('T', 'd')
        structures.Card('T', 'c')
        structures.Card('9', 's')
        structures.Card('9', 'h')
        structures.Card('9', 'd')
        structures.Card('9', 'c')
        structures.Card('8', 's')
        structures.Card('8', 'h')
        structures.Card('8', 'd')
        structures.Card('8', 'c')
        structures.Card('7', 's')
        structures.Card('7', 'h')
        structures.Card('7', 'd')
        structures.Card('7', 'c')
        structures.Card('6', 's')
        structures.Card('6', 'h')
        structures.Card('6', 'd')
        structures.Card('6', 'c')
        structures.Card('5', 's')
        structures.Card('5', 'h')
        structures.Card('5', 'd')
        structures.Card('5', 'c')
        structures.Card('4', 's')
        structures.Card('4', 'h')
        structures.Card('4', 'd')
        structures.Card('4', 'c')
        structures.Card('3', 's')
        structures.Card('3', 'h')
        structures.Card('3', 'd')
        structures.Card('3', 'c')
        structures.Card('2', 's')
        structures.Card('2', 'h')
        structures.Card('2', 'd')
        structures.Card('2', 'c')


        # Valid cases with different upper and lower case parsing

        structures.Card('a', 's')
        structures.Card('k', 's')
        structures.Card('q', 's')
        structures.Card('j', 's')
        structures.Card('t', 's')
        structures.Card('A', 'S')
        structures.Card('A', 'H')
        structures.Card('A', 'D')
        structures.Card('A', 'C')
        structures.Card('a', 'S')
        structures.Card('k', 'H')
        structures.Card('q', 'D')
        structures.Card('j', 'C')
        structures.Card('t', 'S')


        # Invalid input types

        with self.assertRaises(TypeError) as cm:
            structures.Card(8, 's')
        self.assertEqual(cm.exception.args[0], messages.card_not_str_value_message.format(int.__name__))

        with self.assertRaises(TypeError) as cm:
            structures.Card('8', 1)
        self.assertEqual(cm.exception.args[0], messages.card_not_str_suit_message.format(int.__name__))


        # Invalid value parsings that may be valid in future

        with self.assertRaises(ValueError) as cm:
            structures.Card('aces', 's')
        self.assertEqual(cm.exception.args[0], invalid_card_value_full_message)

        with self.assertRaises(ValueError) as cm:
            structures.Card('kings', 's')
        self.assertEqual(cm.exception.args[0], invalid_card_value_full_message)

        with self.assertRaises(ValueError) as cm:
            structures.Card('queens', 's')
        self.assertEqual(cm.exception.args[0], invalid_card_value_full_message)

        with self.assertRaises(ValueError) as cm:
            structures.Card('jacks', 's')
        self.assertEqual(cm.exception.args[0], invalid_card_value_full_message)

        with self.assertRaises(ValueError) as cm:
            structures.Card('tens', 's')
        self.assertEqual(cm.exception.args[0], invalid_card_value_full_message)

        with self.assertRaises(ValueError) as cm:
            structures.Card('10', 's')
        self.assertEqual(cm.exception.args[0], invalid_card_value_full_message)

        with self.assertRaises(ValueError) as cm:
            structures.Card('nines', 's')
        self.assertEqual(cm.exception.args[0], invalid_card_value_full_message)

        with self.assertRaises(ValueError) as cm:
            structures.Card('eights', 's')
        self.assertEqual(cm.exception.args[0], invalid_card_value_full_message)

        with self.assertRaises(ValueError) as cm:
            structures.Card('sevens', 's')
        self.assertEqual(cm.exception.args[0], invalid_card_value_full_message)

        with self.assertRaises(ValueError) as cm:
            structures.Card('sixes', 's')
        self.assertEqual(cm.exception.args[0], invalid_card_value_full_message)

        with self.assertRaises(ValueError) as cm:
            structures.Card('fives', 's')
        self.assertEqual(cm.exception.args[0], invalid_card_value_full_message)

        with self.assertRaises(ValueError) as cm:
            structures.Card('fours', 's')
        self.assertEqual(cm.exception.args[0], invalid_card_value_full_message)

        with self.assertRaises(ValueError) as cm:
            structures.Card('threes', 's')
        self.assertEqual(cm.exception.args[0], invalid_card_value_full_message)

        with self.assertRaises(ValueError) as cm:
            structures.Card('deuces', 's')
        self.assertEqual(cm.exception.args[0], invalid_card_value_full_message)


        # Some invalid values NOT to be considered in future
        
        with self.assertRaises(ValueError) as cm:
            structures.Card('', 's')
        self.assertEqual(cm.exception.args[0], invalid_card_value_full_message)

        with self.assertRaises(ValueError) as cm:
            structures.Card('1', 's')
        self.assertEqual(cm.exception.args[0], invalid_card_value_full_message)

        with self.assertRaises(ValueError) as cm:
            structures.Card('11', 's')
        self.assertEqual(cm.exception.args[0], invalid_card_value_full_message)

        with self.assertRaises(ValueError) as cm:
            structures.Card('aces', 's')
        self.assertEqual(cm.exception.args[0], invalid_card_value_full_message)


        # Invalid suit parsings that may be valid in future

        with self.assertRaises(ValueError) as cm:
            structures.Card('A', 'spades')
        self.assertEqual(cm.exception.args[0], invalid_card_suit_full_message)

        with self.assertRaises(ValueError) as cm:
            structures.Card('A', 'hearts')
        self.assertEqual(cm.exception.args[0], invalid_card_suit_full_message)

        with self.assertRaises(ValueError) as cm:
            structures.Card('A', 'diamonds')
        self.assertEqual(cm.exception.args[0], invalid_card_suit_full_message)

        with self.assertRaises(ValueError) as cm:
            structures.Card('A', 'clubs')
        self.assertEqual(cm.exception.args[0], invalid_card_suit_full_message)


        # Invalid suits NOT to be considered in future

        with self.assertRaises(ValueError) as cm:
            structures.Card('A', 'a')
        self.assertEqual(cm.exception.args[0], invalid_card_suit_full_message)

        with self.assertRaises(ValueError) as cm:
            structures.Card('A', '')
        self.assertEqual(cm.exception.args[0], invalid_card_suit_full_message)

        with self.assertRaises(ValueError) as cm:
            structures.Card('A', 'swords')
        self.assertEqual(cm.exception.args[0], invalid_card_suit_full_message)

        with self.assertRaises(ValueError) as cm:
            structures.Card('A', 'cups')
        self.assertEqual(cm.exception.args[0], invalid_card_suit_full_message)

        with self.assertRaises(ValueError) as cm:
            structures.Card('A', 'coins')
        self.assertEqual(cm.exception.args[0], invalid_card_suit_full_message)


        # Just kidding

        with self.assertRaises(ValueError) as cm:
            structures.Card('joker', 's')
        self.assertEqual(cm.exception.args[0], messages.card_joker_message)

        with self.assertRaises(ValueError) as cm:
            structures.Card('joker', 'whatever')
        self.assertEqual(cm.exception.args[0], messages.card_joker_message)

        with self.assertRaises(ValueError) as cm:
            structures.Card('A', 'joker')
        self.assertEqual(cm.exception.args[0], messages.card_joker_message)

        with self.assertRaises(ValueError) as cm:
            structures.Card('whatever', 'joker')
        self.assertEqual(cm.exception.args[0], messages.card_joker_message)

        with self.assertRaises(ValueError) as cm:
            structures.Card('joker', 'joker')
        self.assertEqual(cm.exception.args[0], messages.card_joker_message)


    def test_comparison(self):


        """
        Runs test cases to check if cards compare to each other as expected.
        """


        # Some equal cards
        
        self.assertEqual(structures.Card('A', 's'), structures.Card('A', 's'))
        self.assertEqual(structures.Card('K', 'h'), structures.Card('K', 'h'))
        self.assertEqual(structures.Card('Q', 'd'), structures.Card('Q', 'd'))
        self.assertEqual(structures.Card('J', 'c'), structures.Card('J', 'c'))


        # Some cards with same values but different suits

        self.assertNotEqual(structures.Card('T', 's'), structures.Card('T', 'h'))
        self.assertNotEqual(structures.Card('9', 'h'), structures.Card('9', 'd'))
        self.assertNotEqual(structures.Card('8', 'd'), structures.Card('8', 'c'))
        self.assertNotEqual(structures.Card('7', 'c'), structures.Card('7', 's'))


        # Some cards with different values but same suits

        self.assertNotEqual(structures.Card('6', 's'), structures.Card('5', 's'))
        self.assertNotEqual(structures.Card('5', 'h'), structures.Card('4', 'h'))
        self.assertNotEqual(structures.Card('4', 'd'), structures.Card('3', 'd'))
        self.assertNotEqual(structures.Card('3', 'c'), structures.Card('2', 'c'))


        # Some cards with different values and suits

        self.assertNotEqual(structures.Card('A', 's'), structures.Card('K', 'h'))
        self.assertNotEqual(structures.Card('T', 'h'), structures.Card('9', 'd'))
        self.assertNotEqual(structures.Card('6', 'd'), structures.Card('5', 'c'))
        self.assertNotEqual(structures.Card('2', 'c'), structures.Card('A', 's'))


    def test_get_deck_position_method(self):


        """
        Runs all test cases on method get_deck_position.
        """


        self.assertEqual(structures.Card('A', 's').get_deck_position(), 51)
        self.assertEqual(structures.Card('A', 'h').get_deck_position(), 50)
        self.assertEqual(structures.Card('A', 'd').get_deck_position(), 49)
        self.assertEqual(structures.Card('A', 'c').get_deck_position(), 48)
        self.assertEqual(structures.Card('K', 's').get_deck_position(), 47)
        self.assertEqual(structures.Card('K', 'h').get_deck_position(), 46)
        self.assertEqual(structures.Card('K', 'd').get_deck_position(), 45)
        self.assertEqual(structures.Card('K', 'c').get_deck_position(), 44)
        self.assertEqual(structures.Card('Q', 's').get_deck_position(), 43)
        self.assertEqual(structures.Card('Q', 'h').get_deck_position(), 42)
        self.assertEqual(structures.Card('Q', 'd').get_deck_position(), 41)
        self.assertEqual(structures.Card('Q', 'c').get_deck_position(), 40)
        self.assertEqual(structures.Card('J', 's').get_deck_position(), 39)
        self.assertEqual(structures.Card('J', 'h').get_deck_position(), 38)
        self.assertEqual(structures.Card('J', 'd').get_deck_position(), 37)
        self.assertEqual(structures.Card('J', 'c').get_deck_position(), 36)
        self.assertEqual(structures.Card('T', 's').get_deck_position(), 35)
        self.assertEqual(structures.Card('T', 'h').get_deck_position(), 34)
        self.assertEqual(structures.Card('T', 'd').get_deck_position(), 33)
        self.assertEqual(structures.Card('T', 'c').get_deck_position(), 32)
        self.assertEqual(structures.Card('9', 's').get_deck_position(), 31)
        self.assertEqual(structures.Card('9', 'h').get_deck_position(), 30)
        self.assertEqual(structures.Card('9', 'd').get_deck_position(), 29)
        self.assertEqual(structures.Card('9', 'c').get_deck_position(), 28)
        self.assertEqual(structures.Card('8', 's').get_deck_position(), 27)
        self.assertEqual(structures.Card('8', 'h').get_deck_position(), 26)
        self.assertEqual(structures.Card('8', 'd').get_deck_position(), 25)
        self.assertEqual(structures.Card('8', 'c').get_deck_position(), 24)
        self.assertEqual(structures.Card('7', 's').get_deck_position(), 23)
        self.assertEqual(structures.Card('7', 'h').get_deck_position(), 22)
        self.assertEqual(structures.Card('7', 'd').get_deck_position(), 21)
        self.assertEqual(structures.Card('7', 'c').get_deck_position(), 20)
        self.assertEqual(structures.Card('6', 's').get_deck_position(), 19)
        self.assertEqual(structures.Card('6', 'h').get_deck_position(), 18)
        self.assertEqual(structures.Card('6', 'd').get_deck_position(), 17)
        self.assertEqual(structures.Card('6', 'c').get_deck_position(), 16)
        self.assertEqual(structures.Card('5', 's').get_deck_position(), 15)
        self.assertEqual(structures.Card('5', 'h').get_deck_position(), 14)
        self.assertEqual(structures.Card('5', 'd').get_deck_position(), 13)
        self.assertEqual(structures.Card('5', 'c').get_deck_position(), 12)
        self.assertEqual(structures.Card('4', 's').get_deck_position(), 11)
        self.assertEqual(structures.Card('4', 'h').get_deck_position(), 10)
        self.assertEqual(structures.Card('4', 'd').get_deck_position(), 9)
        self.assertEqual(structures.Card('4', 'c').get_deck_position(), 8)
        self.assertEqual(structures.Card('3', 's').get_deck_position(), 7)
        self.assertEqual(structures.Card('3', 'h').get_deck_position(), 6)
        self.assertEqual(structures.Card('3', 'd').get_deck_position(), 5)
        self.assertEqual(structures.Card('3', 'c').get_deck_position(), 4)
        self.assertEqual(structures.Card('2', 's').get_deck_position(), 3)
        self.assertEqual(structures.Card('2', 'h').get_deck_position(), 2)
        self.assertEqual(structures.Card('2', 'd').get_deck_position(), 1)
        self.assertEqual(structures.Card('2', 'c').get_deck_position(), 0)


if __name__ == '__main__':
    main()