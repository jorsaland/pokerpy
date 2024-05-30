"""
Defines unit tests on get_category function.
"""


import sys
sys.path.insert(0, '.')


from unittest import main, TestCase


from pokerpy import constants, messages, structures


class TestHandGetCategory(TestCase):


    """
    Runs unit tests on get_category function.
    """


    def test_input(self):


        """
        Runs test cases to check input is valid.
        """


        # More cards than expected

        cards = [
            structures.Card('K', 'h'),
            structures.Card('7', 'h'),
            structures.Card('2', 'd'),
            structures.Card('5', 's'),
            structures.Card('K', 'c'),
            structures.Card('A', 'c'),
            structures.Card('T', 'c'),
        ]

        with self.assertRaises(ValueError) as cm:
            structures.get_category(cards)
        
        self.assertEqual(cm.exception.args[0], messages.hand_not_five_cards_message)

        
        # Less cards than expected

        cards = [
            structures.Card('J', 'h'),
            structures.Card('2', 'c'),
            structures.Card('6', 's'),
        ]

        with self.assertRaises(ValueError) as cm:
            structures.get_category(cards)
        
        self.assertEqual(cm.exception.args[0], messages.hand_not_five_cards_message)


        # No cards

        cards = []

        with self.assertRaises(ValueError) as cm:
            structures.get_category(cards)
        
        self.assertEqual(cm.exception.args[0], messages.hand_not_five_cards_message)


        # Exactly five cards but some repeated

        cards = [
            structures.Card('2', 'd'),
            structures.Card('5', 's'),
            structures.Card('2', 'd'),
            structures.Card('5', 's'),
            structures.Card('T', 'c'),
        ]

        with self.assertRaises(ValueError) as cm:
            structures.get_category(cards)
        
        self.assertEqual(cm.exception.args[0], messages.hand_repeated_cards_message)


    def test_royal_flush(self):


        """
        Runs test cases to check all possible royal flushes are detected.
        """


        # Spades royal flush

        cards = [
            structures.Card('A', 's'),
            structures.Card('J', 's'),
            structures.Card('K', 's'),
            structures.Card('Q', 's'),
            structures.Card('T', 's'),
        ]
        
        self.assertEqual(structures.get_category(cards), constants.ROYAL_FLUSH)


        # Hearts royal flush

        cards = [
            structures.Card('A', 'h'),
            structures.Card('K', 'h'),
            structures.Card('Q', 'h'),
            structures.Card('J', 'h'),
            structures.Card('T', 'h'),
        ]
        
        self.assertEqual(structures.get_category(cards), constants.ROYAL_FLUSH)


        # Diamonds royal flush

        cards = [
            structures.Card('A', 'd'),
            structures.Card('K', 'd'),
            structures.Card('J', 'd'),
            structures.Card('T', 'd'),
            structures.Card('Q', 'd'),
        ]
        
        self.assertEqual(structures.get_category(cards), constants.ROYAL_FLUSH)


        # Clubs royal flush

        cards = [
            structures.Card('T', 'c'),
            structures.Card('J', 'c'),
            structures.Card('Q', 'c'),
            structures.Card('K', 'c'),
            structures.Card('A', 'c'),
        ]
        
        self.assertEqual(structures.get_category(cards), constants.ROYAL_FLUSH)


    def test_straight_flush(self):


        """
        Runs test cases to check straight flushes are detected as expected.
        """


        # King high straight flush

        cards = [
            structures.Card('T', 'c'),
            structures.Card('J', 'c'),
            structures.Card('K', 'c'),
            structures.Card('Q', 'c'),
            structures.Card('9', 'c'),
        ]
        
        self.assertEqual(structures.get_category(cards), constants.STRAIGHT_FLUSH)


        # Intermediate high value straight flush

        cards = [
            structures.Card('T', 's'),
            structures.Card('7', 's'),
            structures.Card('9', 's'),
            structures.Card('8', 's'),
            structures.Card('6', 's'),
        ]
        
        self.assertEqual(structures.get_category(cards), constants.STRAIGHT_FLUSH)


        # Five high straight flush

        cards = [
            structures.Card('A', 'd'),
            structures.Card('5', 'd'),
            structures.Card('4', 'd'),
            structures.Card('3', 'd'),
            structures.Card('2', 'd'),
        ]
        
        self.assertEqual(structures.get_category(cards), constants.STRAIGHT_FLUSH)


    def test_four_of_a_kind(self):


        """
        Runs test cases to check four of a kind is detected as expected.
        """


        # Four of a kind with higher value than unpaired card

        cards = [
            structures.Card('K', 'h'),
            structures.Card('7', 'h'),
            structures.Card('K', 'd'),
            structures.Card('K', 's'),
            structures.Card('K', 'c'),
        ]
        
        self.assertEqual(structures.get_category(cards), constants.FOUR_OF_A_KIND)


        # Four of a kind with lower value than unpaired card

        cards = [
            structures.Card('3', 's'),
            structures.Card('T', 'h'),
            structures.Card('3', 'h'),
            structures.Card('3', 'c'),
            structures.Card('3', 'd'),
        ]
        self.assertEqual(structures.get_category(cards), constants.FOUR_OF_A_KIND)


    def test_full_house(self):


        """
        Runs test cases to check full house is detected as expected.
        """


        # Three of a kind with higher value than pair

        cards = [
            structures.Card('4', 's'),
            structures.Card('T', 'c'),
            structures.Card('T', 'd'),
            structures.Card('4', 'd'),
            structures.Card('T', 's'),
        ]

        self.assertEqual(structures.get_category(cards), constants.FULL_HOUSE)


        # Three kind with lower value than pair

        cards = [
            structures.Card('5', 'h'),
            structures.Card('A', 'c'),
            structures.Card('5', 's'),
            structures.Card('A', 'd'),
            structures.Card('5', 'c'),
        ]

        self.assertEqual(structures.get_category(cards), constants.FULL_HOUSE)


        # Four of a kind with higher value than unpaired card


    def test_flush(self):


        """
        Runs test cases to check flush is detected as expected.
        """


        # Random flush

        cards = [
            structures.Card('K', 's'),
            structures.Card('9', 's'),
            structures.Card('2', 's'),
            structures.Card('7', 's'),
            structures.Card('6', 's'),
        ]

        self.assertEqual(structures.get_category(cards), constants.FLUSH)


        # Almost straight flush

        cards = [
            structures.Card('K', 'd'),
            structures.Card('Q', 'd'),
            structures.Card('J', 'd'),
            structures.Card('T', 'd'),
            structures.Card('8', 'd'),
        ]

        self.assertEqual(structures.get_category(cards), constants.FLUSH)


    def test_straight(self):


        """
        Runs test cases to check straight is detected as expected.
        """


        # Random straight

        cards = [
            structures.Card('K', 's'),
            structures.Card('A', 's'),
            structures.Card('J', 'h'),
            structures.Card('Q', 'd'),
            structures.Card('T', 's'),
        ]

        self.assertEqual(structures.get_category(cards), constants.STRAIGHT)


        # Almost straight flush

        cards = [
            structures.Card('5', 'd'),
            structures.Card('4', 'd'),
            structures.Card('3', 's'),
            structures.Card('2', 'd'),
            structures.Card('A', 'd'),
        ]

        self.assertEqual(structures.get_category(cards), constants.STRAIGHT)


    def test_three_of_a_kind(self):


        """
        Runs test cases to check three of a kind is detected as expected.
        """


        # Three of a kind with higher value than unpaired cards

        cards = [
            structures.Card('5', 'c'),
            structures.Card('2', 'h'),
            structures.Card('5', 's'),
            structures.Card('3', 'd'),
            structures.Card('5', 'd'),
        ]

        self.assertEqual(structures.get_category(cards), constants.THREE_OF_A_KIND)


        # Three of a kind with value between single unpaired card values

        cards = [
            structures.Card('6', 'h'),
            structures.Card('J', 'c'),
            structures.Card('J', 's'),
            structures.Card('K', 'h'),
            structures.Card('J', 'h'),
        ]
        
        self.assertEqual(structures.get_category(cards), constants.THREE_OF_A_KIND)


        # Three of a kind with lower value than unpaired cards

        cards = [
            structures.Card('6', 'h'),
            structures.Card('2', 'c'),
            structures.Card('2', 's'),
            structures.Card('2', 'h'),
            structures.Card('7', 's'),
        ]
        
        self.assertEqual(structures.get_category(cards), constants.THREE_OF_A_KIND)


    def test_two_pair(self):


        """
        Runs test cases to check two pair is detected as expected.
        """


        # Two pairs with higher values than unpaired card

        cards = [
            structures.Card('7', 'c'),
            structures.Card('A', 'h'),
            structures.Card('8', 'c'),
            structures.Card('8', 's'),
            structures.Card('A', 'd'),
        ]
        
        self.assertEqual(structures.get_category(cards), constants.TWO_PAIR)


        # Single card with value between two pairs values

        cards = [
            structures.Card('J', 's'),
            structures.Card('Q', 's'),
            structures.Card('T', 's'),
            structures.Card('Q', 'c'),
            structures.Card('T', 'c'),
        ]
        
        self.assertEqual(structures.get_category(cards), constants.TWO_PAIR)


        # Two pairs with lower values than single card

        cards = [
            structures.Card('K', 'd'),
            structures.Card('5', 'h'),
            structures.Card('5', 's'),
            structures.Card('3', 'h'),
            structures.Card('3', 's'),
        ]
        
        self.assertEqual(structures.get_category(cards), constants.TWO_PAIR)


    def test_pair(self):


        """
        Runs test cases to check pair is detected as expected.
        """


        # Pair with higher values than unpaired cards

        cards = [
            structures.Card('7', 'd'),
            structures.Card('2', 'd'),
            structures.Card('T', 'h'),
            structures.Card('T', 'd'),
            structures.Card('3', 'd'),
        ]
        
        self.assertEqual(structures.get_category(cards), constants.ONE_PAIR)


        # Pair with higher value than two unpaired cards and lower than a single unpaired card

        cards = [
            structures.Card('J', 'h'),
            structures.Card('J', 'c'),
            structures.Card('9', 's'),
            structures.Card('8', 'd'),
            structures.Card('A', 's'),
        ]
        
        self.assertEqual(structures.get_category(cards), constants.ONE_PAIR)


        # Pair with higher value than a single unpaired card and lower than two unpaired cards

        cards = [
            structures.Card('Q', 'd'),
            structures.Card('J', 'c'),
            structures.Card('6', 'c'),
            structures.Card('3', 'd'),
            structures.Card('6', 's'),
        ]
        
        self.assertEqual(structures.get_category(cards), constants.ONE_PAIR)


        # Pair with lower values than unpaired cards

        cards = [
            structures.Card('J', 's'),
            structures.Card('A', 'd'),
            structures.Card('T', 's'),
            structures.Card('T', 'h'),
            structures.Card('Q', 'h'),
        ]

        self.assertEqual(structures.get_category(cards), constants.ONE_PAIR)


    def test_high_card(self):


        """
        Runs test cases to check high card is detected as expected.
        """


        # Random high card

        cards = [
            structures.Card('8', 'd'),
            structures.Card('3', 's'),
            structures.Card('J', 'c'),
            structures.Card('7', 'c'),
            structures.Card('4', 's'),
        ]

        self.assertEqual(structures.get_category(cards), constants.HIGH_CARD)


        # Almost flush

        cards = [
            structures.Card('8', 'd'),
            structures.Card('3', 'd'),
            structures.Card('J', 'd'),
            structures.Card('7', 'h'),
            structures.Card('4', 'd'),
        ]

        self.assertEqual(structures.get_category(cards), constants.HIGH_CARD)


        # Almost straight

        cards = [
            structures.Card('8', 'd'),
            structures.Card('7', 's'),
            structures.Card('6', 'c'),
            structures.Card('5', 'c'),
            structures.Card('3', 's'),
        ]

        self.assertEqual(structures.get_category(cards), constants.HIGH_CARD)


if __name__ == '__main__':
    main()