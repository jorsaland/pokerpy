"""
Defines unit tests on Card class.
"""


import sys
sys.path.insert(0, '.')


from unittest import main, TestCase


import pokerpy as pk


class TestCard(TestCase):


    """
    Runs unit tests on Card class.
    """


    def test_instantiation(self):


        """
        Runs test cases to check if cards stantiation works as expected.
        """


        # Resources

        invalid_card_value_full_message = pk.messages.invalid_card_value_message.format(', '.join(pk.sorted_card_values))
        invalid_card_suit_full_message = pk.messages.invalid_card_suit_message.format(', '.join(pk.sorted_card_suits))


        # The complete deck
        
        pk.Card('A', 's')
        pk.Card('A', 'h')
        pk.Card('A', 'd')
        pk.Card('A', 'c')
        pk.Card('K', 's')
        pk.Card('K', 'h')
        pk.Card('K', 'd')
        pk.Card('K', 'c')
        pk.Card('Q', 's')
        pk.Card('Q', 'h')
        pk.Card('Q', 'd')
        pk.Card('Q', 'c')
        pk.Card('J', 's')
        pk.Card('J', 'h')
        pk.Card('J', 'd')
        pk.Card('J', 'c')
        pk.Card('T', 's')
        pk.Card('T', 'h')
        pk.Card('T', 'd')
        pk.Card('T', 'c')
        pk.Card('9', 's')
        pk.Card('9', 'h')
        pk.Card('9', 'd')
        pk.Card('9', 'c')
        pk.Card('8', 's')
        pk.Card('8', 'h')
        pk.Card('8', 'd')
        pk.Card('8', 'c')
        pk.Card('7', 's')
        pk.Card('7', 'h')
        pk.Card('7', 'd')
        pk.Card('7', 'c')
        pk.Card('6', 's')
        pk.Card('6', 'h')
        pk.Card('6', 'd')
        pk.Card('6', 'c')
        pk.Card('5', 's')
        pk.Card('5', 'h')
        pk.Card('5', 'd')
        pk.Card('5', 'c')
        pk.Card('4', 's')
        pk.Card('4', 'h')
        pk.Card('4', 'd')
        pk.Card('4', 'c')
        pk.Card('3', 's')
        pk.Card('3', 'h')
        pk.Card('3', 'd')
        pk.Card('3', 'c')
        pk.Card('2', 's')
        pk.Card('2', 'h')
        pk.Card('2', 'd')
        pk.Card('2', 'c')


        # Valid cases with different upper and lower case parsing

        pk.Card('a', 's')
        pk.Card('k', 's')
        pk.Card('q', 's')
        pk.Card('j', 's')
        pk.Card('t', 's')
        pk.Card('A', 'S')
        pk.Card('A', 'H')
        pk.Card('A', 'D')
        pk.Card('A', 'C')
        pk.Card('a', 'S')
        pk.Card('k', 'H')
        pk.Card('q', 'D')
        pk.Card('j', 'C')
        pk.Card('t', 'S')


        # Invalid input types

        with self.assertRaises(TypeError) as cm:
            pk.Card(8, 's')
        self.assertEqual(cm.exception.args[0], pk.messages.not_str_card_value_message.format(int.__name__))

        with self.assertRaises(TypeError) as cm:
            pk.Card('8', 1)
        self.assertEqual(cm.exception.args[0], pk.messages.not_str_card_suit_message.format(int.__name__))


        # Invalid value parsings that may be valid in future

        with self.assertRaises(ValueError) as cm:
            pk.Card('aces', 's')
        self.assertEqual(cm.exception.args[0], invalid_card_value_full_message)

        with self.assertRaises(ValueError) as cm:
            pk.Card('kings', 's')
        self.assertEqual(cm.exception.args[0], invalid_card_value_full_message)

        with self.assertRaises(ValueError) as cm:
            pk.Card('queens', 's')
        self.assertEqual(cm.exception.args[0], invalid_card_value_full_message)

        with self.assertRaises(ValueError) as cm:
            pk.Card('jacks', 's')
        self.assertEqual(cm.exception.args[0], invalid_card_value_full_message)

        with self.assertRaises(ValueError) as cm:
            pk.Card('tens', 's')
        self.assertEqual(cm.exception.args[0], invalid_card_value_full_message)

        with self.assertRaises(ValueError) as cm:
            pk.Card('10', 's')
        self.assertEqual(cm.exception.args[0], invalid_card_value_full_message)

        with self.assertRaises(ValueError) as cm:
            pk.Card('nines', 's')
        self.assertEqual(cm.exception.args[0], invalid_card_value_full_message)

        with self.assertRaises(ValueError) as cm:
            pk.Card('eights', 's')
        self.assertEqual(cm.exception.args[0], invalid_card_value_full_message)

        with self.assertRaises(ValueError) as cm:
            pk.Card('sevens', 's')
        self.assertEqual(cm.exception.args[0], invalid_card_value_full_message)

        with self.assertRaises(ValueError) as cm:
            pk.Card('sixes', 's')
        self.assertEqual(cm.exception.args[0], invalid_card_value_full_message)

        with self.assertRaises(ValueError) as cm:
            pk.Card('fives', 's')
        self.assertEqual(cm.exception.args[0], invalid_card_value_full_message)

        with self.assertRaises(ValueError) as cm:
            pk.Card('fours', 's')
        self.assertEqual(cm.exception.args[0], invalid_card_value_full_message)

        with self.assertRaises(ValueError) as cm:
            pk.Card('threes', 's')
        self.assertEqual(cm.exception.args[0], invalid_card_value_full_message)

        with self.assertRaises(ValueError) as cm:
            pk.Card('deuces', 's')
        self.assertEqual(cm.exception.args[0], invalid_card_value_full_message)


        # Some invalid values NOT to be considered in future
        
        with self.assertRaises(ValueError) as cm:
            pk.Card('', 's')
        self.assertEqual(cm.exception.args[0], invalid_card_value_full_message)

        with self.assertRaises(ValueError) as cm:
            pk.Card('1', 's')
        self.assertEqual(cm.exception.args[0], invalid_card_value_full_message)

        with self.assertRaises(ValueError) as cm:
            pk.Card('11', 's')
        self.assertEqual(cm.exception.args[0], invalid_card_value_full_message)

        with self.assertRaises(ValueError) as cm:
            pk.Card('aces', 's')
        self.assertEqual(cm.exception.args[0], invalid_card_value_full_message)


        # Invalid suit parsings that may be valid in future

        with self.assertRaises(ValueError) as cm:
            pk.Card('A', 'spades')
        self.assertEqual(cm.exception.args[0], invalid_card_suit_full_message)

        with self.assertRaises(ValueError) as cm:
            pk.Card('A', 'hearts')
        self.assertEqual(cm.exception.args[0], invalid_card_suit_full_message)

        with self.assertRaises(ValueError) as cm:
            pk.Card('A', 'diamonds')
        self.assertEqual(cm.exception.args[0], invalid_card_suit_full_message)

        with self.assertRaises(ValueError) as cm:
            pk.Card('A', 'clubs')
        self.assertEqual(cm.exception.args[0], invalid_card_suit_full_message)


        # Invalid suits NOT to be considered in future

        with self.assertRaises(ValueError) as cm:
            pk.Card('A', 'a')
        self.assertEqual(cm.exception.args[0], invalid_card_suit_full_message)

        with self.assertRaises(ValueError) as cm:
            pk.Card('A', '')
        self.assertEqual(cm.exception.args[0], invalid_card_suit_full_message)

        with self.assertRaises(ValueError) as cm:
            pk.Card('A', 'swords')
        self.assertEqual(cm.exception.args[0], invalid_card_suit_full_message)

        with self.assertRaises(ValueError) as cm:
            pk.Card('A', 'cups')
        self.assertEqual(cm.exception.args[0], invalid_card_suit_full_message)

        with self.assertRaises(ValueError) as cm:
            pk.Card('A', 'coins')
        self.assertEqual(cm.exception.args[0], invalid_card_suit_full_message)


        # Just kidding

        with self.assertRaises(ValueError) as cm:
            pk.Card('joker', 's')
        self.assertEqual(cm.exception.args[0], pk.messages.joker_card_message)

        with self.assertRaises(ValueError) as cm:
            pk.Card('joker', 'whatever')
        self.assertEqual(cm.exception.args[0], pk.messages.joker_card_message)

        with self.assertRaises(ValueError) as cm:
            pk.Card('A', 'joker')
        self.assertEqual(cm.exception.args[0], pk.messages.joker_card_message)

        with self.assertRaises(ValueError) as cm:
            pk.Card('whatever', 'joker')
        self.assertEqual(cm.exception.args[0], pk.messages.joker_card_message)

        with self.assertRaises(ValueError) as cm:
            pk.Card('joker', 'joker')
        self.assertEqual(cm.exception.args[0], pk.messages.joker_card_message)


    def test_comparison(self):


        """
        Runs test cases to check if cards compare to each other as expected.
        """


        # Some equal cards
        
        self.assertEqual(pk.Card('A', 's'), pk.Card('A', 's'))
        self.assertEqual(pk.Card('K', 'h'), pk.Card('K', 'h'))
        self.assertEqual(pk.Card('Q', 'd'), pk.Card('Q', 'd'))
        self.assertEqual(pk.Card('J', 'c'), pk.Card('J', 'c'))


        # Some cards with same values but different suits

        self.assertNotEqual(pk.Card('T', 's'), pk.Card('T', 'h'))
        self.assertNotEqual(pk.Card('9', 'h'), pk.Card('9', 'd'))
        self.assertNotEqual(pk.Card('8', 'd'), pk.Card('8', 'c'))
        self.assertNotEqual(pk.Card('7', 'c'), pk.Card('7', 's'))


        # Some cards with different values but same suits

        self.assertNotEqual(pk.Card('6', 's'), pk.Card('5', 's'))
        self.assertNotEqual(pk.Card('5', 'h'), pk.Card('4', 'h'))
        self.assertNotEqual(pk.Card('4', 'd'), pk.Card('3', 'd'))
        self.assertNotEqual(pk.Card('3', 'c'), pk.Card('2', 'c'))


        # Some cards with different values and suits

        self.assertNotEqual(pk.Card('A', 's'), pk.Card('K', 'h'))
        self.assertNotEqual(pk.Card('T', 'h'), pk.Card('9', 'd'))
        self.assertNotEqual(pk.Card('6', 'd'), pk.Card('5', 'c'))
        self.assertNotEqual(pk.Card('2', 'c'), pk.Card('A', 's'))


    def test_get_deck_position_method(self):


        """
        Runs all test cases on method get_deck_position.
        """


        self.assertEqual(pk.Card('A', 's').get_deck_position(), 51)
        self.assertEqual(pk.Card('A', 'h').get_deck_position(), 50)
        self.assertEqual(pk.Card('A', 'd').get_deck_position(), 49)
        self.assertEqual(pk.Card('A', 'c').get_deck_position(), 48)
        self.assertEqual(pk.Card('K', 's').get_deck_position(), 47)
        self.assertEqual(pk.Card('K', 'h').get_deck_position(), 46)
        self.assertEqual(pk.Card('K', 'd').get_deck_position(), 45)
        self.assertEqual(pk.Card('K', 'c').get_deck_position(), 44)
        self.assertEqual(pk.Card('Q', 's').get_deck_position(), 43)
        self.assertEqual(pk.Card('Q', 'h').get_deck_position(), 42)
        self.assertEqual(pk.Card('Q', 'd').get_deck_position(), 41)
        self.assertEqual(pk.Card('Q', 'c').get_deck_position(), 40)
        self.assertEqual(pk.Card('J', 's').get_deck_position(), 39)
        self.assertEqual(pk.Card('J', 'h').get_deck_position(), 38)
        self.assertEqual(pk.Card('J', 'd').get_deck_position(), 37)
        self.assertEqual(pk.Card('J', 'c').get_deck_position(), 36)
        self.assertEqual(pk.Card('T', 's').get_deck_position(), 35)
        self.assertEqual(pk.Card('T', 'h').get_deck_position(), 34)
        self.assertEqual(pk.Card('T', 'd').get_deck_position(), 33)
        self.assertEqual(pk.Card('T', 'c').get_deck_position(), 32)
        self.assertEqual(pk.Card('9', 's').get_deck_position(), 31)
        self.assertEqual(pk.Card('9', 'h').get_deck_position(), 30)
        self.assertEqual(pk.Card('9', 'd').get_deck_position(), 29)
        self.assertEqual(pk.Card('9', 'c').get_deck_position(), 28)
        self.assertEqual(pk.Card('8', 's').get_deck_position(), 27)
        self.assertEqual(pk.Card('8', 'h').get_deck_position(), 26)
        self.assertEqual(pk.Card('8', 'd').get_deck_position(), 25)
        self.assertEqual(pk.Card('8', 'c').get_deck_position(), 24)
        self.assertEqual(pk.Card('7', 's').get_deck_position(), 23)
        self.assertEqual(pk.Card('7', 'h').get_deck_position(), 22)
        self.assertEqual(pk.Card('7', 'd').get_deck_position(), 21)
        self.assertEqual(pk.Card('7', 'c').get_deck_position(), 20)
        self.assertEqual(pk.Card('6', 's').get_deck_position(), 19)
        self.assertEqual(pk.Card('6', 'h').get_deck_position(), 18)
        self.assertEqual(pk.Card('6', 'd').get_deck_position(), 17)
        self.assertEqual(pk.Card('6', 'c').get_deck_position(), 16)
        self.assertEqual(pk.Card('5', 's').get_deck_position(), 15)
        self.assertEqual(pk.Card('5', 'h').get_deck_position(), 14)
        self.assertEqual(pk.Card('5', 'd').get_deck_position(), 13)
        self.assertEqual(pk.Card('5', 'c').get_deck_position(), 12)
        self.assertEqual(pk.Card('4', 's').get_deck_position(), 11)
        self.assertEqual(pk.Card('4', 'h').get_deck_position(), 10)
        self.assertEqual(pk.Card('4', 'd').get_deck_position(), 9)
        self.assertEqual(pk.Card('4', 'c').get_deck_position(), 8)
        self.assertEqual(pk.Card('3', 's').get_deck_position(), 7)
        self.assertEqual(pk.Card('3', 'h').get_deck_position(), 6)
        self.assertEqual(pk.Card('3', 'd').get_deck_position(), 5)
        self.assertEqual(pk.Card('3', 'c').get_deck_position(), 4)
        self.assertEqual(pk.Card('2', 's').get_deck_position(), 3)
        self.assertEqual(pk.Card('2', 'h').get_deck_position(), 2)
        self.assertEqual(pk.Card('2', 'd').get_deck_position(), 1)
        self.assertEqual(pk.Card('2', 'c').get_deck_position(), 0)


if __name__ == '__main__':
    main()