"""
Defines unit tests on Table class.
"""


import sys
sys.path.insert(0, '.')


from unittest import main, TestCase


import pokerpy as pk


class TestTableClass(TestCase):


    """
    Runs unit tests on Table class.
    """


    def test_instantiation(self):


        """
        Runs test cases on class instantiation.
        """


        # Valid input

        pk.Table([pk.Player('Andy'), pk.Player('Boa')])


        # Invalid types

        with self.assertRaises(TypeError) as cm:
            pk.Table('Wood')
        self.assertEqual(cm.exception.args[0], pk.messages.table_not_list_players_message.format(str.__name__))
        
        with self.assertRaises(TypeError) as cm:
            pk.Table([pk.Player('Andy'), 'Boa'])
        self.assertEqual(cm.exception.args[0], pk.messages.table_not_all_player_instances_message)


    def test_activate_player_method(self):


        """
        Runs test cases on activate_player method.
        """


        all_players = [
            Andy := pk.Player('Andy'),
            Boa := pk.Player('Boa'),
            Coral := pk.Player('Coral'),
        ]
        table = pk.Table(all_players)


        # Valid inputs

        table.activate_player(Andy)
        table.activate_player(Boa)
        table.activate_player(Coral)


        # Invalid types

        with self.assertRaises(TypeError) as cm:
            table.activate_player('Dino')
        self.assertEqual(cm.exception.args[0], pk.messages.table_not_player_instance_message.format(str.__name__))


        # Invalid values

        with self.assertRaises(ValueError) as cm:
            table.activate_player(pk.Player('Dino'))
        self.assertEqual(cm.exception.args[0], pk.messages.table_player_not_in_table_message.format('Dino'))


    def test_fold_player_method(self):


        """
        Runs test cases on activate_player method.
        """


        all_players = [
            Andy := pk.Player('Andy'),
            Boa := pk.Player('Boa'),
            Coral := pk.Player('Coral'),
        ]
        table = pk.Table(all_players)
        table.reset_cycle_states()


        # Valid inputs

        table.fold_player(Andy)
        table.fold_player(Boa)
        table.fold_player(Coral)


        # Invalid types

        with self.assertRaises(TypeError) as cm:
            table.activate_player('Dino')
        self.assertEqual(cm.exception.args[0], pk.messages.table_not_player_instance_message.format(str.__name__))


        # Invalid values
        
        with self.assertRaises(ValueError) as cm:
            table.activate_player(pk.Player('Dino'))
        self.assertEqual(cm.exception.args[0], pk.messages.table_player_not_in_table_message.format('Dino'))

        with self.assertRaises(ValueError) as cm:
            table.fold_player(Andy)
        self.assertEqual(cm.exception.args[0], pk.messages.table_player_already_folded_message.format(Andy.name))


    def test_set_last_aggressive_player_method(self):


        """
        Runs test cases on set_last_aggressive_player method.
        """


        all_players = [
            Andy := pk.Player('Andy'),
            Boa := pk.Player('Boa'),
            Coral := pk.Player('Coral'),
        ]
        table = pk.Table(all_players)
        table.activate_player(Andy)
        table.activate_player(Boa)


        # Valid inputs

        table.set_last_aggressive_player(Andy)
        table.set_last_aggressive_player(Boa)


        # Invalid types

        with self.assertRaises(TypeError) as cm:
            table.set_last_aggressive_player('Dino')
        self.assertEqual(cm.exception.args[0], pk.messages.table_not_player_instance_message.format(str.__name__))


        # Invalid values
        
        with self.assertRaises(ValueError) as cm:
            table.set_last_aggressive_player(pk.Player('Dino'))
        self.assertEqual(cm.exception.args[0], pk.messages.table_player_not_in_table_message.format('Dino'))

        with self.assertRaises(ValueError) as cm:
            table.set_last_aggressive_player(Coral)
        self.assertEqual(cm.exception.args[0], pk.messages.table_player_already_folded_message.format(Coral.name))


    def test_deal_to_players_method(self):


        """
        Runs test cases on deal_to_players method.
        """


        all_players = [
            pk.Player('Andy'),
            pk.Player('Boa'),
            pk.Player('Coral'),
        ]
        table = pk.Table(all_players)


        # Valid inputs

        table.deal_to_players(3)


        # Invalid types

        with self.assertRaises(TypeError) as cm:
            table.deal_to_players('Andy')
        self.assertEqual(cm.exception.args[0], pk.messages.table_not_int_cards_count_message.format(str.__name__))


    def test_deal_to_players_method(self):


        """
        Runs test cases on deal_common_cards method.
        """


        all_players = [
            pk.Player('Andy'),
            pk.Player('Boa'),
            pk.Player('Coral'),
        ]
        table = pk.Table(all_players)


        # Valid inputs

        table.deal_common_cards(3)


        # Invalid types

        with self.assertRaises(TypeError) as cm:
            table.deal_common_cards('Andy')
        self.assertEqual(cm.exception.args[0], pk.messages.table_not_int_cards_count_message.format(str.__name__))


if __name__ == '__main__':
    main()