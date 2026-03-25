"""
Defines unit tests on Table class.
"""


import sys
sys.path.insert(0, '.')


from unittest import main, TestCase


from pokerpy import constants, messages, structures


class TestTableClass(TestCase):


    """
    Runs unit tests on Table class.
    """


    def test_instantiation(self):


        """
        Runs test cases on class instantiation.
        """


        # Valid inputs

        structures.Table([
            structures.Player('Andy', stack=10),
            structures.Player('Boa', stack=10),
            structures.Player('Coral', stack=10),
        ])


        # Invalid inputs

        with self.assertRaises(TypeError) as cm:
            structures.Table('Wood')
        self.assertEqual(cm.exception.args[0], messages.msg_not_list.format(str.__name__))
        
        with self.assertRaises(TypeError) as cm:
            structures.Table([structures.Player('Andy', stack=10), 'Boa'])
        self.assertEqual(cm.exception.args[0], messages.msg_not_all_player_instances)


    def test_remove_card_from_deck_method(self):


        """
        Runs test cases on remove_card_from_deck method.
        """


        table = structures.Table([
            structures.Player('Andy', stack=10),
            structures.Player('Boa', stack=10),
            structures.Player('Coral', stack=10),
        ])


        # Before and after effects

        self.assertSetEqual(
            set(table.deck),
            {structures.Card(value, suit) for value, suit in constants.full_sorted_values_and_suits}
        )

        table.remove_card_from_deck(structures.Card('7', 'c'))
        table.remove_card_from_deck(structures.Card('T', 'd'))
        table.remove_card_from_deck(structures.Card('2', 's'))

        self.assertEqual(
            set(table.deck),
            {
                structures.Card(value, suit) for value, suit in constants.full_sorted_values_and_suits
                if (value, suit) not in (('7', 'c'), ('T', 'd'), ('2', 's'))
            }
        )


        # Invalid inputs

        with self.assertRaises(TypeError) as cm:
            table.remove_card_from_deck('7c')
        self.assertEqual(cm.exception.args[0], messages.msg_not_card_instance.format(str.__name__))

        with self.assertRaises(ValueError) as cm:
            table.remove_card_from_deck(structures.Card('7', 'c'))
        self.assertEqual(cm.exception.args[0], messages.msg_card_not_in_deck)


    def test_deal_common_card_method(self):


        """
        Runs test cases on deal_common_card method.
        """


        table = structures.Table([
            structures.Player('Andy', stack=10),
            structures.Player('Boa', stack=10),
            structures.Player('Coral', stack=10),
        ])


        # Before and after effects

        self.assertSetEqual(set(table.common_cards), set())

        table.deal_common_card(structures.Card('7', 'c'))
        table.deal_common_card(structures.Card('T', 'd'))
        table.deal_common_card(structures.Card('2', 's'))

        self.assertEqual(
            set(table.common_cards), {structures.Card('7', 'c'), structures.Card('T', 'd'), structures.Card('2', 's')}
        )


        # Invalid inputs

        with self.assertRaises(TypeError) as cm:
            table.deal_common_card('7c')
        self.assertEqual(cm.exception.args[0], messages.msg_not_card_instance.format(str.__name__))

        with self.assertRaises(ValueError) as cm:
            table.deal_common_card(structures.Card('7', 'c'))
        self.assertEqual(cm.exception.args[0], messages.msg_repeated_cards)


    def test_add_to_current_amount_method(self):


        """
        Runs test cases on add_to_current_amount method.
        """


        table = structures.Table([
            structures.Player('Andy', stack=10),
            structures.Player('Boa', stack=10),
            structures.Player('Coral', stack=10),
        ])


        # Before and after effects

        self.assertEqual(table.current_amount, 0)

        table.add_to_current_amount(0)
        table.add_to_current_amount(50)
        table.add_to_current_amount(100)

        self.assertEqual(table.current_amount, 150)


        # Invalid inputs

        with self.assertRaises(TypeError) as cm:
            table.add_to_current_amount('100')
        self.assertEqual(cm.exception.args[0], messages.msg_not_int.format(str.__name__))

        with self.assertRaises(ValueError) as cm:
            table.add_to_current_amount(-100)
        self.assertEqual(cm.exception.args[0], messages.msg_not_positive_or_zero_value.format(-100))


    def test_add_to_central_pot_method(self):


        """
        Runs test cases on add_to_central_pot method.
        """


        table = structures.Table([
            structures.Player('Andy', stack=10),
            structures.Player('Boa', stack=10),
            structures.Player('Coral', stack=10),
        ])


        # Before and after effects

        self.assertEqual(table.central_pot, 0)

        table.add_to_central_pot(0)
        table.add_to_central_pot(50)
        table.add_to_central_pot(100)

        self.assertEqual(table.central_pot, 150)


        # Invalid inputs

        with self.assertRaises(TypeError) as cm:
            table.add_to_central_pot('100')
        self.assertEqual(cm.exception.args[0], messages.msg_not_int.format(str.__name__))

        with self.assertRaises(ValueError) as cm:
            table.add_to_central_pot(-100)
        self.assertEqual(cm.exception.args[0], messages.msg_not_positive_or_zero_value.format(-100))


    def test_reset_betting_round_states_method(self):


        """
        Runs test cases on reset_betting_round_states method.
        """


        table = structures.Table([
            Andy := structures.Player('Andy', stack=10),
            structures.Player('Boa', stack=10),
            structures.Player('Coral', stack=10),
        ])

        # Set previous states
        Andy.request_action(structures.Action(constants.ACTION_BET, 200))
        Andy.add_to_current_amount(200)
        table.add_to_current_amount(200)

        table.reset_betting_round_states()

        # Evaluate after states
        self.assertIsNone(Andy.requested_action)
        self.assertEqual(Andy.current_amount, 0)
        self.assertEqual(table.current_amount, 0)
    

    def test_reset_cycle_states_method(self):


        """
        Runs test cases on reset_cycle_states method.
        """


        table = structures.Table([
            Andy := structures.Player('Andy', stack=10),
            structures.Player('Boa', stack=10),
            structures.Player('Coral', stack=10),
        ])

        # Set previous states
        Andy.request_action(structures.Action(constants.ACTION_BET, 200))
        Andy.add_to_current_amount(200)
        Andy.deal_card(structures.Card('J', 'd'))
        Andy.assign_hand(structures.Hand([
            structures.Card('7', 's'),
            structures.Card('7', 'd'),
            structures.Card('7', 'c'),
            structures.Card('2', 's'),
            structures.Card('2', 'c'),
        ]))
        table.add_to_current_amount(200)
        table.remove_card_from_deck(structures.Card('7', 'c'))
        table.deal_common_card(structures.Card('7', 'c'))
        table.add_to_central_pot(200)

        table.reset_cycle_states()

        # Evaluate after states
        self.assertIsNone(Andy.requested_action)
        self.assertEqual(Andy.current_amount, 0)
        self.assertTupleEqual(Andy.cards, ())
        self.assertIsNone(Andy.hand)
        self.assertEqual(table.current_amount, 0)
        self.assertEqual(table.central_pot, 0)
        self.assertSetEqual(set(table.common_cards), set())
        self.assertSetEqual(
            set(table.deck),
            {structures.Card(value, suit) for value, suit in constants.full_sorted_values_and_suits},
        )


if __name__ == '__main__':
    main()