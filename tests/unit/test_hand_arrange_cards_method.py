"""
Defines unit tests on Hand class arrange_cards method.
"""


import sys
sys.path.insert(0, '.')


from unittest import main, TestCase


import pokerpy as pk


class TestHandArrangeCardsMethod(TestCase):


    """
    Runs unit tests on Hand class arrange_cards method.
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
            pk.Hand.arrange_cards(cards)
        
        self.assertEqual(cm.exception.args[0], pk.messages.not_five_cards_hand_message)

        
        # Less cards than expected

        cards = (
            pk.Card('J', 'h'),
            pk.Card('2', 'c'),
            pk.Card('6', 's'),
        )

        with self.assertRaises(ValueError) as cm:
            pk.Hand.arrange_cards(cards)
        
        self.assertEqual(cm.exception.args[0], pk.messages.not_five_cards_hand_message)


        # No cards

        cards = tuple()

        with self.assertRaises(ValueError) as cm:
            pk.Hand.arrange_cards(cards)
        
        self.assertEqual(cm.exception.args[0], pk.messages.not_five_cards_hand_message)


        # Exactly five cards but some repeated

        cards = (
            pk.Card('2', 'd'),
            pk.Card('5', 's'),
            pk.Card('2', 'd'),
            pk.Card('5', 's'),
            pk.Card('T', 'c'),
        )

        with self.assertRaises(ValueError) as cm:
            pk.Hand.arrange_cards(cards)
        
        self.assertEqual(cm.exception.args[0], pk.messages.repeated_cards_hand_message)


    def test_four_of_a_kind_arrangements(self):


        """
        Runs test cases to check sets with four of a kind are arranged as expected.
        """


        # Four of a kind with higher value than unpaired card

        cards = (
            pk.Card('K', 'h'),
            pk.Card('7', 'h'),
            pk.Card('K', 'd'),
            pk.Card('K', 's'),
            pk.Card('K', 'c'),
        )

        expected_arrangement = (
            pk.Card('K', 's'),
            pk.Card('K', 'h'),
            pk.Card('K', 'd'),
            pk.Card('K', 'c'),
            pk.Card('7', 'h'),
        )
        
        self.assertEqual(pk.Hand.arrange_cards(cards), expected_arrangement)


        # Four of a kind with lower value than unpaired card

        cards = (
            pk.Card('3', 's'),
            pk.Card('T', 'h'),
            pk.Card('3', 'h'),
            pk.Card('3', 'c'),
            pk.Card('3', 'd'),
        )
        expected_arrangement = (
            pk.Card('3', 's'),
            pk.Card('3', 'h'),
            pk.Card('3', 'd'),
            pk.Card('3', 'c'),
            pk.Card('T', 'h'),
        )
        self.assertEqual(pk.Hand.arrange_cards(cards), expected_arrangement)


    def test_three_of_a_kind_arrangements(self):


        """
        Runs test cases to check sets with three of a kind are arranged as expected.
        """


        # Three of a kind with higher value than pair

        cards = (
            pk.Card('4', 's'),
            pk.Card('T', 'c'),
            pk.Card('T', 'd'),
            pk.Card('4', 'd'),
            pk.Card('T', 's'),
        )

        expected_arrangement = (
            pk.Card('T', 's'),
            pk.Card('T', 'd'),
            pk.Card('T', 'c'),
            pk.Card('4', 's'),
            pk.Card('4', 'd'),
        )

        self.assertEqual(pk.Hand.arrange_cards(cards), expected_arrangement)


        # Three kind with lower value than pair

        cards = (
            pk.Card('5', 'h'),
            pk.Card('A', 'c'),
            pk.Card('5', 's'),
            pk.Card('A', 'd'),
            pk.Card('5', 'c'),
        )

        expected_arrangement = (
            pk.Card('5', 's'),
            pk.Card('5', 'h'),
            pk.Card('5', 'c'),
            pk.Card('A', 'd'),
            pk.Card('A', 'c'),
        )

        self.assertEqual(pk.Hand.arrange_cards(cards), expected_arrangement)


        # Three of a kind with higher value than unpaired cards

        cards = (
            pk.Card('5', 'c'),
            pk.Card('2', 'h'),
            pk.Card('5', 's'),
            pk.Card('3', 'd'),
            pk.Card('5', 'd'),
        )

        expected_arrangement = (
            pk.Card('5', 's'),
            pk.Card('5', 'd'),
            pk.Card('5', 'c'),
            pk.Card('3', 'd'),
            pk.Card('2', 'h'),
        )
        
        self.assertEqual(pk.Hand.arrange_cards(cards), expected_arrangement)


        # Three of a kind with value between single unpaired card values

        cards = (
            pk.Card('6', 'h'),
            pk.Card('J', 'c'),
            pk.Card('J', 's'),
            pk.Card('K', 'h'),
            pk.Card('J', 'h'),
        )

        expected_arrangement = (
            pk.Card('J', 's'),
            pk.Card('J', 'h'),
            pk.Card('J', 'c'),
            pk.Card('K', 'h'),
            pk.Card('6', 'h'),
        )
        
        self.assertEqual(pk.Hand.arrange_cards(cards), expected_arrangement)


        # Three of a kind with lower value than unpaired cards

        cards = (
            pk.Card('6', 'h'),
            pk.Card('2', 'c'),
            pk.Card('2', 's'),
            pk.Card('2', 'h'),
            pk.Card('7', 's'),
        )

        expected_arrangement = (
            pk.Card('2', 's'),
            pk.Card('2', 'h'),
            pk.Card('2', 'c'),
            pk.Card('7', 's'),
            pk.Card('6', 'h'),
        )
        
        self.assertEqual(pk.Hand.arrange_cards(cards), expected_arrangement)


    def test_pair_arrangements(self):


        """
        Runs test cases to check sets with pairs are arranged as expected.
        """


        # Two pairs with higher values than unpaired card

        cards = (
            pk.Card('7', 'c'),
            pk.Card('A', 'h'),
            pk.Card('8', 'c'),
            pk.Card('8', 's'),
            pk.Card('A', 'd'),
        )

        expected_arrangement = (
            pk.Card('A', 'h'),
            pk.Card('A', 'd'),
            pk.Card('8', 's'),
            pk.Card('8', 'c'),
            pk.Card('7', 'c'),
        )
        
        self.assertEqual(pk.Hand.arrange_cards(cards), expected_arrangement)


        # Single card with value between two pairs values

        cards = (
            pk.Card('J', 's'),
            pk.Card('Q', 's'),
            pk.Card('T', 's'),
            pk.Card('Q', 'c'),
            pk.Card('T', 'c'),
        )

        expected_arrangement = (
            pk.Card('Q', 's'),
            pk.Card('Q', 'c'),
            pk.Card('T', 's'),
            pk.Card('T', 'c'),
            pk.Card('J', 's'),
        )
        
        self.assertEqual(pk.Hand.arrange_cards(cards), expected_arrangement)


        # Two pairs with lower values than single card

        cards = (
            pk.Card('K', 'd'),
            pk.Card('5', 'h'),
            pk.Card('5', 's'),
            pk.Card('3', 'h'),
            pk.Card('3', 's'),
        )

        expected_arrangement = (
            pk.Card('5', 's'),
            pk.Card('5', 'h'),
            pk.Card('3', 's'),
            pk.Card('3', 'h'),
            pk.Card('K', 'd'),
        )
        
        self.assertEqual(pk.Hand.arrange_cards(cards), expected_arrangement)


        # Pair with higher values than unpaired cards

        cards = (
            pk.Card('7', 'd'),
            pk.Card('2', 'd'),
            pk.Card('T', 'h'),
            pk.Card('T', 'd'),
            pk.Card('3', 'd'),
        )

        expected_arrangement = (
            pk.Card('T', 'h'),
            pk.Card('T', 'd'),
            pk.Card('7', 'd'),
            pk.Card('3', 'd'),
            pk.Card('2', 'd'),
        )
        
        self.assertEqual(pk.Hand.arrange_cards(cards), expected_arrangement)


        # Pair with higher value than two unpaired cards and lower than a single unpaired card

        cards = (
            pk.Card('J', 'h'),
            pk.Card('J', 'c'),
            pk.Card('9', 's'),
            pk.Card('8', 'd'),
            pk.Card('A', 's'),
        )

        expected_arrangement = (
            pk.Card('J', 'h'),
            pk.Card('J', 'c'),
            pk.Card('A', 's'),
            pk.Card('9', 's'),
            pk.Card('8', 'd'),
        )
        
        self.assertEqual(pk.Hand.arrange_cards(cards), expected_arrangement)


        # Pair with higher value than a single unpaired card and lower than two unpaired cards

        cards = (
            pk.Card('Q', 'd'),
            pk.Card('J', 'c'),
            pk.Card('6', 'c'),
            pk.Card('3', 'd'),
            pk.Card('6', 's'),
        )

        expected_arrangement = (
            pk.Card('6', 's'),
            pk.Card('6', 'c'),
            pk.Card('Q', 'd'),
            pk.Card('J', 'c'),
            pk.Card('3', 'd'),
        )
        
        self.assertEqual(pk.Hand.arrange_cards(cards), expected_arrangement)


        # Pair with lower values than unpaired cards

        cards = (
            pk.Card('J', 's'),
            pk.Card('A', 'd'),
            pk.Card('T', 's'),
            pk.Card('T', 'h'),
            pk.Card('Q', 'h'),
        )

        expected_arrangement = (
            pk.Card('T', 's'),
            pk.Card('T', 'h'),
            pk.Card('A', 'd'),
            pk.Card('Q', 'h'),
            pk.Card('J', 's'),
        )
        
        self.assertEqual(pk.Hand.arrange_cards(cards), expected_arrangement)


    def test_unpaired_arrangements(self):


        """
        Runs test cases to check sets with unpaired cards are arranged as expected.
        """


        # Straight flush

        cards = (
            pk.Card('6', 'h'),
            pk.Card('T', 'h'),
            pk.Card('7', 'h'),
            pk.Card('8', 'h'),
            pk.Card('9', 'h'),
        )

        expected_arrangement = (
            pk.Card('T', 'h'),
            pk.Card('9', 'h'),
            pk.Card('8', 'h'),
            pk.Card('7', 'h'),
            pk.Card('6', 'h'),
        )

        self.assertEqual(pk.Hand.arrange_cards(cards), expected_arrangement)


        # Special case: five to ace straight flush

        cards = (
            pk.Card('3', 'd'),
            pk.Card('4', 'd'),
            pk.Card('A', 'd'),
            pk.Card('5', 'd'),
            pk.Card('2', 'c'),
        )

        expected_arrangement = (
            pk.Card('5', 'd'),
            pk.Card('4', 'd'),
            pk.Card('3', 'd'),
            pk.Card('2', 'd'),
            pk.Card('A', 'd'),
        )


        # Straight without flush

        cards = (
            pk.Card('K', 's'),
            pk.Card('A', 's'),
            pk.Card('J', 'h'),
            pk.Card('Q', 'd'),
            pk.Card('T', 's'),
        )

        expected_arrangement = (
            pk.Card('A', 's'),
            pk.Card('K', 's'),
            pk.Card('Q', 'd'),
            pk.Card('J', 'h'),
            pk.Card('T', 's'),
        )

        self.assertEqual(pk.Hand.arrange_cards(cards), expected_arrangement)


        # Special case: five to ace straight without flush

        cards = (
            pk.Card('3', 'd'),
            pk.Card('5', 'd'),
            pk.Card('A', 'c'),
            pk.Card('4', 's'),
            pk.Card('2', 'c'),
        )

        expected_arrangement = (
            pk.Card('5', 'd'),
            pk.Card('4', 's'),
            pk.Card('3', 'd'),
            pk.Card('2', 'c'),
            pk.Card('A', 'c'),
        )

        self.assertEqual(pk.Hand.arrange_cards(cards), expected_arrangement)


        # Flush without straight

        cards = (
            pk.Card('K', 's'),
            pk.Card('9', 's'),
            pk.Card('2', 's'),
            pk.Card('7', 's'),
            pk.Card('6', 's'),
        )

        expected_arrangement = (
            pk.Card('K', 's'),
            pk.Card('9', 's'),
            pk.Card('7', 's'),
            pk.Card('6', 's'),
            pk.Card('2', 's'),
        )

        self.assertEqual(pk.Hand.arrange_cards(cards), expected_arrangement)


        # No straight and no flush

        cards = (
            pk.Card('8', 'd'),
            pk.Card('3', 's'),
            pk.Card('J', 'c'),
            pk.Card('7', 'c'),
            pk.Card('4', 's'),
        )

        expected_arrangement = (
            pk.Card('J', 'c'),
            pk.Card('8', 'd'),
            pk.Card('7', 'c'),
            pk.Card('4', 's'),
            pk.Card('3', 's'),
        )

        self.assertEqual(pk.Hand.arrange_cards(cards), expected_arrangement)


if __name__ == '__main__':
    main()