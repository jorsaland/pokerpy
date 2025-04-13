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


        # Valid input

        structures.Table([structures.Player('Andy'), structures.Player('Boa')])


        # Invalid types

        with self.assertRaises(TypeError) as cm:
            structures.Table('Wood')
        self.assertEqual(cm.exception.args[0], messages.table_not_list_players_message.format(str.__name__))
        
        with self.assertRaises(TypeError) as cm:
            structures.Table([structures.Player('Andy'), 'Boa'])
        self.assertEqual(cm.exception.args[0], messages.table_not_all_player_instances_message)

        
        # Fold to nothing

        players = [structures.Player('Andy'), structures.Player('Boa')]

        table = structures.Table(players, open_fold_allowed=False)
        self.assertFalse(table.open_fold_allowed)

        table = structures.Table(players, open_fold_allowed=True)
        self.assertTrue(table.open_fold_allowed)
        
        table = structures.Table(players)
        self.assertFalse(table.open_fold_allowed)


    def test_activate_player_method(self):


        """
        Runs test cases on activate_player method.
        """


        all_players = [
            Andy := structures.Player('Andy'),
            Boa := structures.Player('Boa'),
            Coral := structures.Player('Coral'),
        ]
        table = structures.Table(all_players)


        # Valid inputs

        table.activate_player(Andy)
        table.activate_player(Boa)
        table.activate_player(Coral)


        # Invalid types

        with self.assertRaises(TypeError) as cm:
            table.activate_player('Dino')
        self.assertEqual(cm.exception.args[0], messages.table_not_player_instance_message.format(str.__name__))


        # Invalid values

        with self.assertRaises(ValueError) as cm:
            table.activate_player(structures.Player('Dino'))
        self.assertEqual(cm.exception.args[0], messages.table_player_not_in_table_message.format('Dino'))


    def test_add_to_current_amount(self):


        """
        Runs test cases on add_to_current_amount method.
        """


        all_players = [
            structures.Player('Andy'),
            structures.Player('Boa'),
            structures.Player('Coral'),
        ]
        table = structures.Table(all_players, smallest_chip=10)


        # Valid inputs

        table.add_to_current_amount(0)
        table.add_to_current_amount(50)
        table.add_to_current_amount(100)

        self.assertEqual(table.current_amount, 150)


        # Invalid types

        with self.assertRaises(TypeError) as cm:
            table.add_to_current_amount('100')
        self.assertEqual(cm.exception.args[0], messages.table_not_int_current_amount_message.format(str.__name__))


        # Negative amount

        with self.assertRaises(ValueError) as cm:
            table.add_to_current_amount(-100)
        self.assertEqual(cm.exception.args[0], messages.table_negative_increase_message.format(-100))


        # Not multiple of smallest chip

        with self.assertRaises(ValueError) as cm:
            table.add_to_current_amount(5)
        self.assertEqual(cm.exception.args[0], messages.table_not_smallest_chip_multiple_increase_message.format(10, 5))

        with self.assertRaises(ValueError) as cm:
            table.add_to_current_amount(107)
        self.assertEqual(cm.exception.args[0], messages.table_not_smallest_chip_multiple_increase_message.format(10, 107))


    def test_add_to_central_pot(self):


        """
        Runs test cases on add_to_central_pot method.
        """


        all_players = [
            structures.Player('Andy'),
            structures.Player('Boa'),
            structures.Player('Coral'),
        ]
        table = structures.Table(all_players, smallest_chip=10)


        # Valid inputs

        table.add_to_central_pot(0)
        table.add_to_central_pot(50)
        table.add_to_central_pot(100)

        self.assertEqual(table.central_pot, 150)


        # Invalid types

        with self.assertRaises(TypeError) as cm:
            table.add_to_central_pot('100')
        self.assertEqual(cm.exception.args[0], messages.table_not_int_central_pot_message.format(str.__name__))


        # Negative amount

        with self.assertRaises(ValueError) as cm:
            table.add_to_central_pot(-100)
        self.assertEqual(cm.exception.args[0], messages.table_negative_increase_message.format(-100))


        # Not multiple of smallest chip

        with self.assertRaises(ValueError) as cm:
            table.add_to_central_pot(5)
        self.assertEqual(cm.exception.args[0], messages.table_not_smallest_chip_multiple_increase_message.format(10, 5))

        with self.assertRaises(ValueError) as cm:
            table.add_to_central_pot(107)
        self.assertEqual(cm.exception.args[0], messages.table_not_smallest_chip_multiple_increase_message.format(10, 107))


    def test_fold_player_method(self):


        """
        Runs test cases on activate_player method.
        """


        all_players = [
            Andy := structures.Player('Andy'),
            Boa := structures.Player('Boa'),
            Coral := structures.Player('Coral'),
        ]
        table = structures.Table(all_players)
        table.reset_cycle_states()


        # Valid inputs

        table.fold_player(Andy)
        self.assertTupleEqual(table.active_players, (Boa, Coral))

        table.fold_player(Boa)
        self.assertTupleEqual(table.active_players, (Coral,))

        table.fold_player(Coral)
        self.assertTupleEqual(table.active_players, ())


        # Invalid types

        with self.assertRaises(TypeError) as cm:
            table.activate_player('Dino')
        self.assertEqual(cm.exception.args[0], messages.table_not_player_instance_message.format(str.__name__))


        # Invalid values
        
        with self.assertRaises(ValueError) as cm:
            table.activate_player(structures.Player('Dino'))
        self.assertEqual(cm.exception.args[0], messages.table_player_not_in_table_message.format('Dino'))

        with self.assertRaises(ValueError) as cm:
            table.fold_player(Andy)
        self.assertEqual(cm.exception.args[0], messages.table_player_already_folded_message.format(Andy.name))


    def test_set_last_aggressive_player_method(self):


        """
        Runs test cases on set_last_aggressive_player method.
        """


        all_players = [
            Andy := structures.Player('Andy'),
            Boa := structures.Player('Boa'),
            Coral := structures.Player('Coral'),
        ]
        table = structures.Table(all_players)
        table.activate_player(Andy)
        table.activate_player(Boa)


        # Valid inputs

        table.set_last_aggressive_player(Andy)
        self.assertEqual(table.last_aggressive_player, Andy)

        table.set_last_aggressive_player(Boa)
        self.assertEqual(table.last_aggressive_player, Boa)


        # Invalid types

        with self.assertRaises(TypeError) as cm:
            table.set_last_aggressive_player('Dino')
        self.assertEqual(cm.exception.args[0], messages.table_not_player_instance_message.format(str.__name__))


        # Invalid values
        
        with self.assertRaises(ValueError) as cm:
            table.set_last_aggressive_player(structures.Player('Dino'))
        self.assertEqual(cm.exception.args[0], messages.table_player_not_in_table_message.format('Dino'))

        with self.assertRaises(ValueError) as cm:
            table.set_last_aggressive_player(Coral)
        self.assertEqual(cm.exception.args[0], messages.table_player_already_folded_message.format(Coral.name))


    def test_deal_to_players_method(self):


        """
        Runs test cases on deal_to_players method.
        """


        all_players = [
            structures.Player('Andy'),
            structures.Player('Boa'),
            structures.Player('Coral'),
        ]
        table = structures.Table(all_players)


        # Valid inputs

        table.deal_to_players(3)

        self.assertSetEqual(
            set(table.deck).union(*[player.cards for player in table.players]),
            set(structures.Card(value, suit) for value, suit in constants.full_sorted_values_and_suits)
        )

        # Invalid types

        with self.assertRaises(TypeError) as cm:
            table.deal_to_players('Andy')
        self.assertEqual(cm.exception.args[0], messages.table_not_int_cards_count_message.format(str.__name__))


    def test_deal_common_cards(self):


        """
        Runs test cases on deal_common_cards method.
        """


        all_players = [
            structures.Player('Andy'),
            structures.Player('Boa'),
            structures.Player('Coral'),
        ]
        table = structures.Table(all_players)


        # Valid inputs

        table.deal_common_cards(10)

        self.assertSetEqual(
            set(table.deck).union(table.common_cards),
            set(structures.Card(value, suit) for value, suit in constants.full_sorted_values_and_suits)
        )


        # Invalid types

        with self.assertRaises(TypeError) as cm:
            table.deal_common_cards('AKQJT')
        self.assertEqual(cm.exception.args[0], messages.table_not_int_cards_count_message.format(str.__name__))


    def test_reset_betting_round_states_method(self):


        """
        Runs test cases on reset_betting_round_states method.
        """


        all_players = [
            Andy := structures.Player('Andy'),
            structures.Player('Boa'),
            structures.Player('Coral'),
        ]
        table = structures.Table(all_players)

        table.add_to_current_amount(200)
        table.activate_player(Andy)
        table.set_last_aggressive_player(Andy)

        table.reset_betting_round_states()

        self.assertEqual(table.current_amount, 0)
        self.assertIsNone(table.last_aggressive_player)
    

    def test_reset_cycle_states_method(self):


        """
        Runs test cases on reset_cycle_states method.
        """


        all_players = [
            Andy := structures.Player('Andy'),
            structures.Player('Boa'),
            structures.Player('Coral'),
        ]
        table = structures.Table(all_players)

        table.add_to_current_amount(200)
        table.deal_common_cards(5)
        table.activate_player(Andy)
        table.set_last_aggressive_player(Andy)
        table.deal_common_cards(5)
        table.deal_to_players(2)
        table.add_to_central_pot(300)

        table.reset_cycle_states()

        self.assertEqual(table.current_amount, 0)
        self.assertIsNone(table.last_aggressive_player)
        self.assertTupleEqual(table.active_players, tuple(all_players))
        self.assertTupleEqual(table.deck, tuple(structures.Card(value, suit) for value, suit in constants.full_sorted_values_and_suits))
        self.assertEqual(table.central_pot, 0)


if __name__ == '__main__':
    main()