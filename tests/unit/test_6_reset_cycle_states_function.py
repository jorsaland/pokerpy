"""
Defines unit unit tests on reset_cycle_states function.
"""


import sys
sys.path.insert(0, '.')


from unittest import main, TestCase


from pokerpy import constants, managers, messages, structures


class TestResetCycleStatesFunction(TestCase):


    """
    Runs unit tests on reset_cycle_states function.
    """


    def test_invalid_input(self):


        """
        Runs test cases on reset_cycle_states function with an invalid input.
        """


        with self.assertRaises(TypeError) as context:
            managers.reset_cycle_states('Wood')
        self.assertEqual(context.exception.args[0], messages.msg_not_table_instance.format(str.__name__))

    
    def test_reset_cycle_states_function(self):


        """
        Runs test cases on reset_cycle_states function effects.
        """


        table = structures.Table([
            Andy := structures.Player('Andy', 10),
            structures.Player('Boa', 10),
            structures.Player('Coral', 10),
        ])

        action = structures.Action(constants.ACTION_BET, 200)
        player_cards = [
            structures.Card('7', 's'),
            structures.Card('7', 'd'),
        ]
        hand = structures.Hand([
            structures.Card('7', 's'),
            structures.Card('7', 'd'),
            structures.Card('7', 'c'),
            structures.Card('2', 's'),
            structures.Card('2', 'c'),
        ])
        deck = [structures.Card(value, suit) for value, suit in constants.full_sorted_values_and_suits]
        common_cards = [
            structures.Card('7', 'c'),
            structures.Card('2', 's'),
            structures.Card('2', 'c'),            
        ]

        # Set previous states

        Andy.request_action(action)
        Andy.add_to_current_amount(200)
        for card in player_cards:
            table.remove_card_from_deck(card)
            Andy.assign_card(card)
        Andy.assign_hand(hand)
        Andy.set_as_folded()

        for card in common_cards:
            table.remove_card_from_deck(card)
            table.assign_common_card(card)
        table.add_to_current_amount(200)
        table.add_to_central_pot(500)

        # Evaluate before states

        self.assertEqual(Andy.requested_action, action)
        self.assertEqual(Andy.current_amount, 200)
        self.assertTupleEqual(Andy.cards, tuple(player_cards))
        self.assertEqual(Andy.hand, hand)
        self.assertTrue(Andy.is_folded)

        self.assertTupleEqual(table.players_in_hand, tuple(player for player in table.players if player != Andy))
        self.assertEqual(table.current_amount, 200)
        self.assertEqual(table.central_pot, 500)
        self.assertTupleEqual(table.common_cards, tuple(common_cards))
        self.assertSetEqual(set(table.deck), set(card for card in deck if card not in (*player_cards, *common_cards)))

        # Reset states

        managers.reset_cycle_states(table)

        # Evaluate after states

        self.assertIsNone(Andy.requested_action)
        self.assertEqual(Andy.current_amount, 0)
        self.assertTupleEqual(Andy.cards, ())
        self.assertIsNone(Andy.hand)
        self.assertFalse(Andy.is_folded)

        self.assertTupleEqual(table.players_in_hand, table.players)
        self.assertEqual(table.current_amount, 0)
        self.assertEqual(table.central_pot, 0)
        self.assertTupleEqual(table.common_cards, ())
        self.assertSetEqual(set(table.deck), set(deck))


if __name__ == '__main__':
    main()