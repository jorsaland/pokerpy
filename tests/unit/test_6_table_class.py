"""
Defines unit tests on Table class.
"""


import sys
sys.path.insert(0, '.')


from unittest import main, TestCase


from pokerpy import messages, structures


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

        table = structures.Table(players, fold_to_nothing=False)
        self.assertFalse(table.fold_to_nothing)

        table = structures.Table(players, fold_to_nothing=True)
        self.assertTrue(table.fold_to_nothing)
        
        table = structures.Table(players)
        self.assertFalse(table.fold_to_nothing)


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
        table.fold_player(Boa)
        table.fold_player(Coral)


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
        table.set_last_aggressive_player(Boa)


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


        # Invalid types

        with self.assertRaises(TypeError) as cm:
            table.deal_to_players('Andy')
        self.assertEqual(cm.exception.args[0], messages.table_not_int_cards_count_message.format(str.__name__))


    def test_deal_to_players_method(self):


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

        table.deal_common_cards(3)


        # Invalid types

        with self.assertRaises(TypeError) as cm:
            table.deal_common_cards('Andy')
        self.assertEqual(cm.exception.args[0], messages.table_not_int_cards_count_message.format(str.__name__))


if __name__ == '__main__':
    main()