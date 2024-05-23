"""
Defines unit tests on Hand relations.
"""


import sys
sys.path.insert(0, '.')


from unittest import main, TestCase


import pokerpy as pk


class TestHandRelations(TestCase):


    """
    Runs unit tests on Hand class relations.
    """


    def test_royal_flush_relations(self):


        """
        Runs test cases to check relations between royal flush hands work as expected.
        """


        # Exactly same hand

        hand_1 = pk.Hand([
            pk.Card('A', 's'),
            pk.Card('K', 's'),
            pk.Card('Q', 's'),
            pk.Card('J', 's'),
            pk.Card('T', 's'),
        ])

        hand_2 = pk.Hand([
            pk.Card('A', 's'),
            pk.Card('K', 's'),
            pk.Card('Q', 's'),
            pk.Card('J', 's'),
            pk.Card('T', 's'),
        ])
        
        self.assertEqual(hand_1, hand_2)
        self.assertGreaterEqual(hand_1, hand_2)


        # Same hand, different suits

        hand_1 = pk.Hand([
            pk.Card('A', 'c'),
            pk.Card('K', 'c'),
            pk.Card('Q', 'c'),
            pk.Card('J', 'c'),
            pk.Card('T', 'c'),
        ])

        hand_2 = pk.Hand([
            pk.Card('A', 's'),
            pk.Card('K', 's'),
            pk.Card('Q', 's'),
            pk.Card('J', 's'),
            pk.Card('T', 's'),
        ])
        
        self.assertEqual(hand_1, hand_2)
        self.assertGreaterEqual(hand_1, hand_2)


    def test_straight_flush_relations(self):


        """
        Runs test cases to check relations between royal flush hands work as expected.
        """


        # Exactly same hand

        hand_1 = pk.Hand([
            pk.Card('T', 's'),
            pk.Card('9', 's'),
            pk.Card('8', 's'),
            pk.Card('7', 's'),
            pk.Card('6', 's'),
        ])

        hand_2 = pk.Hand([
            pk.Card('T', 's'),
            pk.Card('9', 's'),
            pk.Card('8', 's'),
            pk.Card('7', 's'),
            pk.Card('6', 's'),
        ])
        
        self.assertEqual(hand_1, hand_2)
        self.assertGreaterEqual(hand_1, hand_2)


        # Same hand, different suits

        hand_1 = pk.Hand([
            pk.Card('T', 'h'),
            pk.Card('9', 'h'),
            pk.Card('8', 'h'),
            pk.Card('7', 'h'),
            pk.Card('6', 'h'),
        ])

        hand_2 = pk.Hand([
            pk.Card('T', 'c'),
            pk.Card('9', 'c'),
            pk.Card('8', 'c'),
            pk.Card('7', 'c'),
            pk.Card('6', 'c'),
        ])
        
        self.assertEqual(hand_1, hand_2)
        self.assertGreaterEqual(hand_1, hand_2)


        # Higher straight

        hand_1 = pk.Hand([
            pk.Card('T', 'h'),
            pk.Card('9', 'h'),
            pk.Card('8', 'h'),
            pk.Card('7', 'h'),
            pk.Card('6', 'h'),
        ])

        hand_2 = pk.Hand([
            pk.Card('6', 'c'),
            pk.Card('5', 'c'),
            pk.Card('4', 'c'),
            pk.Card('3', 'c'),
            pk.Card('2', 'c'),
        ])
        
        self.assertGreater(hand_1, hand_2)
        self.assertGreaterEqual(hand_1, hand_2)


        # Straight higher than ace to five straight

        hand_1 = pk.Hand([
            pk.Card('6', 'h'),
            pk.Card('5', 'h'),
            pk.Card('4', 'h'),
            pk.Card('3', 'h'),
            pk.Card('2', 'h'),
        ])

        hand_2 = pk.Hand([
            pk.Card('5', 'c'),
            pk.Card('4', 'c'),
            pk.Card('3', 'c'),
            pk.Card('2', 'c'),
            pk.Card('A', 'c'),
        ])
        
        self.assertGreater(hand_1, hand_2)
        self.assertGreaterEqual(hand_1, hand_2)


    def test_four_of_a_kind_relations(self):


        """
        Runs test cases to check relations between four of a kind hands work as expected.
        """


        # Exactly same hand

        hand_1 = pk.Hand([
            pk.Card('T', 's'),
            pk.Card('T', 'h'),
            pk.Card('T', 'd'),
            pk.Card('T', 'c'),
            pk.Card('7', 's'),
        ])

        hand_2 = pk.Hand([
            pk.Card('T', 's'),
            pk.Card('T', 'h'),
            pk.Card('T', 'd'),
            pk.Card('T', 'c'),
            pk.Card('7', 's'),
        ])
        
        self.assertEqual(hand_1, hand_2)
        self.assertGreaterEqual(hand_1, hand_2)


        # Same hand, different kicker suits

        hand_1 = pk.Hand([
            pk.Card('T', 's'),
            pk.Card('T', 'h'),
            pk.Card('T', 'd'),
            pk.Card('T', 'c'),
            pk.Card('7', 's'),
        ])

        hand_2 = pk.Hand([
            pk.Card('T', 's'),
            pk.Card('T', 'h'),
            pk.Card('T', 'd'),
            pk.Card('T', 'c'),
            pk.Card('7', 'h'),
        ])

        self.assertEqual(hand_1, hand_2)
        self.assertGreaterEqual(hand_1, hand_2)
        

        # Same four of a kind, higher kicker

        hand_1 = pk.Hand([
            pk.Card('T', 's'),
            pk.Card('T', 'h'),
            pk.Card('T', 'd'),
            pk.Card('T', 'c'),
            pk.Card('8', 's'),
        ])

        hand_2 = pk.Hand([
            pk.Card('T', 's'),
            pk.Card('T', 'h'),
            pk.Card('T', 'd'),
            pk.Card('T', 'c'),
            pk.Card('7', 'h'),
        ])
        
        self.assertGreater(hand_1, hand_2)
        self.assertGreaterEqual(hand_1, hand_2)


        # Higher four of a kind, higher kicker

        hand_1 = pk.Hand([
            pk.Card('T', 's'),
            pk.Card('T', 'h'),
            pk.Card('T', 'd'),
            pk.Card('T', 'c'),
            pk.Card('5', 's'),
        ])

        hand_2 = pk.Hand([
            pk.Card('9', 's'),
            pk.Card('9', 'h'),
            pk.Card('9', 'd'),
            pk.Card('9', 'c'),
            pk.Card('3', 'h'),
        ])
        
        self.assertGreater(hand_1, hand_2)
        self.assertGreaterEqual(hand_1, hand_2)


        # Higher four of a kind, lower kicker

        hand_1 = pk.Hand([
            pk.Card('T', 's'),
            pk.Card('T', 'h'),
            pk.Card('T', 'd'),
            pk.Card('T', 'c'),
            pk.Card('2', 's'),
        ])

        hand_2 = pk.Hand([
            pk.Card('9', 's'),
            pk.Card('9', 'h'),
            pk.Card('9', 'd'),
            pk.Card('9', 'c'),
            pk.Card('K', 'h'),
        ])
        
        self.assertGreater(hand_1, hand_2)
        self.assertGreaterEqual(hand_1, hand_2)


    def test_full_house_relations(self):


        """
        Runs test cases to check relations between full house hands work as expected.
        """


        # Exactly same hand

        hand_1 = pk.Hand([
            pk.Card('Q', 's'),
            pk.Card('Q', 'h'),
            pk.Card('Q', 'd'),
            pk.Card('8', 's'),
            pk.Card('8', 'd'),
        ])

        hand_2 = pk.Hand([
            pk.Card('Q', 's'),
            pk.Card('Q', 'h'),
            pk.Card('Q', 'd'),
            pk.Card('8', 's'),
            pk.Card('8', 'd'),
        ])
        
        self.assertEqual(hand_1, hand_2)
        self.assertGreaterEqual(hand_1, hand_2)


        # Same hand, different suits

        hand_1 = pk.Hand([
            pk.Card('Q', 's'),
            pk.Card('Q', 'h'),
            pk.Card('Q', 'd'),
            pk.Card('8', 's'),
            pk.Card('8', 'd'),
        ])

        hand_2 = pk.Hand([
            pk.Card('Q', 'h'),
            pk.Card('Q', 'd'),
            pk.Card('Q', 'c'),
            pk.Card('8', 'h'),
            pk.Card('8', 'c'),
        ])

        self.assertEqual(hand_1, hand_2)
        self.assertGreaterEqual(hand_1, hand_2)
        

        # Same three of a kind, higher pair

        hand_1 = pk.Hand([
            pk.Card('Q', 's'),
            pk.Card('Q', 'h'),
            pk.Card('Q', 'd'),
            pk.Card('A', 's'),
            pk.Card('A', 'd'),
        ])

        hand_2 = pk.Hand([
            pk.Card('Q', 'h'),
            pk.Card('Q', 'd'),
            pk.Card('Q', 'c'),
            pk.Card('8', 'h'),
            pk.Card('8', 'c'),
        ])
        
        self.assertGreater(hand_1, hand_2)
        self.assertGreaterEqual(hand_1, hand_2)


        # Higher three of a kind, higher pair

        hand_1 = pk.Hand([
            pk.Card('Q', 's'),
            pk.Card('Q', 'h'),
            pk.Card('Q', 'd'),
            pk.Card('9', 's'),
            pk.Card('9', 'd'),
        ])

        hand_2 = pk.Hand([
            pk.Card('T', 'h'),
            pk.Card('T', 'd'),
            pk.Card('T', 'c'),
            pk.Card('3', 'h'),
            pk.Card('3', 'c'),
        ])
        
        self.assertGreater(hand_1, hand_2)
        self.assertGreaterEqual(hand_1, hand_2)


        # Higher three of a kind, lower pair

        hand_1 = pk.Hand([
            pk.Card('Q', 's'),
            pk.Card('Q', 'h'),
            pk.Card('Q', 'd'),
            pk.Card('3', 's'),
            pk.Card('3', 'd'),
        ])

        hand_2 = pk.Hand([
            pk.Card('T', 'h'),
            pk.Card('T', 'd'),
            pk.Card('T', 'c'),
            pk.Card('9', 'h'),
            pk.Card('9', 'c'),
        ])
        
        self.assertGreater(hand_1, hand_2)
        self.assertGreaterEqual(hand_1, hand_2)


    def test_flush_relations(self):


        """
        Runs test cases to check relations between flush hands work as expected.
        """


        # Exactly same hand

        hand_1 = pk.Hand([
            pk.Card('Q', 'h'),
            pk.Card('J', 'h'),
            pk.Card('7', 'h'),
            pk.Card('4', 'h'),
            pk.Card('2', 'h'),
        ])

        hand_2 = pk.Hand([
            pk.Card('Q', 'h'),
            pk.Card('J', 'h'),
            pk.Card('7', 'h'),
            pk.Card('4', 'h'),
            pk.Card('2', 'h'),
        ])
        
        self.assertEqual(hand_1, hand_2)
        self.assertGreaterEqual(hand_1, hand_2)


        # Same hand, different suits

        hand_1 = pk.Hand([
            pk.Card('Q', 'h'),
            pk.Card('J', 'h'),
            pk.Card('7', 'h'),
            pk.Card('4', 'h'),
            pk.Card('2', 'h'),
        ])

        hand_2 = pk.Hand([
            pk.Card('Q', 'c'),
            pk.Card('J', 'c'),
            pk.Card('7', 'c'),
            pk.Card('4', 'c'),
            pk.Card('2', 'c'),
        ])

        self.assertEqual(hand_1, hand_2)
        self.assertGreaterEqual(hand_1, hand_2)
        

        # Flush with all cards higher

        hand_1 = pk.Hand([
            pk.Card('A', 's'),
            pk.Card('K', 's'),
            pk.Card('Q', 's'),
            pk.Card('J', 's'),
            pk.Card('9', 's'),
        ])

        hand_2 = pk.Hand([
            pk.Card('8', 'd'),
            pk.Card('6', 'd'),
            pk.Card('5', 'd'),
            pk.Card('3', 'd'),
            pk.Card('2', 'd'),
        ])
  
        self.assertGreater(hand_1, hand_2)
        self.assertGreaterEqual(hand_1, hand_2)


        # Flush with higher main card, lower secondary cards

        hand_1 = pk.Hand([
            pk.Card('A', 'c'),
            pk.Card('6', 's'),
            pk.Card('5', 's'),
            pk.Card('3', 's'),
            pk.Card('2', 's'),
        ])

        hand_2 = pk.Hand([
            pk.Card('K', 's'),
            pk.Card('Q', 'c'),
            pk.Card('J', 'c'),
            pk.Card('9', 'c'),
            pk.Card('8', 'c'),
        ])
  
        self.assertGreater(hand_1, hand_2)
        self.assertGreaterEqual(hand_1, hand_2)


    def test_straight_relations(self):


        """
        Runs test cases to check relations between straight hands work as expected.
        """


        # Exactly same hand

        hand_1 = pk.Hand([
            pk.Card('7', 's'),
            pk.Card('6', 'h'),
            pk.Card('5', 'd'),
            pk.Card('4', 's'),
            pk.Card('3', 'd'),
        ])

        hand_2 = pk.Hand([
            pk.Card('7', 's'),
            pk.Card('6', 'h'),
            pk.Card('5', 'd'),
            pk.Card('4', 's'),
            pk.Card('3', 'd'),
        ])
        
        self.assertEqual(hand_1, hand_2)
        self.assertGreaterEqual(hand_1, hand_2)


        # Same hand, different suits

        hand_1 = pk.Hand([
            pk.Card('7', 's'),
            pk.Card('6', 'h'),
            pk.Card('5', 'd'),
            pk.Card('4', 's'),
            pk.Card('3', 'd'),
        ])

        hand_2 = pk.Hand([
            pk.Card('7', 's'),
            pk.Card('6', 's'),
            pk.Card('5', 'd'),
            pk.Card('4', 'c'),
            pk.Card('3', 'd'),
        ])

        self.assertEqual(hand_1, hand_2)
        self.assertGreaterEqual(hand_1, hand_2)
        

        # Higher straight

        hand_1 = pk.Hand([
            pk.Card('8', 'd'),
            pk.Card('7', 's'),
            pk.Card('6', 'h'),
            pk.Card('5', 'd'),
            pk.Card('4', 's'),
        ])

        hand_2 = pk.Hand([
            pk.Card('7', 's'),
            pk.Card('6', 'h'),
            pk.Card('5', 'd'),
            pk.Card('4', 's'),
            pk.Card('3', 'd'),
        ])
        
        self.assertGreater(hand_1, hand_2)
        self.assertGreaterEqual(hand_1, hand_2)


        # Straight higher than ace to five straight

        hand_1 = pk.Hand([
            pk.Card('6', 'd'),
            pk.Card('5', 's'),
            pk.Card('4', 'h'),
            pk.Card('3', 'd'),
            pk.Card('2', 's'),
        ])

        hand_2 = pk.Hand([
            pk.Card('5', 's'),
            pk.Card('4', 'h'),
            pk.Card('3', 'd'),
            pk.Card('2', 's'),
            pk.Card('A', 'd'),
        ])
        
        self.assertGreater(hand_1, hand_2)
        self.assertGreaterEqual(hand_1, hand_2)


    def test_three_of_a_kind_relations(self):


        """
        Runs test cases to check relations between three of a kind hands work as expected.
        """


        # Exactly same hand

        hand_1 = pk.Hand([
            pk.Card('Q', 's'),
            pk.Card('Q', 'h'),
            pk.Card('Q', 'd'),
            pk.Card('7', 's'),
            pk.Card('4', 'd'),
        ])

        hand_2 = pk.Hand([
            pk.Card('Q', 's'),
            pk.Card('Q', 'h'),
            pk.Card('Q', 'd'),
            pk.Card('7', 's'),
            pk.Card('4', 'd'),
        ])
        
        self.assertEqual(hand_1, hand_2)
        self.assertGreaterEqual(hand_1, hand_2)


        # Same hand, different suits

        hand_1 = pk.Hand([
            pk.Card('Q', 's'),
            pk.Card('Q', 'h'),
            pk.Card('Q', 'd'),
            pk.Card('7', 's'),
            pk.Card('4', 'd'),
        ])

        hand_2 = pk.Hand([
            pk.Card('Q', 'h'),
            pk.Card('Q', 'd'),
            pk.Card('Q', 'c'),
            pk.Card('7', 'h'),
            pk.Card('4', 'c'),
        ])

        self.assertEqual(hand_1, hand_2)
        self.assertGreaterEqual(hand_1, hand_2)
        

        # Same three of a kind, both kickers higher

        hand_1 = pk.Hand([
            pk.Card('Q', 's'),
            pk.Card('Q', 'h'),
            pk.Card('Q', 'd'),
            pk.Card('T', 's'),
            pk.Card('8', 'd'),
        ])

        hand_2 = pk.Hand([
            pk.Card('Q', 'h'),
            pk.Card('Q', 'd'),
            pk.Card('Q', 'c'),
            pk.Card('5', 'h'),
            pk.Card('2', 'c'),
        ])

        self.assertGreater(hand_1, hand_2)
        self.assertGreaterEqual(hand_1, hand_2)


        # Same three of a kind, main kicker higher, secondary kicker lower

        hand_1 = pk.Hand([
            pk.Card('Q', 's'),
            pk.Card('Q', 'h'),
            pk.Card('Q', 'd'),
            pk.Card('T', 's'),
            pk.Card('2', 'd'),
        ])

        hand_2 = pk.Hand([
            pk.Card('Q', 'h'),
            pk.Card('Q', 'd'),
            pk.Card('Q', 'c'),
            pk.Card('9', 'h'),
            pk.Card('5', 'c'),
        ])

        self.assertGreater(hand_1, hand_2)
        self.assertGreaterEqual(hand_1, hand_2)


        # Higher three of a kind, both kickers higher

        hand_1 = pk.Hand([
            pk.Card('K', 's'),
            pk.Card('K', 'h'),
            pk.Card('K', 'd'),
            pk.Card('T', 's'),
            pk.Card('8', 'd'),
        ])

        hand_2 = pk.Hand([
            pk.Card('Q', 'h'),
            pk.Card('Q', 'd'),
            pk.Card('Q', 'c'),
            pk.Card('5', 'h'),
            pk.Card('2', 'c'),
        ])

        self.assertGreater(hand_1, hand_2)
        self.assertGreaterEqual(hand_1, hand_2)


        # Same three of a kind, both kickers lower

        hand_1 = pk.Hand([
            pk.Card('K', 's'),
            pk.Card('K', 'h'),
            pk.Card('K', 'd'),
            pk.Card('T', 's'),
            pk.Card('2', 'd'),
        ])

        hand_2 = pk.Hand([
            pk.Card('Q', 'h'),
            pk.Card('Q', 'd'),
            pk.Card('Q', 'c'),
            pk.Card('9', 'h'),
            pk.Card('5', 'c'),
        ])

        self.assertGreater(hand_1, hand_2)
        self.assertGreaterEqual(hand_1, hand_2)


    def test_two_pair_relations(self):


        """
        Runs test cases to check relations between two pair hands work as expected.
        """


        # Exactly same hand

        hand_1 = pk.Hand([
            pk.Card('A', 's'),
            pk.Card('A', 'h'),
            pk.Card('6', 'd'),
            pk.Card('6', 's'),
            pk.Card('T', 'd'),
        ])

        hand_2 = pk.Hand([
            pk.Card('A', 's'),
            pk.Card('A', 'h'),
            pk.Card('6', 'd'),
            pk.Card('6', 's'),
            pk.Card('T', 'd'),
        ])
        
        self.assertEqual(hand_1, hand_2)
        self.assertGreaterEqual(hand_1, hand_2)


        # Same hand, different suits

        hand_1 = pk.Hand([
            pk.Card('A', 's'),
            pk.Card('A', 'h'),
            pk.Card('6', 'd'),
            pk.Card('6', 's'),
            pk.Card('T', 'd'),
        ])

        hand_2 = pk.Hand([
            pk.Card('A', 's'),
            pk.Card('A', 'h'),
            pk.Card('6', 'h'),
            pk.Card('6', 'c'),
            pk.Card('T', 'd'),
        ])

        self.assertEqual(hand_1, hand_2)
        self.assertGreaterEqual(hand_1, hand_2)
        

        # Same pairs, higher kicker

        hand_1 = pk.Hand([
            pk.Card('A', 's'),
            pk.Card('A', 'h'),
            pk.Card('6', 'c'),
            pk.Card('6', 'h'),
            pk.Card('T', 'd'),
        ])

        hand_2 = pk.Hand([
            pk.Card('A', 's'),
            pk.Card('A', 'c'),
            pk.Card('6', 'h'),
            pk.Card('6', 'd'),
            pk.Card('9', 'h'),
        ])

        self.assertGreater(hand_1, hand_2)
        self.assertGreaterEqual(hand_1, hand_2)


        # Same main pair, higher secondary pair and kicker

        hand_1 = pk.Hand([
            pk.Card('A', 's'),
            pk.Card('A', 'h'),
            pk.Card('K', 'c'),
            pk.Card('K', 'h'),
            pk.Card('T', 'd'),
        ])

        hand_2 = pk.Hand([
            pk.Card('A', 's'),
            pk.Card('A', 'c'),
            pk.Card('6', 'h'),
            pk.Card('6', 'd'),
            pk.Card('9', 'h'),
        ])

        self.assertGreater(hand_1, hand_2)
        self.assertGreaterEqual(hand_1, hand_2)


        # Same main pair, higher secondary pair, lower kicker

        hand_1 = pk.Hand([
            pk.Card('A', 's'),
            pk.Card('A', 'h'),
            pk.Card('K', 'c'),
            pk.Card('K', 'h'),
            pk.Card('T', 'd'),
        ])

        hand_2 = pk.Hand([
            pk.Card('A', 's'),
            pk.Card('A', 'c'),
            pk.Card('6', 'h'),
            pk.Card('6', 'd'),
            pk.Card('K', 'h'),
        ])

        self.assertGreater(hand_1, hand_2)
        self.assertGreaterEqual(hand_1, hand_2)


        # Higher main pair, secondary pair and kicker

        hand_1 = pk.Hand([
            pk.Card('A', 's'),
            pk.Card('A', 'h'),
            pk.Card('8', 'c'),
            pk.Card('8', 'h'),
            pk.Card('K', 'd'),
        ])

        hand_2 = pk.Hand([
            pk.Card('Q', 's'),
            pk.Card('Q', 'c'),
            pk.Card('6', 'h'),
            pk.Card('6', 'd'),
            pk.Card('J', 'h'),
        ])

        self.assertGreater(hand_1, hand_2)
        self.assertGreaterEqual(hand_1, hand_2)


        # Higher main pair, lower secondary pair and kicker

        hand_1 = pk.Hand([
            pk.Card('A', 's'),
            pk.Card('A', 'h'),
            pk.Card('2', 'c'),
            pk.Card('2', 'h'),
            pk.Card('3', 'd'),
        ])

        hand_2 = pk.Hand([
            pk.Card('Q', 's'),
            pk.Card('Q', 'c'),
            pk.Card('6', 'h'),
            pk.Card('6', 'd'),
            pk.Card('J', 'h'),
        ])

        self.assertGreater(hand_1, hand_2)
        self.assertGreaterEqual(hand_1, hand_2)


    def test_pair_relations(self):


        """
        Runs test cases to check relations between pair hands work as expected.
        """


        # Exactly same hand

        hand_1 = pk.Hand([
            pk.Card('3', 's'),
            pk.Card('3', 'h'),
            pk.Card('6', 'd'),
            pk.Card('4', 's'),
            pk.Card('2', 'd'),
        ])

        hand_2 = pk.Hand([
            pk.Card('3', 's'),
            pk.Card('3', 'h'),
            pk.Card('6', 'd'),
            pk.Card('4', 's'),
            pk.Card('2', 'd'),
        ])
        
        self.assertEqual(hand_1, hand_2)
        self.assertGreaterEqual(hand_1, hand_2)


        # Same hand, different suits

        hand_1 = pk.Hand([
            pk.Card('3', 's'),
            pk.Card('3', 'h'),
            pk.Card('6', 'd'),
            pk.Card('4', 's'),
            pk.Card('2', 'd'),
        ])

        hand_2 = pk.Hand([
            pk.Card('3', 'h'),
            pk.Card('3', 'd'),
            pk.Card('6', 's'),
            pk.Card('4', 'c'),
            pk.Card('2', 'd'),
        ])

        self.assertEqual(hand_1, hand_2)
        self.assertGreaterEqual(hand_1, hand_2)
        

        # Same pairs, higher kickers

        hand_1 = pk.Hand([
            pk.Card('A', 's'),
            pk.Card('A', 'h'),
            pk.Card('K', 'c'),
            pk.Card('T', 'h'),
            pk.Card('9', 'd'),
        ])

        hand_2 = pk.Hand([
            pk.Card('A', 's'),
            pk.Card('A', 'c'),
            pk.Card('6', 'h'),
            pk.Card('4', 'd'),
            pk.Card('2', 'h'),
        ])

        self.assertGreater(hand_1, hand_2)
        self.assertGreaterEqual(hand_1, hand_2)


        # Same pairs, higher main kicker, lower secondary kickers

        hand_1 = pk.Hand([
            pk.Card('A', 's'),
            pk.Card('A', 'h'),
            pk.Card('K', 'c'),
            pk.Card('3', 'h'),
            pk.Card('2', 'd'),
        ])

        hand_2 = pk.Hand([
            pk.Card('A', 's'),
            pk.Card('A', 'c'),
            pk.Card('Q', 'h'),
            pk.Card('J', 'd'),
            pk.Card('T', 'h'),
        ])

        self.assertGreater(hand_1, hand_2)
        self.assertGreaterEqual(hand_1, hand_2)


        # Higher pair, higher kickers

        hand_1 = pk.Hand([
            pk.Card('A', 's'),
            pk.Card('A', 'h'),
            pk.Card('K', 'c'),
            pk.Card('J', 'h'),
            pk.Card('8', 'd'),
        ])

        hand_2 = pk.Hand([
            pk.Card('K', 's'),
            pk.Card('K', 'c'),
            pk.Card('5', 'h'),
            pk.Card('3', 'd'),
            pk.Card('2', 'h'),
        ])

        self.assertGreater(hand_1, hand_2)
        self.assertGreaterEqual(hand_1, hand_2)


        # Higher pair, lower kickers

        hand_1 = pk.Hand([
            pk.Card('A', 's'),
            pk.Card('A', 'h'),
            pk.Card('4', 'c'),
            pk.Card('3', 'h'),
            pk.Card('2', 'd'),
        ])

        hand_2 = pk.Hand([
            pk.Card('K', 's'),
            pk.Card('K', 'c'),
            pk.Card('Q', 'h'),
            pk.Card('J', 'd'),
            pk.Card('T', 'h'),
        ])

        self.assertGreater(hand_1, hand_2)
        self.assertGreaterEqual(hand_1, hand_2)


    def test_high_card_relations(self):


        """
        Runs test cases to check relations between high card hands work as expected.
        """


        # Exactly same hand

        hand_1 = pk.Hand([
            pk.Card('T', 's'),
            pk.Card('8', 'h'),
            pk.Card('5', 'd'),
            pk.Card('3', 's'),
            pk.Card('2', 'd'),
        ])

        hand_2 = pk.Hand([
            pk.Card('T', 's'),
            pk.Card('8', 'h'),
            pk.Card('5', 'd'),
            pk.Card('3', 's'),
            pk.Card('2', 'd'),
        ])
        
        self.assertEqual(hand_1, hand_2)
        self.assertGreaterEqual(hand_1, hand_2)


        # Same hand, different suits

        hand_1 = pk.Hand([
            pk.Card('T', 's'),
            pk.Card('8', 'h'),
            pk.Card('5', 'd'),
            pk.Card('3', 's'),
            pk.Card('2', 'd'),
        ])

        hand_2 = pk.Hand([
            pk.Card('T', 'h'),
            pk.Card('8', 'd'),
            pk.Card('5', 's'),
            pk.Card('3', 'c'),
            pk.Card('2', 'd'),
        ])

        self.assertEqual(hand_1, hand_2)
        self.assertGreaterEqual(hand_1, hand_2)
        

        # All cards higher

        hand_1 = pk.Hand([
            pk.Card('A', 'h'),
            pk.Card('K', 'd'),
            pk.Card('J', 's'),
            pk.Card('T', 'c'),
            pk.Card('8', 'd'),
        ])

        hand_2 = pk.Hand([
            pk.Card('7', 'h'),
            pk.Card('6', 'd'),
            pk.Card('5', 's'),
            pk.Card('3', 'c'),
            pk.Card('2', 'd'),
        ])


        # Main card higher, all kickers lower

        hand_1 = pk.Hand([
            pk.Card('A', 'h'),
            pk.Card('6', 'd'),
            pk.Card('5', 's'),
            pk.Card('3', 'c'),
            pk.Card('2', 'd'),
        ])

        hand_2 = pk.Hand([
            pk.Card('7', 'h'),
            pk.Card('K', 'd'),
            pk.Card('J', 's'),
            pk.Card('T', 'c'),
            pk.Card('8', 'd'),
        ])


        self.assertGreater(hand_1, hand_2)
        self.assertGreaterEqual(hand_1, hand_2)


    def test_different_category_relations(self):
        

        """
        Runs test cases to check relations between different categories.
        """

        
        # Resources

        royal_flush_hand = pk.Hand([
            pk.Card('A', 's'),
            pk.Card('K', 's'),
            pk.Card('Q', 's'),
            pk.Card('J', 's'),
            pk.Card('T', 's'),
        ])

        straight_flush_hand = pk.Hand([
            pk.Card('5', 's'),
            pk.Card('4', 's'),
            pk.Card('3', 's'),
            pk.Card('2', 's'),
            pk.Card('A', 's'),
        ])

        four_of_a_kind_hand = pk.Hand([
            pk.Card('6', 's'),
            pk.Card('6', 'h'),
            pk.Card('6', 'd'),
            pk.Card('6', 'c'),
            pk.Card('7', 's'),
        ])

        full_house_hand = pk.Hand([
            pk.Card('8', 's'),
            pk.Card('8', 'h'),
            pk.Card('8', 'd'),
            pk.Card('9', 's'),
            pk.Card('9', 'd'),
        ])

        flush_hand = pk.Hand([
            pk.Card('9', 'h'),
            pk.Card('8', 'h'),
            pk.Card('7', 'h'),
            pk.Card('6', 'h'),
            pk.Card('4', 'h'),
        ])

        straight_hand = pk.Hand([
            pk.Card('T', 's'),
            pk.Card('9', 'h'),
            pk.Card('8', 'd'),
            pk.Card('7', 's'),
            pk.Card('6', 'd'),
        ])

        three_of_a_kind_hand = pk.Hand([
            pk.Card('J', 's'),
            pk.Card('J', 'h'),
            pk.Card('J', 'd'),
            pk.Card('9', 's'),
            pk.Card('8', 'd'),
        ])

        two_pair_hand = pk.Hand([
            pk.Card('Q', 's'),
            pk.Card('Q', 'h'),
            pk.Card('J', 'd'),
            pk.Card('J', 's'),
            pk.Card('T', 'd'),
        ])

        pair_hand = pk.Hand([
            pk.Card('K', 's'),
            pk.Card('K', 'h'),
            pk.Card('Q', 's'),
            pk.Card('J', 's'),
            pk.Card('T', 's'),
        ])

        high_card_hand = pk.Hand([
            pk.Card('A', 's'),
            pk.Card('K', 's'),
            pk.Card('Q', 's'),
            pk.Card('J', 's'),
            pk.Card('9', 'h'),
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