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
        self.assertEqual(cm.exception.args[0], messages.not_list_players_message.format(str.__name__))
        
        with self.assertRaises(TypeError) as cm:
            structures.Table([structures.Player('Andy'), 'Boa'])
        self.assertEqual(cm.exception.args[0], messages.not_all_player_instances_message)


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
        self.assertEqual(cm.exception.args[0], messages.not_player_instance_message.format(str.__name__))


        # Invalid values

        with self.assertRaises(ValueError) as cm:
            table.activate_player(structures.Player('Dino'))
        self.assertEqual(cm.exception.args[0], messages.player_not_in_table_message.format('Dino'))


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
        table.activate_all_players()


        # Valid inputs

        table.fold_player(Andy)
        table.fold_player(Boa)
        table.fold_player(Coral)


        # Invalid types

        with self.assertRaises(TypeError) as cm:
            table.activate_player('Dino')
        self.assertEqual(cm.exception.args[0], messages.not_player_instance_message.format(str.__name__))


        # Invalid values
        
        with self.assertRaises(ValueError) as cm:
            table.activate_player(structures.Player('Dino'))
        self.assertEqual(cm.exception.args[0], messages.player_not_in_table_message.format('Dino'))

        with self.assertRaises(ValueError) as cm:
            table.fold_player(Andy)
        self.assertEqual(cm.exception.args[0], messages.player_already_folded_message.format(Andy.name))


if __name__ == '__main__':
    main()