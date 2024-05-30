"""
Defines unit tests on Hand class get_category method.
"""


import sys
sys.path.insert(0, '.')


from unittest import main, TestCase


import pokerpy as pk


class TestHandGetCategory(TestCase):


    """
    Runs unit tests on Hand class get_category method.
    """


    def test_input(self):


        """
        Runs test cases to check input is valid.
        """


        # More cards than expected

        cards = (
            pk.Card('K', 'h'),
            pk.Card('7', 'h'),
            pk.Card('2', 'd'),
            pk.Card('5', 's'),
            pk.Card('K', 'c'),
            pk.Card('A', 'c'),
            pk.Card('T', 'c'),
        )

        with self.assertRaises(ValueError) as cm:
            pk.Hand.get_category(cards)
        
        self.assertEqual(cm.exception.args[0], pk.messages.hand_not_five_cards_message)

        
        # Less cards than expected

        cards = (
            pk.Card('J', 'h'),
            pk.Card('2', 'c'),
            pk.Card('6', 's'),
        )

        with self.assertRaises(ValueError) as cm:
            pk.Hand.get_category(cards)
        
        self.assertEqual(cm.exception.args[0], pk.messages.hand_not_five_cards_message)


        # No cards

        cards = tuple()

        with self.assertRaises(ValueError) as cm:
            pk.Hand.get_category(cards)
        
        self.assertEqual(cm.exception.args[0], pk.messages.hand_not_five_cards_message)


        # Exactly five cards but some repeated

        cards = (
            pk.Card('2', 'd'),
            pk.Card('5', 's'),
            pk.Card('2', 'd'),
            pk.Card('5', 's'),
            pk.Card('T', 'c'),
        )

        with self.assertRaises(ValueError) as cm:
            pk.Hand.get_category(cards)
        
        self.assertEqual(cm.exception.args[0], pk.messages.hand_repeated_cards_message)


    def test_royal_flush(self):


        """
        Runs test cases to check all possible royal flushes are detected.
        """


        # Spades royal flush

        cards = (
            pk.Card('A', 's'),
            pk.Card('J', 's'),
            pk.Card('K', 's'),
            pk.Card('Q', 's'),
            pk.Card('T', 's'),
        )
        
        self.assertEqual(pk.Hand.get_category(cards), pk.ROYAL_FLUSH)


        # Hearts royal flush

        cards = (
            pk.Card('A', 'h'),
            pk.Card('K', 'h'),
            pk.Card('Q', 'h'),
            pk.Card('J', 'h'),
            pk.Card('T', 'h'),
        )
        
        self.assertEqual(pk.Hand.get_category(cards), pk.ROYAL_FLUSH)


        # Diamonds royal flush

        cards = (
            pk.Card('A', 'd'),
            pk.Card('K', 'd'),
            pk.Card('J', 'd'),
            pk.Card('T', 'd'),
            pk.Card('Q', 'd'),
        )
        
        self.assertEqual(pk.Hand.get_category(cards), pk.ROYAL_FLUSH)


        # Clubs royal flush

        cards = (
            pk.Card('T', 'c'),
            pk.Card('J', 'c'),
            pk.Card('Q', 'c'),
            pk.Card('K', 'c'),
            pk.Card('A', 'c'),
        )
        
        self.assertEqual(pk.Hand.get_category(cards), pk.ROYAL_FLUSH)


    def test_straight_flush(self):


        """
        Runs test cases to check straight flushes are detected as expected.
        """


        # King high straight flush

        cards = (
            pk.Card('T', 'c'),
            pk.Card('J', 'c'),
            pk.Card('K', 'c'),
            pk.Card('Q', 'c'),
            pk.Card('9', 'c'),
        )
        
        self.assertEqual(pk.Hand.get_category(cards), pk.STRAIGHT_FLUSH)


        # Intermediate high value straight flush

        cards = (
            pk.Card('T', 's'),
            pk.Card('7', 's'),
            pk.Card('9', 's'),
            pk.Card('8', 's'),
            pk.Card('6', 's'),
        )
        
        self.assertEqual(pk.Hand.get_category(cards), pk.STRAIGHT_FLUSH)


        # Five high straight flush

        cards = (
            pk.Card('A', 'd'),
            pk.Card('5', 'd'),
            pk.Card('4', 'd'),
            pk.Card('3', 'd'),
            pk.Card('2', 'd'),
        )
        
        self.assertEqual(pk.Hand.get_category(cards), pk.STRAIGHT_FLUSH)


    def test_four_of_a_kind(self):


        """
        Runs test cases to check four of a kind is detected as expected.
        """


        # Four of a kind with higher value than unpaired card

        cards = (
            pk.Card('K', 'h'),
            pk.Card('7', 'h'),
            pk.Card('K', 'd'),
            pk.Card('K', 's'),
            pk.Card('K', 'c'),
        )
        
        self.assertEqual(pk.Hand.get_category(cards), pk.FOUR_OF_A_KIND)


        # Four of a kind with lower value than unpaired card

        cards = (
            pk.Card('3', 's'),
            pk.Card('T', 'h'),
            pk.Card('3', 'h'),
            pk.Card('3', 'c'),
            pk.Card('3', 'd'),
        )
        self.assertEqual(pk.Hand.get_category(cards), pk.FOUR_OF_A_KIND)


    def test_full_house(self):


        """
        Runs test cases to check full house is detected as expected.
        """


        # Three of a kind with higher value than pair

        cards = (
            pk.Card('4', 's'),
            pk.Card('T', 'c'),
            pk.Card('T', 'd'),
            pk.Card('4', 'd'),
            pk.Card('T', 's'),
        )

        self.assertEqual(pk.Hand.get_category(cards), pk.FULL_HOUSE)


        # Three kind with lower value than pair

        cards = (
            pk.Card('5', 'h'),
            pk.Card('A', 'c'),
            pk.Card('5', 's'),
            pk.Card('A', 'd'),
            pk.Card('5', 'c'),
        )

        self.assertEqual(pk.Hand.get_category(cards), pk.FULL_HOUSE)


        # Four of a kind with higher value than unpaired card


    def test_flush(self):


        """
        Runs test cases to check flush is detected as expected.
        """


        # Random flush

        cards = (
            pk.Card('K', 's'),
            pk.Card('9', 's'),
            pk.Card('2', 's'),
            pk.Card('7', 's'),
            pk.Card('6', 's'),
        )

        self.assertEqual(pk.Hand.get_category(cards), pk.FLUSH)


        # Almost straight flush

        cards = (
            pk.Card('K', 'd'),
            pk.Card('Q', 'd'),
            pk.Card('J', 'd'),
            pk.Card('T', 'd'),
            pk.Card('8', 'd'),
        )

        self.assertEqual(pk.Hand.get_category(cards), pk.FLUSH)


    def test_straight(self):


        """
        Runs test cases to check straight is detected as expected.
        """


        # Random straight

        cards = (
            pk.Card('K', 's'),
            pk.Card('A', 's'),
            pk.Card('J', 'h'),
            pk.Card('Q', 'd'),
            pk.Card('T', 's'),
        )

        self.assertEqual(pk.Hand.get_category(cards), pk.STRAIGHT)


        # Almost straight flush

        cards = (
            pk.Card('5', 'd'),
            pk.Card('4', 'd'),
            pk.Card('3', 's'),
            pk.Card('2', 'd'),
            pk.Card('A', 'd'),
        )

        self.assertEqual(pk.Hand.get_category(cards), pk.STRAIGHT)


    def test_three_of_a_kind(self):


        """
        Runs test cases to check three of a kind is detected as expected.
        """


        # Three of a kind with higher value than unpaired cards

        cards = (
            pk.Card('5', 'c'),
            pk.Card('2', 'h'),
            pk.Card('5', 's'),
            pk.Card('3', 'd'),
            pk.Card('5', 'd'),
        )

        self.assertEqual(pk.Hand.get_category(cards), pk.THREE_OF_A_KIND)


        # Three of a kind with value between single unpaired card values

        cards = (
            pk.Card('6', 'h'),
            pk.Card('J', 'c'),
            pk.Card('J', 's'),
            pk.Card('K', 'h'),
            pk.Card('J', 'h'),
        )
        
        self.assertEqual(pk.Hand.get_category(cards), pk.THREE_OF_A_KIND)


        # Three of a kind with lower value than unpaired cards

        cards = (
            pk.Card('6', 'h'),
            pk.Card('2', 'c'),
            pk.Card('2', 's'),
            pk.Card('2', 'h'),
            pk.Card('7', 's'),
        )
        
        self.assertEqual(pk.Hand.get_category(cards), pk.THREE_OF_A_KIND)


    def test_two_pair(self):


        """
        Runs test cases to check two pair is detected as expected.
        """


        # Two pairs with higher values than unpaired card

        cards = (
            pk.Card('7', 'c'),
            pk.Card('A', 'h'),
            pk.Card('8', 'c'),
            pk.Card('8', 's'),
            pk.Card('A', 'd'),
        )
        
        self.assertEqual(pk.Hand.get_category(cards), pk.TWO_PAIR)


        # Single card with value between two pairs values

        cards = (
            pk.Card('J', 's'),
            pk.Card('Q', 's'),
            pk.Card('T', 's'),
            pk.Card('Q', 'c'),
            pk.Card('T', 'c'),
        )
        
        self.assertEqual(pk.Hand.get_category(cards), pk.TWO_PAIR)


        # Two pairs with lower values than single card

        cards = (
            pk.Card('K', 'd'),
            pk.Card('5', 'h'),
            pk.Card('5', 's'),
            pk.Card('3', 'h'),
            pk.Card('3', 's'),
        )
        
        self.assertEqual(pk.Hand.get_category(cards), pk.TWO_PAIR)


    def test_pair(self):


        """
        Runs test cases to check pair is detected as expected.
        """


        # Pair with higher values than unpaired cards

        cards = (
            pk.Card('7', 'd'),
            pk.Card('2', 'd'),
            pk.Card('T', 'h'),
            pk.Card('T', 'd'),
            pk.Card('3', 'd'),
        )
        
        self.assertEqual(pk.Hand.get_category(cards), pk.ONE_PAIR)


        # Pair with higher value than two unpaired cards and lower than a single unpaired card

        cards = (
            pk.Card('J', 'h'),
            pk.Card('J', 'c'),
            pk.Card('9', 's'),
            pk.Card('8', 'd'),
            pk.Card('A', 's'),
        )
        
        self.assertEqual(pk.Hand.get_category(cards), pk.ONE_PAIR)


        # Pair with higher value than a single unpaired card and lower than two unpaired cards

        cards = (
            pk.Card('Q', 'd'),
            pk.Card('J', 'c'),
            pk.Card('6', 'c'),
            pk.Card('3', 'd'),
            pk.Card('6', 's'),
        )
        
        self.assertEqual(pk.Hand.get_category(cards), pk.ONE_PAIR)


        # Pair with lower values than unpaired cards

        cards = (
            pk.Card('J', 's'),
            pk.Card('A', 'd'),
            pk.Card('T', 's'),
            pk.Card('T', 'h'),
            pk.Card('Q', 'h'),
        )

        self.assertEqual(pk.Hand.get_category(cards), pk.ONE_PAIR)


    def test_high_card(self):


        """
        Runs test cases to check high card is detected as expected.
        """


        # Random high card

        cards = (
            pk.Card('8', 'd'),
            pk.Card('3', 's'),
            pk.Card('J', 'c'),
            pk.Card('7', 'c'),
            pk.Card('4', 's'),
        )

        self.assertEqual(pk.Hand.get_category(cards), pk.HIGH_CARD)


        # Almost flush

        cards = (
            pk.Card('8', 'd'),
            pk.Card('3', 'd'),
            pk.Card('J', 'd'),
            pk.Card('7', 'h'),
            pk.Card('4', 'd'),
        )

        self.assertEqual(pk.Hand.get_category(cards), pk.HIGH_CARD)


        # Almost straight

        cards = (
            pk.Card('8', 'd'),
            pk.Card('7', 's'),
            pk.Card('6', 'c'),
            pk.Card('5', 'c'),
            pk.Card('3', 's'),
        )

        self.assertEqual(pk.Hand.get_category(cards), pk.HIGH_CARD)


if __name__ == '__main__':
    main()