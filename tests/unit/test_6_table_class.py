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

        structures.Table([structures.Player('Andy'), structures.Player('Boa')])

        structures.Table(
            [structures.Player('Andy'), structures.Player('Boa')],
            smallest_chip = 5,
        )

        structures.Table(
            [structures.Player('Andy'), structures.Player('Boa')],
            smallest_chip = 5,
            smallest_bet = 10,
        )

        structures.Table(
            [structures.Player('Andy'), structures.Player('Boa')],
            smallest_chip = 5,
            smallest_bet = 10,
            open_fold_allowed = True,
        )


        # Invalid inputs

        # Argument 'players' is not a list
        with self.assertRaises(TypeError) as cm:
            structures.Table('Wood')
        self.assertEqual(cm.exception.args[0], messages.table_not_list_players_message.format(str.__name__))
        
        # Not all elements in argument 'players' are players
        with self.assertRaises(TypeError) as cm:
            structures.Table([structures.Player('Andy'), 'Boa'])
        self.assertEqual(cm.exception.args[0], messages.table_not_all_player_instances_message)

        # Argument 'smallest_chip' is not an integer
        with self.assertRaises(TypeError) as cm:
            structures.Table(
                [structures.Player('Andy'), structures.Player('Boa')],
                smallest_chip = '5'
            )
        self.assertEqual(cm.exception.args[0], messages.table_not_int_smallest_chip_message.format(str.__name__))

        # Argument 'smallest_chip' is not positive
        with self.assertRaises(ValueError) as cm:
            structures.Table(
                [structures.Player('Andy'), structures.Player('Boa')],
                smallest_chip = -5
            )
        self.assertEqual(cm.exception.args[0], messages.table_smallest_chip_not_more_than_zero_message.format(-5))

        # Argument 'smallest_bet' is not an integer
        with self.assertRaises(TypeError) as cm:
            structures.Table(
                [structures.Player('Andy'), structures.Player('Boa')],
                smallest_chip = 5,
                smallest_bet = '10'
            )
        self.assertEqual(cm.exception.args[0], messages.table_not_int_smallest_bet_message.format(str.__name__))

        # Argument 'smallest_bet' is not a multiple of 'smallest_chip'
        with self.assertRaises(ValueError) as cm:
            structures.Table(
                [structures.Player('Andy'), structures.Player('Boa')],
                smallest_chip = 5,
                smallest_bet = 7,
            )
        self.assertEqual(cm.exception.args[0], messages.table_smallest_bet_not_multiple_of_smallest_chip_message.format(5, 7))

        # Argument 'smallest_bet' is not positive
        with self.assertRaises(ValueError) as cm:
            structures.Table(
                [structures.Player('Andy'), structures.Player('Boa')],
                smallest_chip = 5,
                smallest_bet = -10
            )
        self.assertEqual(cm.exception.args[0], messages.table_smallest_bet_not_multiple_of_smallest_chip_message.format(5, -10))


    def test_activate_player_and_fold_player_methods(self):


        """
        Runs test cases on activate_player and fold_player methods.
        """


        all_players = [
            Andy := structures.Player('Andy'),
            Boa := structures.Player('Boa'),
            Coral := structures.Player('Coral'),
        ]
        table = structures.Table(all_players)


        # Valid inputs

        self.assertTupleEqual(table.active_players, ())

        table.activate_player(Andy)
        self.assertTupleEqual(table.active_players, (Andy,))

        table.activate_player(Boa)
        self.assertTupleEqual(table.active_players, (Andy, Boa))

        table.activate_player(Coral)
        self.assertTupleEqual(table.active_players, (Andy, Boa, Coral))

        table.fold_player(Andy)
        self.assertTupleEqual(table.active_players, (Boa, Coral))

        table.fold_player(Boa)
        self.assertTupleEqual(table.active_players, (Coral,))

        table.fold_player(Coral)
        self.assertTupleEqual(table.active_players, ())


        # Invalid inputs

        with self.assertRaises(TypeError) as cm:
            table.activate_player('Dino')
        self.assertEqual(cm.exception.args[0], messages.table_not_player_instance_message.format(str.__name__))

        with self.assertRaises(TypeError) as cm:
            table.fold_player('Dino')
        self.assertEqual(cm.exception.args[0], messages.table_not_player_instance_message.format(str.__name__))

        with self.assertRaises(ValueError) as cm:
            table.activate_player(structures.Player('Dino'))
        self.assertEqual(cm.exception.args[0], messages.table_player_not_in_table_message.format('Dino'))

        with self.assertRaises(ValueError) as cm:
            table.fold_player(structures.Player('Dino'))
        self.assertEqual(cm.exception.args[0], messages.table_player_not_in_table_message.format('Dino'))

        with self.assertRaises(ValueError) as cm:
            table.fold_player(Andy)
        self.assertEqual(cm.exception.args[0], messages.table_player_already_folded_message.format('Andy'))


    def test_set_stopping_player_method(self):


        """
        Runs test cases on set_stopping_player method.
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

        table.set_stopping_player(Andy)
        self.assertEqual(table.stopping_player, Andy)

        table.set_stopping_player(Boa)
        self.assertEqual(table.stopping_player, Boa)


        # Invalid inputs

        with self.assertRaises(TypeError) as cm:
            table.set_stopping_player('Dino')
        self.assertEqual(cm.exception.args[0], messages.table_not_player_instance_message.format(str.__name__))
        
        with self.assertRaises(ValueError) as cm:
            table.set_stopping_player(structures.Player('Dino'))
        self.assertEqual(cm.exception.args[0], messages.table_player_not_in_table_message.format('Dino'))


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
        for player in all_players:
            table.activate_player(player)

        for player in all_players:
            self.assertEqual(len(player.cards), 0)


        # Valid inputs

        table.deal_to_players(3)

        self.assertSetEqual(
            set(table.deck).union(*[player.cards for player in table.players]),
            set(structures.Card(value, suit) for value, suit in constants.full_sorted_values_and_suits)
        )

        for player in all_players:
            self.assertEqual(len(player.cards), 3)


        # Invalid inputs

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

        self.assertEqual(len(table.common_cards), 0)


        # Valid inputs

        table.deal_common_cards(10)

        self.assertSetEqual(
            set(table.deck).union(table.common_cards),
            set(structures.Card(value, suit) for value, suit in constants.full_sorted_values_and_suits)
        )

        self.assertEqual(len(table.common_cards), 10)


        # Invalid types

        with self.assertRaises(TypeError) as cm:
            table.deal_common_cards('AKQJT')
        self.assertEqual(cm.exception.args[0], messages.table_not_int_cards_count_message.format(str.__name__))


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


        # Invalid inputs

        with self.assertRaises(TypeError) as cm:
            table.add_to_current_amount('100')
        self.assertEqual(cm.exception.args[0], messages.table_not_int_current_amount_message.format(str.__name__))

        with self.assertRaises(ValueError) as cm:
            table.add_to_current_amount(-100)
        self.assertEqual(cm.exception.args[0], messages.table_not_smallest_chip_multiple_increase_message.format(10, -100))

        with self.assertRaises(ValueError) as cm:
            table.add_to_current_amount(5)
        self.assertEqual(cm.exception.args[0], messages.table_not_smallest_chip_multiple_increase_message.format(10, 5))

        with self.assertRaises(ValueError) as cm:
            table.add_to_current_amount(107)
        self.assertEqual(cm.exception.args[0], messages.table_not_smallest_chip_multiple_increase_message.format(10, 107))


    def test_overwrite_smallest_rising_amount(self):


        """
        Runs test cases on overwrite_smallest_rising_amount method.
        """


        all_players = [
            structures.Player('Andy'),
            structures.Player('Boa'),
            structures.Player('Coral'),
        ]
        table = structures.Table(all_players, smallest_chip=10)


        # Valid inputs

        table.overwrite_smallest_rising_amount(50)
        self.assertEqual(table.smallest_rising_amount, 50)

        table.overwrite_smallest_rising_amount(100)
        self.assertEqual(table.smallest_rising_amount, 100)


        # Invalid inputs

        with self.assertRaises(TypeError) as cm:
            table.overwrite_smallest_rising_amount('100')
        self.assertEqual(cm.exception.args[0], messages.table_not_int_smallest_rising_amount_message.format(str.__name__))

        with self.assertRaises(ValueError) as cm:
            table.overwrite_smallest_rising_amount(-100)
        self.assertEqual(cm.exception.args[0], messages.table_sra_not_multiple_of_smallest_chip_message.format(10, -100))

        with self.assertRaises(ValueError) as cm:
            table.overwrite_smallest_rising_amount(0)
        self.assertEqual(cm.exception.args[0], messages.table_sra_not_multiple_of_smallest_chip_message.format(10, 0))

        with self.assertRaises(ValueError) as cm:
            table.overwrite_smallest_rising_amount(5)
        self.assertEqual(cm.exception.args[0], messages.table_sra_not_multiple_of_smallest_chip_message.format(10, 5))

        with self.assertRaises(ValueError) as cm:
            table.overwrite_smallest_rising_amount(107)
        self.assertEqual(cm.exception.args[0], messages.table_sra_not_multiple_of_smallest_chip_message.format(10, 107))


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
        self.assertEqual(cm.exception.args[0], messages.table_not_smallest_chip_multiple_increase_message.format(10, -100))


        # Not multiple of smallest chip

        with self.assertRaises(ValueError) as cm:
            table.add_to_central_pot(5)
        self.assertEqual(cm.exception.args[0], messages.table_not_smallest_chip_multiple_increase_message.format(10, 5))

        with self.assertRaises(ValueError) as cm:
            table.add_to_central_pot(107)
        self.assertEqual(cm.exception.args[0], messages.table_not_smallest_chip_multiple_increase_message.format(10, 107))


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
        table.set_stopping_player(Andy)

        table.reset_betting_round_states()

        self.assertEqual(table.current_amount, 0)
        self.assertIsNone(table.stopping_player)
    

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
        table.set_stopping_player(Andy)
        table.deal_common_cards(5)
        table.deal_to_players(2)
        table.add_to_central_pot(300)

        table.reset_cycle_states()

        self.assertEqual(table.current_amount, 0)
        self.assertIsNone(table.stopping_player)
        self.assertTupleEqual(table.active_players, tuple(all_players))
        self.assertTupleEqual(table.deck, tuple(structures.Card(value, suit) for value, suit in constants.full_sorted_values_and_suits))
        self.assertEqual(table.central_pot, 0)


if __name__ == '__main__':
    main()