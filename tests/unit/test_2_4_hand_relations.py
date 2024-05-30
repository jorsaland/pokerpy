"""
Defines unit tests on Hand relations.
"""


import sys
sys.path.insert(0, '.')


from unittest import main, TestCase


from pokerpy import structures


class TestHandRelations(TestCase):


    """
    Runs unit tests on Hand class relations.
    """


    def test_royal_flush_relations(self):


        """
        Runs test cases to check relations between royal flush hands work as expected.
        """


        # Exactly same hand

        hand_1 = structures.Hand([
            structures.Card('A', 's'),
            structures.Card('K', 's'),
            structures.Card('Q', 's'),
            structures.Card('J', 's'),
            structures.Card('T', 's'),
        ])

        hand_2 = structures.Hand([
            structures.Card('A', 's'),
            structures.Card('K', 's'),
            structures.Card('Q', 's'),
            structures.Card('J', 's'),
            structures.Card('T', 's'),
        ])
        
        self.assertEqual(hand_1, hand_2)
        self.assertGreaterEqual(hand_1, hand_2)


        # Same hand, different suits

        hand_1 = structures.Hand([
            structures.Card('A', 'c'),
            structures.Card('K', 'c'),
            structures.Card('Q', 'c'),
            structures.Card('J', 'c'),
            structures.Card('T', 'c'),
        ])

        hand_2 = structures.Hand([
            structures.Card('A', 's'),
            structures.Card('K', 's'),
            structures.Card('Q', 's'),
            structures.Card('J', 's'),
            structures.Card('T', 's'),
        ])
        
        self.assertEqual(hand_1, hand_2)
        self.assertGreaterEqual(hand_1, hand_2)


    def test_straight_flush_relations(self):


        """
        Runs test cases to check relations between royal flush hands work as expected.
        """


        # Exactly same hand

        hand_1 = structures.Hand([
            structures.Card('T', 's'),
            structures.Card('9', 's'),
            structures.Card('8', 's'),
            structures.Card('7', 's'),
            structures.Card('6', 's'),
        ])

        hand_2 = structures.Hand([
            structures.Card('T', 's'),
            structures.Card('9', 's'),
            structures.Card('8', 's'),
            structures.Card('7', 's'),
            structures.Card('6', 's'),
        ])
        
        self.assertEqual(hand_1, hand_2)
        self.assertGreaterEqual(hand_1, hand_2)


        # Same hand, different suits

        hand_1 = structures.Hand([
            structures.Card('T', 'h'),
            structures.Card('9', 'h'),
            structures.Card('8', 'h'),
            structures.Card('7', 'h'),
            structures.Card('6', 'h'),
        ])

        hand_2 = structures.Hand([
            structures.Card('T', 'c'),
            structures.Card('9', 'c'),
            structures.Card('8', 'c'),
            structures.Card('7', 'c'),
            structures.Card('6', 'c'),
        ])
        
        self.assertEqual(hand_1, hand_2)
        self.assertGreaterEqual(hand_1, hand_2)


        # Higher straight

        hand_1 = structures.Hand([
            structures.Card('T', 'h'),
            structures.Card('9', 'h'),
            structures.Card('8', 'h'),
            structures.Card('7', 'h'),
            structures.Card('6', 'h'),
        ])

        hand_2 = structures.Hand([
            structures.Card('6', 'c'),
            structures.Card('5', 'c'),
            structures.Card('4', 'c'),
            structures.Card('3', 'c'),
            structures.Card('2', 'c'),
        ])
        
        self.assertGreater(hand_1, hand_2)
        self.assertGreaterEqual(hand_1, hand_2)


        # Straight higher than five to ace straight

        hand_1 = structures.Hand([
            structures.Card('6', 'h'),
            structures.Card('5', 'h'),
            structures.Card('4', 'h'),
            structures.Card('3', 'h'),
            structures.Card('2', 'h'),
        ])

        hand_2 = structures.Hand([
            structures.Card('5', 'c'),
            structures.Card('4', 'c'),
            structures.Card('3', 'c'),
            structures.Card('2', 'c'),
            structures.Card('A', 'c'),
        ])
        
        self.assertGreater(hand_1, hand_2)
        self.assertGreaterEqual(hand_1, hand_2)


    def test_four_of_a_kind_relations(self):


        """
        Runs test cases to check relations between four of a kind hands work as expected.
        """


        # Exactly same hand

        hand_1 = structures.Hand([
            structures.Card('T', 's'),
            structures.Card('T', 'h'),
            structures.Card('T', 'd'),
            structures.Card('T', 'c'),
            structures.Card('7', 's'),
        ])

        hand_2 = structures.Hand([
            structures.Card('T', 's'),
            structures.Card('T', 'h'),
            structures.Card('T', 'd'),
            structures.Card('T', 'c'),
            structures.Card('7', 's'),
        ])
        
        self.assertEqual(hand_1, hand_2)
        self.assertGreaterEqual(hand_1, hand_2)


        # Same hand, different kicker suits

        hand_1 = structures.Hand([
            structures.Card('T', 's'),
            structures.Card('T', 'h'),
            structures.Card('T', 'd'),
            structures.Card('T', 'c'),
            structures.Card('7', 's'),
        ])

        hand_2 = structures.Hand([
            structures.Card('T', 's'),
            structures.Card('T', 'h'),
            structures.Card('T', 'd'),
            structures.Card('T', 'c'),
            structures.Card('7', 'h'),
        ])

        self.assertEqual(hand_1, hand_2)
        self.assertGreaterEqual(hand_1, hand_2)
        

        # Same four of a kind, higher kicker

        hand_1 = structures.Hand([
            structures.Card('T', 's'),
            structures.Card('T', 'h'),
            structures.Card('T', 'd'),
            structures.Card('T', 'c'),
            structures.Card('8', 's'),
        ])

        hand_2 = structures.Hand([
            structures.Card('T', 's'),
            structures.Card('T', 'h'),
            structures.Card('T', 'd'),
            structures.Card('T', 'c'),
            structures.Card('7', 'h'),
        ])
        
        self.assertGreater(hand_1, hand_2)
        self.assertGreaterEqual(hand_1, hand_2)


        # Higher four of a kind, higher kicker

        hand_1 = structures.Hand([
            structures.Card('T', 's'),
            structures.Card('T', 'h'),
            structures.Card('T', 'd'),
            structures.Card('T', 'c'),
            structures.Card('5', 's'),
        ])

        hand_2 = structures.Hand([
            structures.Card('9', 's'),
            structures.Card('9', 'h'),
            structures.Card('9', 'd'),
            structures.Card('9', 'c'),
            structures.Card('3', 'h'),
        ])
        
        self.assertGreater(hand_1, hand_2)
        self.assertGreaterEqual(hand_1, hand_2)


        # Higher four of a kind, lower kicker

        hand_1 = structures.Hand([
            structures.Card('T', 's'),
            structures.Card('T', 'h'),
            structures.Card('T', 'd'),
            structures.Card('T', 'c'),
            structures.Card('2', 's'),
        ])

        hand_2 = structures.Hand([
            structures.Card('9', 's'),
            structures.Card('9', 'h'),
            structures.Card('9', 'd'),
            structures.Card('9', 'c'),
            structures.Card('K', 'h'),
        ])
        
        self.assertGreater(hand_1, hand_2)
        self.assertGreaterEqual(hand_1, hand_2)


    def test_full_house_relations(self):


        """
        Runs test cases to check relations between full house hands work as expected.
        """


        # Exactly same hand

        hand_1 = structures.Hand([
            structures.Card('Q', 's'),
            structures.Card('Q', 'h'),
            structures.Card('Q', 'd'),
            structures.Card('8', 's'),
            structures.Card('8', 'd'),
        ])

        hand_2 = structures.Hand([
            structures.Card('Q', 's'),
            structures.Card('Q', 'h'),
            structures.Card('Q', 'd'),
            structures.Card('8', 's'),
            structures.Card('8', 'd'),
        ])
        
        self.assertEqual(hand_1, hand_2)
        self.assertGreaterEqual(hand_1, hand_2)


        # Same hand, different suits

        hand_1 = structures.Hand([
            structures.Card('Q', 's'),
            structures.Card('Q', 'h'),
            structures.Card('Q', 'd'),
            structures.Card('8', 's'),
            structures.Card('8', 'd'),
        ])

        hand_2 = structures.Hand([
            structures.Card('Q', 'h'),
            structures.Card('Q', 'd'),
            structures.Card('Q', 'c'),
            structures.Card('8', 'h'),
            structures.Card('8', 'c'),
        ])

        self.assertEqual(hand_1, hand_2)
        self.assertGreaterEqual(hand_1, hand_2)
        

        # Same three of a kind, higher pair

        hand_1 = structures.Hand([
            structures.Card('Q', 's'),
            structures.Card('Q', 'h'),
            structures.Card('Q', 'd'),
            structures.Card('A', 's'),
            structures.Card('A', 'd'),
        ])

        hand_2 = structures.Hand([
            structures.Card('Q', 'h'),
            structures.Card('Q', 'd'),
            structures.Card('Q', 'c'),
            structures.Card('8', 'h'),
            structures.Card('8', 'c'),
        ])
        
        self.assertGreater(hand_1, hand_2)
        self.assertGreaterEqual(hand_1, hand_2)


        # Higher three of a kind, higher pair

        hand_1 = structures.Hand([
            structures.Card('Q', 's'),
            structures.Card('Q', 'h'),
            structures.Card('Q', 'd'),
            structures.Card('9', 's'),
            structures.Card('9', 'd'),
        ])

        hand_2 = structures.Hand([
            structures.Card('T', 'h'),
            structures.Card('T', 'd'),
            structures.Card('T', 'c'),
            structures.Card('3', 'h'),
            structures.Card('3', 'c'),
        ])
        
        self.assertGreater(hand_1, hand_2)
        self.assertGreaterEqual(hand_1, hand_2)


        # Higher three of a kind, lower pair

        hand_1 = structures.Hand([
            structures.Card('Q', 's'),
            structures.Card('Q', 'h'),
            structures.Card('Q', 'd'),
            structures.Card('3', 's'),
            structures.Card('3', 'd'),
        ])

        hand_2 = structures.Hand([
            structures.Card('T', 'h'),
            structures.Card('T', 'd'),
            structures.Card('T', 'c'),
            structures.Card('9', 'h'),
            structures.Card('9', 'c'),
        ])
        
        self.assertGreater(hand_1, hand_2)
        self.assertGreaterEqual(hand_1, hand_2)


    def test_flush_relations(self):


        """
        Runs test cases to check relations between flush hands work as expected.
        """


        # Exactly same hand

        hand_1 = structures.Hand([
            structures.Card('Q', 'h'),
            structures.Card('J', 'h'),
            structures.Card('7', 'h'),
            structures.Card('4', 'h'),
            structures.Card('2', 'h'),
        ])

        hand_2 = structures.Hand([
            structures.Card('Q', 'h'),
            structures.Card('J', 'h'),
            structures.Card('7', 'h'),
            structures.Card('4', 'h'),
            structures.Card('2', 'h'),
        ])
        
        self.assertEqual(hand_1, hand_2)
        self.assertGreaterEqual(hand_1, hand_2)


        # Same hand, different suits

        hand_1 = structures.Hand([
            structures.Card('Q', 'h'),
            structures.Card('J', 'h'),
            structures.Card('7', 'h'),
            structures.Card('4', 'h'),
            structures.Card('2', 'h'),
        ])

        hand_2 = structures.Hand([
            structures.Card('Q', 'c'),
            structures.Card('J', 'c'),
            structures.Card('7', 'c'),
            structures.Card('4', 'c'),
            structures.Card('2', 'c'),
        ])

        self.assertEqual(hand_1, hand_2)
        self.assertGreaterEqual(hand_1, hand_2)
        

        # Flush with all cards higher

        hand_1 = structures.Hand([
            structures.Card('A', 's'),
            structures.Card('K', 's'),
            structures.Card('Q', 's'),
            structures.Card('J', 's'),
            structures.Card('9', 's'),
        ])

        hand_2 = structures.Hand([
            structures.Card('8', 'd'),
            structures.Card('6', 'd'),
            structures.Card('5', 'd'),
            structures.Card('3', 'd'),
            structures.Card('2', 'd'),
        ])
  
        self.assertGreater(hand_1, hand_2)
        self.assertGreaterEqual(hand_1, hand_2)


        # Flush with higher main card, lower secondary cards

        hand_1 = structures.Hand([
            structures.Card('A', 'c'),
            structures.Card('6', 's'),
            structures.Card('5', 's'),
            structures.Card('3', 's'),
            structures.Card('2', 's'),
        ])

        hand_2 = structures.Hand([
            structures.Card('K', 's'),
            structures.Card('Q', 'c'),
            structures.Card('J', 'c'),
            structures.Card('9', 'c'),
            structures.Card('8', 'c'),
        ])
  
        self.assertGreater(hand_1, hand_2)
        self.assertGreaterEqual(hand_1, hand_2)


    def test_straight_relations(self):


        """
        Runs test cases to check relations between straight hands work as expected.
        """


        # Exactly same hand

        hand_1 = structures.Hand([
            structures.Card('7', 's'),
            structures.Card('6', 'h'),
            structures.Card('5', 'd'),
            structures.Card('4', 's'),
            structures.Card('3', 'd'),
        ])

        hand_2 = structures.Hand([
            structures.Card('7', 's'),
            structures.Card('6', 'h'),
            structures.Card('5', 'd'),
            structures.Card('4', 's'),
            structures.Card('3', 'd'),
        ])
        
        self.assertEqual(hand_1, hand_2)
        self.assertGreaterEqual(hand_1, hand_2)


        # Same hand, different suits

        hand_1 = structures.Hand([
            structures.Card('7', 's'),
            structures.Card('6', 'h'),
            structures.Card('5', 'd'),
            structures.Card('4', 's'),
            structures.Card('3', 'd'),
        ])

        hand_2 = structures.Hand([
            structures.Card('7', 's'),
            structures.Card('6', 's'),
            structures.Card('5', 'd'),
            structures.Card('4', 'c'),
            structures.Card('3', 'd'),
        ])

        self.assertEqual(hand_1, hand_2)
        self.assertGreaterEqual(hand_1, hand_2)
        

        # Higher straight

        hand_1 = structures.Hand([
            structures.Card('8', 'd'),
            structures.Card('7', 's'),
            structures.Card('6', 'h'),
            structures.Card('5', 'd'),
            structures.Card('4', 's'),
        ])

        hand_2 = structures.Hand([
            structures.Card('7', 's'),
            structures.Card('6', 'h'),
            structures.Card('5', 'd'),
            structures.Card('4', 's'),
            structures.Card('3', 'd'),
        ])
        
        self.assertGreater(hand_1, hand_2)
        self.assertGreaterEqual(hand_1, hand_2)


        # Straight higher than five to ace straight

        hand_1 = structures.Hand([
            structures.Card('6', 'd'),
            structures.Card('5', 's'),
            structures.Card('4', 'h'),
            structures.Card('3', 'd'),
            structures.Card('2', 's'),
        ])

        hand_2 = structures.Hand([
            structures.Card('5', 's'),
            structures.Card('4', 'h'),
            structures.Card('3', 'd'),
            structures.Card('2', 's'),
            structures.Card('A', 'd'),
        ])
        
        self.assertGreater(hand_1, hand_2)
        self.assertGreaterEqual(hand_1, hand_2)


    def test_three_of_a_kind_relations(self):


        """
        Runs test cases to check relations between three of a kind hands work as expected.
        """


        # Exactly same hand

        hand_1 = structures.Hand([
            structures.Card('Q', 's'),
            structures.Card('Q', 'h'),
            structures.Card('Q', 'd'),
            structures.Card('7', 's'),
            structures.Card('4', 'd'),
        ])

        hand_2 = structures.Hand([
            structures.Card('Q', 's'),
            structures.Card('Q', 'h'),
            structures.Card('Q', 'd'),
            structures.Card('7', 's'),
            structures.Card('4', 'd'),
        ])
        
        self.assertEqual(hand_1, hand_2)
        self.assertGreaterEqual(hand_1, hand_2)


        # Same hand, different suits

        hand_1 = structures.Hand([
            structures.Card('Q', 's'),
            structures.Card('Q', 'h'),
            structures.Card('Q', 'd'),
            structures.Card('7', 's'),
            structures.Card('4', 'd'),
        ])

        hand_2 = structures.Hand([
            structures.Card('Q', 'h'),
            structures.Card('Q', 'd'),
            structures.Card('Q', 'c'),
            structures.Card('7', 'h'),
            structures.Card('4', 'c'),
        ])

        self.assertEqual(hand_1, hand_2)
        self.assertGreaterEqual(hand_1, hand_2)
        

        # Same three of a kind, both kickers higher

        hand_1 = structures.Hand([
            structures.Card('Q', 's'),
            structures.Card('Q', 'h'),
            structures.Card('Q', 'd'),
            structures.Card('T', 's'),
            structures.Card('8', 'd'),
        ])

        hand_2 = structures.Hand([
            structures.Card('Q', 'h'),
            structures.Card('Q', 'd'),
            structures.Card('Q', 'c'),
            structures.Card('5', 'h'),
            structures.Card('2', 'c'),
        ])

        self.assertGreater(hand_1, hand_2)
        self.assertGreaterEqual(hand_1, hand_2)


        # Same three of a kind, main kicker higher, secondary kicker lower

        hand_1 = structures.Hand([
            structures.Card('Q', 's'),
            structures.Card('Q', 'h'),
            structures.Card('Q', 'd'),
            structures.Card('T', 's'),
            structures.Card('2', 'd'),
        ])

        hand_2 = structures.Hand([
            structures.Card('Q', 'h'),
            structures.Card('Q', 'd'),
            structures.Card('Q', 'c'),
            structures.Card('9', 'h'),
            structures.Card('5', 'c'),
        ])

        self.assertGreater(hand_1, hand_2)
        self.assertGreaterEqual(hand_1, hand_2)


        # Higher three of a kind, both kickers higher

        hand_1 = structures.Hand([
            structures.Card('K', 's'),
            structures.Card('K', 'h'),
            structures.Card('K', 'd'),
            structures.Card('T', 's'),
            structures.Card('8', 'd'),
        ])

        hand_2 = structures.Hand([
            structures.Card('Q', 'h'),
            structures.Card('Q', 'd'),
            structures.Card('Q', 'c'),
            structures.Card('5', 'h'),
            structures.Card('2', 'c'),
        ])

        self.assertGreater(hand_1, hand_2)
        self.assertGreaterEqual(hand_1, hand_2)


        # Same three of a kind, both kickers lower

        hand_1 = structures.Hand([
            structures.Card('K', 's'),
            structures.Card('K', 'h'),
            structures.Card('K', 'd'),
            structures.Card('T', 's'),
            structures.Card('2', 'd'),
        ])

        hand_2 = structures.Hand([
            structures.Card('Q', 'h'),
            structures.Card('Q', 'd'),
            structures.Card('Q', 'c'),
            structures.Card('9', 'h'),
            structures.Card('5', 'c'),
        ])

        self.assertGreater(hand_1, hand_2)
        self.assertGreaterEqual(hand_1, hand_2)


    def test_two_pair_relations(self):


        """
        Runs test cases to check relations between two pair hands work as expected.
        """


        # Exactly same hand

        hand_1 = structures.Hand([
            structures.Card('A', 's'),
            structures.Card('A', 'h'),
            structures.Card('6', 'd'),
            structures.Card('6', 's'),
            structures.Card('T', 'd'),
        ])

        hand_2 = structures.Hand([
            structures.Card('A', 's'),
            structures.Card('A', 'h'),
            structures.Card('6', 'd'),
            structures.Card('6', 's'),
            structures.Card('T', 'd'),
        ])
        
        self.assertEqual(hand_1, hand_2)
        self.assertGreaterEqual(hand_1, hand_2)


        # Same hand, different suits

        hand_1 = structures.Hand([
            structures.Card('A', 's'),
            structures.Card('A', 'h'),
            structures.Card('6', 'd'),
            structures.Card('6', 's'),
            structures.Card('T', 'd'),
        ])

        hand_2 = structures.Hand([
            structures.Card('A', 's'),
            structures.Card('A', 'h'),
            structures.Card('6', 'h'),
            structures.Card('6', 'c'),
            structures.Card('T', 'd'),
        ])

        self.assertEqual(hand_1, hand_2)
        self.assertGreaterEqual(hand_1, hand_2)
        

        # Same pairs, higher kicker

        hand_1 = structures.Hand([
            structures.Card('A', 's'),
            structures.Card('A', 'h'),
            structures.Card('6', 'c'),
            structures.Card('6', 'h'),
            structures.Card('T', 'd'),
        ])

        hand_2 = structures.Hand([
            structures.Card('A', 's'),
            structures.Card('A', 'c'),
            structures.Card('6', 'h'),
            structures.Card('6', 'd'),
            structures.Card('9', 'h'),
        ])

        self.assertGreater(hand_1, hand_2)
        self.assertGreaterEqual(hand_1, hand_2)


        # Same main pair, higher secondary pair and kicker

        hand_1 = structures.Hand([
            structures.Card('A', 's'),
            structures.Card('A', 'h'),
            structures.Card('K', 'c'),
            structures.Card('K', 'h'),
            structures.Card('T', 'd'),
        ])

        hand_2 = structures.Hand([
            structures.Card('A', 's'),
            structures.Card('A', 'c'),
            structures.Card('6', 'h'),
            structures.Card('6', 'd'),
            structures.Card('9', 'h'),
        ])

        self.assertGreater(hand_1, hand_2)
        self.assertGreaterEqual(hand_1, hand_2)


        # Same main pair, higher secondary pair, lower kicker

        hand_1 = structures.Hand([
            structures.Card('A', 's'),
            structures.Card('A', 'h'),
            structures.Card('K', 'c'),
            structures.Card('K', 'h'),
            structures.Card('T', 'd'),
        ])

        hand_2 = structures.Hand([
            structures.Card('A', 's'),
            structures.Card('A', 'c'),
            structures.Card('6', 'h'),
            structures.Card('6', 'd'),
            structures.Card('K', 'h'),
        ])

        self.assertGreater(hand_1, hand_2)
        self.assertGreaterEqual(hand_1, hand_2)


        # Higher main pair, secondary pair and kicker

        hand_1 = structures.Hand([
            structures.Card('A', 's'),
            structures.Card('A', 'h'),
            structures.Card('8', 'c'),
            structures.Card('8', 'h'),
            structures.Card('K', 'd'),
        ])

        hand_2 = structures.Hand([
            structures.Card('Q', 's'),
            structures.Card('Q', 'c'),
            structures.Card('6', 'h'),
            structures.Card('6', 'd'),
            structures.Card('J', 'h'),
        ])

        self.assertGreater(hand_1, hand_2)
        self.assertGreaterEqual(hand_1, hand_2)


        # Higher main pair, lower secondary pair and kicker

        hand_1 = structures.Hand([
            structures.Card('A', 's'),
            structures.Card('A', 'h'),
            structures.Card('2', 'c'),
            structures.Card('2', 'h'),
            structures.Card('3', 'd'),
        ])

        hand_2 = structures.Hand([
            structures.Card('Q', 's'),
            structures.Card('Q', 'c'),
            structures.Card('6', 'h'),
            structures.Card('6', 'd'),
            structures.Card('J', 'h'),
        ])

        self.assertGreater(hand_1, hand_2)
        self.assertGreaterEqual(hand_1, hand_2)


    def test_pair_relations(self):


        """
        Runs test cases to check relations between pair hands work as expected.
        """


        # Exactly same hand

        hand_1 = structures.Hand([
            structures.Card('3', 's'),
            structures.Card('3', 'h'),
            structures.Card('6', 'd'),
            structures.Card('4', 's'),
            structures.Card('2', 'd'),
        ])

        hand_2 = structures.Hand([
            structures.Card('3', 's'),
            structures.Card('3', 'h'),
            structures.Card('6', 'd'),
            structures.Card('4', 's'),
            structures.Card('2', 'd'),
        ])
        
        self.assertEqual(hand_1, hand_2)
        self.assertGreaterEqual(hand_1, hand_2)


        # Same hand, different suits

        hand_1 = structures.Hand([
            structures.Card('3', 's'),
            structures.Card('3', 'h'),
            structures.Card('6', 'd'),
            structures.Card('4', 's'),
            structures.Card('2', 'd'),
        ])

        hand_2 = structures.Hand([
            structures.Card('3', 'h'),
            structures.Card('3', 'd'),
            structures.Card('6', 's'),
            structures.Card('4', 'c'),
            structures.Card('2', 'd'),
        ])

        self.assertEqual(hand_1, hand_2)
        self.assertGreaterEqual(hand_1, hand_2)
        

        # Same pairs, higher kickers

        hand_1 = structures.Hand([
            structures.Card('A', 's'),
            structures.Card('A', 'h'),
            structures.Card('K', 'c'),
            structures.Card('T', 'h'),
            structures.Card('9', 'd'),
        ])

        hand_2 = structures.Hand([
            structures.Card('A', 's'),
            structures.Card('A', 'c'),
            structures.Card('6', 'h'),
            structures.Card('4', 'd'),
            structures.Card('2', 'h'),
        ])

        self.assertGreater(hand_1, hand_2)
        self.assertGreaterEqual(hand_1, hand_2)


        # Same pairs, higher main kicker, lower secondary kickers

        hand_1 = structures.Hand([
            structures.Card('A', 's'),
            structures.Card('A', 'h'),
            structures.Card('K', 'c'),
            structures.Card('3', 'h'),
            structures.Card('2', 'd'),
        ])

        hand_2 = structures.Hand([
            structures.Card('A', 's'),
            structures.Card('A', 'c'),
            structures.Card('Q', 'h'),
            structures.Card('J', 'd'),
            structures.Card('T', 'h'),
        ])

        self.assertGreater(hand_1, hand_2)
        self.assertGreaterEqual(hand_1, hand_2)


        # Higher pair, higher kickers

        hand_1 = structures.Hand([
            structures.Card('A', 's'),
            structures.Card('A', 'h'),
            structures.Card('K', 'c'),
            structures.Card('J', 'h'),
            structures.Card('8', 'd'),
        ])

        hand_2 = structures.Hand([
            structures.Card('K', 's'),
            structures.Card('K', 'c'),
            structures.Card('5', 'h'),
            structures.Card('3', 'd'),
            structures.Card('2', 'h'),
        ])

        self.assertGreater(hand_1, hand_2)
        self.assertGreaterEqual(hand_1, hand_2)


        # Higher pair, lower kickers

        hand_1 = structures.Hand([
            structures.Card('A', 's'),
            structures.Card('A', 'h'),
            structures.Card('4', 'c'),
            structures.Card('3', 'h'),
            structures.Card('2', 'd'),
        ])

        hand_2 = structures.Hand([
            structures.Card('K', 's'),
            structures.Card('K', 'c'),
            structures.Card('Q', 'h'),
            structures.Card('J', 'd'),
            structures.Card('T', 'h'),
        ])

        self.assertGreater(hand_1, hand_2)
        self.assertGreaterEqual(hand_1, hand_2)


    def test_high_card_relations(self):


        """
        Runs test cases to check relations between high card hands work as expected.
        """


        # Exactly same hand

        hand_1 = structures.Hand([
            structures.Card('T', 's'),
            structures.Card('8', 'h'),
            structures.Card('5', 'd'),
            structures.Card('3', 's'),
            structures.Card('2', 'd'),
        ])

        hand_2 = structures.Hand([
            structures.Card('T', 's'),
            structures.Card('8', 'h'),
            structures.Card('5', 'd'),
            structures.Card('3', 's'),
            structures.Card('2', 'd'),
        ])
        
        self.assertEqual(hand_1, hand_2)
        self.assertGreaterEqual(hand_1, hand_2)


        # Same hand, different suits

        hand_1 = structures.Hand([
            structures.Card('T', 's'),
            structures.Card('8', 'h'),
            structures.Card('5', 'd'),
            structures.Card('3', 's'),
            structures.Card('2', 'd'),
        ])

        hand_2 = structures.Hand([
            structures.Card('T', 'h'),
            structures.Card('8', 'd'),
            structures.Card('5', 's'),
            structures.Card('3', 'c'),
            structures.Card('2', 'd'),
        ])

        self.assertEqual(hand_1, hand_2)
        self.assertGreaterEqual(hand_1, hand_2)
        

        # All cards higher

        hand_1 = structures.Hand([
            structures.Card('A', 'h'),
            structures.Card('K', 'd'),
            structures.Card('J', 's'),
            structures.Card('T', 'c'),
            structures.Card('8', 'd'),
        ])

        hand_2 = structures.Hand([
            structures.Card('7', 'h'),
            structures.Card('6', 'd'),
            structures.Card('5', 's'),
            structures.Card('3', 'c'),
            structures.Card('2', 'd'),
        ])


        # Main card higher, all kickers lower

        hand_1 = structures.Hand([
            structures.Card('A', 'h'),
            structures.Card('6', 'd'),
            structures.Card('5', 's'),
            structures.Card('3', 'c'),
            structures.Card('2', 'd'),
        ])

        hand_2 = structures.Hand([
            structures.Card('7', 'h'),
            structures.Card('K', 'd'),
            structures.Card('J', 's'),
            structures.Card('T', 'c'),
            structures.Card('8', 'd'),
        ])


        self.assertGreater(hand_1, hand_2)
        self.assertGreaterEqual(hand_1, hand_2)


    def test_different_category_relations(self):
        

        """
        Runs test cases to check relations between different categories.
        """

        
        # Resources

        royal_flush_hand = structures.Hand([
            structures.Card('A', 's'),
            structures.Card('K', 's'),
            structures.Card('Q', 's'),
            structures.Card('J', 's'),
            structures.Card('T', 's'),
        ])

        straight_flush_hand = structures.Hand([
            structures.Card('5', 's'),
            structures.Card('4', 's'),
            structures.Card('3', 's'),
            structures.Card('2', 's'),
            structures.Card('A', 's'),
        ])

        four_of_a_kind_hand = structures.Hand([
            structures.Card('6', 's'),
            structures.Card('6', 'h'),
            structures.Card('6', 'd'),
            structures.Card('6', 'c'),
            structures.Card('7', 's'),
        ])

        full_house_hand = structures.Hand([
            structures.Card('8', 's'),
            structures.Card('8', 'h'),
            structures.Card('8', 'd'),
            structures.Card('9', 's'),
            structures.Card('9', 'd'),
        ])

        flush_hand = structures.Hand([
            structures.Card('9', 'h'),
            structures.Card('8', 'h'),
            structures.Card('7', 'h'),
            structures.Card('6', 'h'),
            structures.Card('4', 'h'),
        ])

        straight_hand = structures.Hand([
            structures.Card('T', 's'),
            structures.Card('9', 'h'),
            structures.Card('8', 'd'),
            structures.Card('7', 's'),
            structures.Card('6', 'd'),
        ])

        three_of_a_kind_hand = structures.Hand([
            structures.Card('J', 's'),
            structures.Card('J', 'h'),
            structures.Card('J', 'd'),
            structures.Card('9', 's'),
            structures.Card('8', 'd'),
        ])

        two_pair_hand = structures.Hand([
            structures.Card('Q', 's'),
            structures.Card('Q', 'h'),
            structures.Card('J', 'd'),
            structures.Card('J', 's'),
            structures.Card('T', 'd'),
        ])

        pair_hand = structures.Hand([
            structures.Card('K', 's'),
            structures.Card('K', 'h'),
            structures.Card('Q', 's'),
            structures.Card('J', 's'),
            structures.Card('T', 's'),
        ])

        high_card_hand = structures.Hand([
            structures.Card('A', 's'),
            structures.Card('K', 's'),
            structures.Card('Q', 's'),
            structures.Card('J', 's'),
            structures.Card('9', 'h'),
        ])


        # Compare to royal flush

        self.assertGreater(royal_flush_hand, straight_flush_hand)
        self.assertGreaterEqual(royal_flush_hand, straight_flush_hand)

        self.assertGreater(royal_flush_hand, four_of_a_kind_hand)
        self.assertGreaterEqual(royal_flush_hand, four_of_a_kind_hand)

        self.assertGreater(royal_flush_hand, full_house_hand)
        self.assertGreaterEqual(royal_flush_hand, full_house_hand)

        self.assertGreater(royal_flush_hand, flush_hand)
        self.assertGreaterEqual(royal_flush_hand, flush_hand)

        self.assertGreater(royal_flush_hand, straight_hand)
        self.assertGreaterEqual(royal_flush_hand, straight_hand)

        self.assertGreater(royal_flush_hand, three_of_a_kind_hand)
        self.assertGreaterEqual(royal_flush_hand, three_of_a_kind_hand)

        self.assertGreater(royal_flush_hand, two_pair_hand)
        self.assertGreaterEqual(royal_flush_hand, two_pair_hand)

        self.assertGreater(royal_flush_hand, pair_hand)
        self.assertGreaterEqual(royal_flush_hand, pair_hand)

        self.assertGreater(royal_flush_hand, high_card_hand)
        self.assertGreaterEqual(royal_flush_hand, high_card_hand)


        # Compare to straight flush

        self.assertGreater(straight_flush_hand, four_of_a_kind_hand)
        self.assertGreaterEqual(straight_flush_hand, four_of_a_kind_hand)

        self.assertGreater(straight_flush_hand, full_house_hand)
        self.assertGreaterEqual(straight_flush_hand, full_house_hand)

        self.assertGreater(straight_flush_hand, flush_hand)
        self.assertGreaterEqual(straight_flush_hand, flush_hand)

        self.assertGreater(straight_flush_hand, straight_hand)
        self.assertGreaterEqual(straight_flush_hand, straight_hand)

        self.assertGreater(straight_flush_hand, three_of_a_kind_hand)
        self.assertGreaterEqual(straight_flush_hand, three_of_a_kind_hand)

        self.assertGreater(straight_flush_hand, two_pair_hand)
        self.assertGreaterEqual(straight_flush_hand, two_pair_hand)

        self.assertGreater(straight_flush_hand, pair_hand)
        self.assertGreaterEqual(straight_flush_hand, pair_hand)

        self.assertGreater(straight_flush_hand, high_card_hand)
        self.assertGreaterEqual(straight_flush_hand, high_card_hand)


        # Compare to four of a kind

        self.assertGreater(four_of_a_kind_hand, full_house_hand)
        self.assertGreaterEqual(four_of_a_kind_hand, full_house_hand)

        self.assertGreater(four_of_a_kind_hand, flush_hand)
        self.assertGreaterEqual(four_of_a_kind_hand, flush_hand)

        self.assertGreater(four_of_a_kind_hand, straight_hand)
        self.assertGreaterEqual(four_of_a_kind_hand, straight_hand)

        self.assertGreater(four_of_a_kind_hand, three_of_a_kind_hand)
        self.assertGreaterEqual(four_of_a_kind_hand, three_of_a_kind_hand)

        self.assertGreater(four_of_a_kind_hand, two_pair_hand)
        self.assertGreaterEqual(four_of_a_kind_hand, two_pair_hand)

        self.assertGreater(four_of_a_kind_hand, pair_hand)
        self.assertGreaterEqual(four_of_a_kind_hand, pair_hand)

        self.assertGreater(four_of_a_kind_hand, high_card_hand)
        self.assertGreaterEqual(four_of_a_kind_hand, high_card_hand)


        # Compare to full house

        self.assertGreater(full_house_hand, flush_hand)
        self.assertGreaterEqual(full_house_hand, flush_hand)

        self.assertGreater(full_house_hand, straight_hand)
        self.assertGreaterEqual(full_house_hand, straight_hand)

        self.assertGreater(full_house_hand, three_of_a_kind_hand)
        self.assertGreaterEqual(full_house_hand, three_of_a_kind_hand)

        self.assertGreater(full_house_hand, two_pair_hand)
        self.assertGreaterEqual(full_house_hand, two_pair_hand)

        self.assertGreater(full_house_hand, pair_hand)
        self.assertGreaterEqual(full_house_hand, pair_hand)

        self.assertGreater(full_house_hand, high_card_hand)
        self.assertGreaterEqual(full_house_hand, high_card_hand)


        # Compare to flush

        self.assertGreater(flush_hand, straight_hand)
        self.assertGreaterEqual(flush_hand, straight_hand)

        self.assertGreater(flush_hand, three_of_a_kind_hand)
        self.assertGreaterEqual(flush_hand, three_of_a_kind_hand)

        self.assertGreater(flush_hand, two_pair_hand)
        self.assertGreaterEqual(flush_hand, two_pair_hand)

        self.assertGreater(flush_hand, pair_hand)
        self.assertGreaterEqual(flush_hand, pair_hand)

        self.assertGreater(flush_hand, high_card_hand)
        self.assertGreaterEqual(flush_hand, high_card_hand)


        # Compare to straight

        self.assertGreater(straight_hand, three_of_a_kind_hand)
        self.assertGreaterEqual(straight_hand, three_of_a_kind_hand)

        self.assertGreater(straight_hand, two_pair_hand)
        self.assertGreaterEqual(straight_hand, two_pair_hand)

        self.assertGreater(straight_hand, pair_hand)
        self.assertGreaterEqual(straight_hand, pair_hand)

        self.assertGreater(straight_hand, high_card_hand)
        self.assertGreaterEqual(straight_hand, high_card_hand)


        # Compare to three of a kind

        self.assertGreater(three_of_a_kind_hand, two_pair_hand)
        self.assertGreaterEqual(three_of_a_kind_hand, two_pair_hand)

        self.assertGreater(three_of_a_kind_hand, pair_hand)
        self.assertGreaterEqual(three_of_a_kind_hand, pair_hand)

        self.assertGreater(three_of_a_kind_hand, high_card_hand)
        self.assertGreaterEqual(three_of_a_kind_hand, high_card_hand)


        # Compare to two pair

        self.assertGreater(two_pair_hand, pair_hand)
        self.assertGreaterEqual(two_pair_hand, pair_hand)

        self.assertGreater(two_pair_hand, high_card_hand)
        self.assertGreaterEqual(two_pair_hand, high_card_hand)


        # Compare to pair

        self.assertGreater(pair_hand, high_card_hand)
        self.assertGreaterEqual(pair_hand, high_card_hand)


if __name__ == '__main__':
    main()