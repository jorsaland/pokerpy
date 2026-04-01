"""
Defines unit tests on Table class.
"""


import sys
sys.path.insert(0, '.')


from unittest import main, TestCase


from pokerpy import constants, messages, structures


class TestTableClassInstantiation(TestCase):


    """
    Runs unit tests on Table class instantiation.
    """


    def test_instantiation(self):


        """
        Runs test cases on class instantiation.
        """


        # Valid inputs

        table = structures.Table([
            Andy := structures.Player('Andy', 10),
            Boa := structures.Player('Boa', 10),
            Coral := structures.Player('Coral', 10),
        ])
        self.assertSetEqual(set(table.players), {Andy, Boa, Coral})
        self.assertEqual(table.starting_player, Andy)
        self.assertEqual(table.stopping_player, Coral)
        self.assertSetEqual(set(table.players_in_hand), {Andy, Boa, Coral})
        self.assertEqual(table.full_bet, 1)
        self.assertEqual(table.full_raise_increase, 1)
        self.assertEqual(table.current_level, 0)
        self.assertEqual(table.complete_current_level, 0)
        self.assertEqual(table.central_pot, 0)
        self.assertSetEqual(
            set(table.deck),
            {structures.Card(value, suit) for value, suit in constants.full_sorted_values_and_suits}
        )
        self.assertSetEqual(set(table.common_cards), set())

        table = structures.Table(
            players = [
                Andy := structures.Player('Andy', 10),
                Boa := structures.Player('Boa', 10),
                Coral := structures.Player('Coral', 10),
            ],
            full_bet = 5,
            starting_player = Boa,
            stopping_player = Andy,
        )
        self.assertSetEqual(set(table.players), {Andy, Boa, Coral})
        self.assertEqual(table.starting_player, Boa)
        self.assertEqual(table.stopping_player, Andy)
        self.assertSetEqual(set(table.players_in_hand), {Andy, Boa, Coral})
        self.assertEqual(table.full_bet, 5)
        self.assertEqual(table.full_raise_increase, 5)
        self.assertEqual(table.current_level, 0)
        self.assertEqual(table.complete_current_level, 0)
        self.assertEqual(table.central_pot, 0)
        self.assertSetEqual(
            set(table.deck),
            {structures.Card(value, suit) for value, suit in constants.full_sorted_values_and_suits}
        )
        self.assertSetEqual(set(table.common_cards), set())

        # Type errors

        # Invalid table
        with self.assertRaises(TypeError) as context:
            structures.Table('Wood')
        self.assertEqual(context.exception.args[0], messages.msg_not_list.format(str.__name__))

        # Invalid player in table
        with self.assertRaises(TypeError) as context:
            structures.Table([structures.Player('Andy', 10), 'Boa'])
        self.assertEqual(context.exception.args[0], messages.msg_not_all_player_instances)

        # Invalid smallest bet
        with self.assertRaises(TypeError) as context:
            structures.Table([structures.Player('Andy', 10)], full_bet='zero')
        self.assertEqual(context.exception.args[0], messages.msg_not_int.format(str.__name__))

        # Invalid starting player
        with self.assertRaises(TypeError) as context:
            structures.Table([structures.Player('Andy', 10)], starting_player='Andy')
        self.assertEqual(context.exception.args[0], messages.msg_not_player_instance.format(str.__name__))

        # Invalid stopping player
        with self.assertRaises(TypeError) as context:
            structures.Table([structures.Player('Andy', 10)], stopping_player='Andy')
        self.assertEqual(context.exception.args[0], messages.msg_not_player_instance.format(str.__name__))

        # Value errors

        # Empty table
        with self.assertRaises(ValueError) as context:
            structures.Table([])
        self.assertEqual(context.exception.args[0], messages.msg_no_players_in_table)

        # Zero smallest bet
        with self.assertRaises(ValueError) as context:
            structures.Table([structures.Player('Andy', 10)], full_bet=0)
        self.assertEqual(context.exception.args[0], messages.msg_not_positive_value.format(0))

        # Negative smallest bet
        with self.assertRaises(ValueError) as context:
            structures.Table([structures.Player('Andy', 10)], full_bet=-1)
        self.assertEqual(context.exception.args[0], messages.msg_not_positive_value.format(-1))

        # Starting player not in table
        with self.assertRaises(ValueError) as context:
            structures.Table([structures.Player('Andy', 10)], starting_player=structures.Player('Dino', 10))
        self.assertEqual(context.exception.args[0], messages.msg_player_not_in_table.format('Dino'))

        # Stopping player not in table
        with self.assertRaises(ValueError) as context:
            structures.Table([structures.Player('Andy', 10)], stopping_player=structures.Player('Dino', 10))
        self.assertEqual(context.exception.args[0], messages.msg_player_not_in_table.format('Dino'))


class TestTableClassMethodsForCards(TestCase):


    """
    Runs unit tests on Table class related to cards.
    """


    def test_methods_for_deck(self):


        """
        Runs test cases on remove_card_from_deck and reset_deck methods.
        """


        table = structures.Table([
            structures.Player('Andy', 10),
            structures.Player('Boa', 10),
            structures.Player('Coral', 10),
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

        table.reset_deck()

        self.assertEqual(
            set(table.deck),
            {structures.Card(value, suit) for value, suit in constants.full_sorted_values_and_suits},
        )


        # Invalid inputs

        with self.assertRaises(TypeError) as context:
            table.remove_card_from_deck('7c')
        self.assertEqual(context.exception.args[0], messages.msg_not_card_instance.format(str.__name__))

        table.remove_card_from_deck(structures.Card('2', 's'))
        with self.assertRaises(ValueError) as context:
            table.remove_card_from_deck(structures.Card('2', 's'))
        self.assertEqual(context.exception.args[0], messages.msg_card_not_in_deck)


    def test_methods_for_common_cards(self):


        """
        Runs test cases on assign_common_card and reset_common_cards methods.
        """


        table = structures.Table([
            structures.Player('Andy', 10),
            structures.Player('Boa', 10),
            structures.Player('Coral', 10),
        ])


        # Before and after effects

        self.assertSetEqual(set(table.common_cards), set())

        table.assign_common_card(structures.Card('7', 'c'))
        table.assign_common_card(structures.Card('T', 'd'))
        table.assign_common_card(structures.Card('2', 's'))

        self.assertEqual(
            set(table.common_cards), {structures.Card('7', 'c'), structures.Card('T', 'd'), structures.Card('2', 's')}
        )

        table.reset_common_cards()
        self.assertEqual(set(table.common_cards), set())


        # Invalid inputs

        with self.assertRaises(TypeError) as context:
            table.assign_common_card('7c')
        self.assertEqual(context.exception.args[0], messages.msg_not_card_instance.format(str.__name__))

        table.assign_common_card(structures.Card('7', 'c'))
        with self.assertRaises(ValueError) as context:
            table.assign_common_card(structures.Card('7', 'c'))
        self.assertEqual(context.exception.args[0], messages.msg_repeated_cards)


class TestTableClassMethodsForCards(TestCase):


    """
    Runs unit tests on Table class related to money.
    """


    def test_methods_to_set_amounts(self):


        """
        Runs test cases on method_set_full_bet, method_set_full_raise_increase,
        method_set_current_level and method_set_complete_current_level methods.
        """


        table = structures.Table([
            structures.Player('Andy', 10),
            structures.Player('Boa', 10),
            structures.Player('Coral', 10),
        ])

        # Valid inputs

        table.set_full_bet(5)
        self.assertEqual(table.full_bet, 5)
        table.set_full_bet(10)
        self.assertEqual(table.full_bet, 10)

        table.set_full_raise_increase(5)
        self.assertEqual(table.full_raise_increase, 5)
        table.set_full_raise_increase(10)
        self.assertEqual(table.full_raise_increase, 10)

        table.set_current_level(5)
        self.assertEqual(table.current_level, 5)
        table.set_current_level(10)
        self.assertEqual(table.current_level, 10)

        table.set_complete_current_level(5)
        self.assertEqual(table.complete_current_level, 5)
        table.set_complete_current_level(10)
        self.assertEqual(table.complete_current_level, 10)

        # Type errors

        with self.assertRaises(TypeError) as context:
            table.set_full_bet('10')
        self.assertEqual(context.exception.args[0], messages.msg_not_int.format(str.__name__))

        with self.assertRaises(TypeError) as context:
            table.set_full_raise_increase('10')
        self.assertEqual(context.exception.args[0], messages.msg_not_int.format(str.__name__))

        with self.assertRaises(TypeError) as context:
            table.set_current_level('10')
        self.assertEqual(context.exception.args[0], messages.msg_not_int.format(str.__name__))

        with self.assertRaises(TypeError) as context:
            table.set_complete_current_level('10')
        self.assertEqual(context.exception.args[0], messages.msg_not_int.format(str.__name__))

        # Value errors

        with self.assertRaises(ValueError) as context:
            table.set_full_bet(-10)
        self.assertEqual(context.exception.args[0], messages.msg_not_positive_value.format(-10))

        with self.assertRaises(ValueError) as context:
            table.set_full_bet(0)
        self.assertEqual(context.exception.args[0], messages.msg_not_positive_value.format(0))

        with self.assertRaises(ValueError) as context:
            table.set_full_raise_increase(-10)
        self.assertEqual(context.exception.args[0], messages.msg_not_positive_value.format(-10))

        with self.assertRaises(ValueError) as context:
            table.set_full_raise_increase(0)
        self.assertEqual(context.exception.args[0], messages.msg_not_positive_value.format(0))

        with self.assertRaises(ValueError) as context:
            table.set_complete_current_level(-10)
        self.assertEqual(context.exception.args[0], messages.msg_not_positive_or_zero_value.format(-10))

        with self.assertRaises(ValueError) as context:
            table.set_complete_current_level(-10)
        self.assertEqual(context.exception.args[0], messages.msg_not_positive_or_zero_value.format(-10))


    def test_central_pot_methods(self):


        """
        Runs test cases on add_to_central_pot and reset_central_pot methods.
        """


        table = structures.Table([
            structures.Player('Andy', 10),
            structures.Player('Boa', 10),
            structures.Player('Coral', 10),
        ])


        # Before and after effects

        self.assertEqual(table.central_pot, 0)

        table.add_to_central_pot(0)
        table.add_to_central_pot(5)
        table.add_to_central_pot(10)

        self.assertEqual(table.central_pot, 15)

        table.reset_central_pot()

        self.assertEqual(table.central_pot, 0)

        # Invalid inputs

        with self.assertRaises(TypeError) as context:
            table.add_to_central_pot('10')
        self.assertEqual(context.exception.args[0], messages.msg_not_int.format(str.__name__))

        with self.assertRaises(ValueError) as context:
            table.add_to_central_pot(-10)
        self.assertEqual(context.exception.args[0], messages.msg_not_positive_or_zero_value.format(-10))



class TestTableClassMethodsForIteration(TestCase):


    """
    Runs unit tests on Table class related to iteration.
    """


    def test_get_next_player_method(self):


        """
        Runs test cases on get_next_player method.
        """

        # Normal cases

        table = structures.Table([
            Andy := structures.Player('Andy', 10),
            Boa := structures.Player('Boa', 10),
            Coral := structures.Player('Coral', 10),
        ])
        Dino = structures.Player('Dino', 10)

        # Valid inputs
        self.assertEqual(table.get_next_player(Andy), Boa)
        self.assertEqual(table.get_next_player(Boa), Coral)
        self.assertEqual(table.get_next_player(Coral), Andy)

        # Invalid inputs
        with self.assertRaises(ValueError) as context:
            table.get_next_player(Dino)
        self.assertEqual(context.exception.args[0], messages.msg_player_not_in_table.format(Dino.name))

        # Edge cases

        table = structures.Table([Andy := structures.Player('Andy', 10)])
        self.assertEqual(table.get_next_player(Andy), Andy)


    def test_get_previous_player_method(self):


        """
        Runs test cases on get_previous_player method.
        """

        # Normal cases

        table = structures.Table([
            Andy := structures.Player('Andy', 10),
            Boa := structures.Player('Boa', 10),
            Coral := structures.Player('Coral', 10),
        ])
        Dino = structures.Player('Dino', 10)

        # Valid inputs
        self.assertEqual(table.get_previous_player(Andy), Coral)
        self.assertEqual(table.get_previous_player(Boa), Andy)
        self.assertEqual(table.get_previous_player(Coral), Boa)

        # Invalid inputs
        with self.assertRaises(ValueError) as context:
            table.get_previous_player(Dino)
        self.assertEqual(context.exception.args[0], messages.msg_player_not_in_table.format(Dino.name))

        # Edge cases

        table = structures.Table([Andy := structures.Player('Andy', 10)])
        self.assertEqual(table.get_next_player(Andy), Andy)


    def test_iter_players_method_going_forward(self):


        """
        Runs test cases on iter_players method going forward.
        """


        table = structures.Table([
            Andy := structures.Player('Andy', 10),
            Boa := structures.Player('Boa', 10),
            Coral := structures.Player('Coral', 10),
        ])
        Dino = structures.Player('Dino', 10)

        # Iteration

        iterator = table.iter_players()
        self.assertEqual(next(iterator), Andy)
        self.assertEqual(next(iterator), Boa)
        self.assertEqual(next(iterator), Coral)
        with self.assertRaises(StopIteration) as context:
            next(iterator)
        self.assertIsNone(context.exception.value)

        iterator = table.iter_players(Andy)
        self.assertEqual(next(iterator), Andy)
        self.assertEqual(next(iterator), Boa)
        self.assertEqual(next(iterator), Coral)
        with self.assertRaises(StopIteration) as context:
            next(iterator)
        self.assertIsNone(context.exception.value)

        iterator = table.iter_players(Boa)
        self.assertEqual(next(iterator), Boa)
        self.assertEqual(next(iterator), Coral)
        self.assertEqual(next(iterator), Andy)
        with self.assertRaises(StopIteration) as context:
            next(iterator)
        self.assertIsNone(context.exception.value)

        iterator = table.iter_players(Coral)
        self.assertEqual(next(iterator), Coral)
        self.assertEqual(next(iterator), Andy)
        self.assertEqual(next(iterator), Boa)
        with self.assertRaises(StopIteration) as context:
            next(iterator)
        self.assertIsNone(context.exception.value)

        # For loop

        iterated_players = [player for player in table.iter_players()]
        self.assertEqual(iterated_players, [Andy, Boa, Coral])

        iterated_players = [player for player in table.iter_players(Andy)]
        self.assertEqual(iterated_players, [Andy, Boa, Coral])

        iterated_players = [player for player in table.iter_players(Boa)]
        self.assertEqual(iterated_players, [Boa, Coral, Andy])

        iterated_players = [player for player in table.iter_players(Coral)]
        self.assertEqual(iterated_players, [Coral, Andy, Boa])

        # Invalid inputs

        with self.assertRaises(ValueError) as context:
            table.iter_players(Dino)
        self.assertEqual(context.exception.args[0], messages.msg_player_not_in_table.format(Dino.name))


    def test_iter_players_method_going_backwards(self):


        """
        Runs test cases on iter_players method going backwards.
        """


        table = structures.Table([
            Andy := structures.Player('Andy', 10),
            Boa := structures.Player('Boa', 10),
            Coral := structures.Player('Coral', 10),
        ])
        Dino = structures.Player('Dino', 10)

        # Iteration

        iterator = table.iter_players(reverse=True)
        self.assertEqual(next(iterator), Andy)
        self.assertEqual(next(iterator), Coral)
        self.assertEqual(next(iterator), Boa)
        with self.assertRaises(StopIteration) as context:
            next(iterator)
        self.assertIsNone(context.exception.value)

        iterator = table.iter_players(Andy, reverse=True)
        self.assertEqual(next(iterator), Andy)
        self.assertEqual(next(iterator), Coral)
        self.assertEqual(next(iterator), Boa)
        with self.assertRaises(StopIteration) as context:
            next(iterator)
        self.assertIsNone(context.exception.value)

        iterator = table.iter_players(Boa, reverse=True)
        self.assertEqual(next(iterator), Boa)
        self.assertEqual(next(iterator), Andy)
        self.assertEqual(next(iterator), Coral)
        with self.assertRaises(StopIteration) as context:
            next(iterator)
        self.assertIsNone(context.exception.value)

        iterator = table.iter_players(Coral, reverse=True)
        self.assertEqual(next(iterator), Coral)
        self.assertEqual(next(iterator), Boa)
        self.assertEqual(next(iterator), Andy)
        with self.assertRaises(StopIteration) as context:
            next(iterator)
        self.assertIsNone(context.exception.value)

        # For loop

        iterated_players = [player for player in table.iter_players(reverse=True)]
        self.assertEqual(iterated_players, [Andy, Coral, Boa])

        iterated_players = [player for player in table.iter_players(Andy, reverse=True)]
        self.assertEqual(iterated_players, [Andy, Coral, Boa])

        iterated_players = [player for player in table.iter_players(Boa, reverse=True)]
        self.assertEqual(iterated_players, [Boa, Andy, Coral])

        iterated_players = [player for player in table.iter_players(Coral, reverse=True)]
        self.assertEqual(iterated_players, [Coral, Boa, Andy])

        # Invalid inputs

        with self.assertRaises(ValueError) as context:
            table.iter_players(Dino, reverse=True)
        self.assertEqual(context.exception.args[0], messages.msg_player_not_in_table.format(Dino.name))


    def test_iter_players_method_edge_cases(self):


        """
        Runs test cases on iter_players method edge cases.
        """

        # Iteration with a single player

        table = structures.Table([Andy := structures.Player('Andy', 10)])

        iterator = table.iter_players()
        self.assertEqual(next(iterator), Andy)
        with self.assertRaises(StopIteration) as context:
            next(iterator)
        self.assertIsNone(context.exception.value)

        iterator = table.iter_players(reverse=True)
        self.assertEqual(next(iterator), Andy)
        with self.assertRaises(StopIteration) as context:
            next(iterator)
        self.assertIsNone(context.exception.value)

        # For loop with a single player

        table = structures.Table([Andy := structures.Player('Andy', 10)])

        iterated_players = [player for player in table.iter_players()]
        self.assertEqual(iterated_players, [Andy])

        iterated_players = [player for player in table.iter_players(reverse=True)]
        self.assertEqual(iterated_players, [Andy])


    def test_get_previous_active_player_method(self):


        """
        Runs test cases on get_previous_active_player method
        """

        # Normal cases

        table = structures.Table([
            Andy := structures.Player('Andy', 10),
            Boa := structures.Player('Boa', 10),
            Coral := structures.Player('Coral', 10),
        ])
        Dino = structures.Player('Dino', 10)

        # Everybody active
        self.assertEqual(table.get_previous_active_player(Andy), Coral)
        self.assertEqual(table.get_previous_active_player(Boa), Andy)
        self.assertEqual(table.get_previous_active_player(Coral), Boa)

        # One folded
        Andy.mark_is_folded()
        self.assertEqual(table.get_previous_active_player(Andy), Coral)
        self.assertEqual(table.get_previous_active_player(Boa), Coral)
        self.assertEqual(table.get_previous_active_player(Coral), Boa)

        # One folded and one all-in
        Boa.remove_from_stack(10)
        self.assertEqual(table.get_previous_active_player(Andy), Coral)
        self.assertEqual(table.get_previous_active_player(Boa), Coral)
        self.assertEqual(table.get_previous_active_player(Coral), Coral)

        # Nobody active
        Coral.mark_is_folded()
        self.assertIsNone(table.get_previous_active_player(Andy))
        self.assertIsNone(table.get_previous_active_player(Boa))
        self.assertIsNone(table.get_previous_active_player(Coral))

        # Invalid inputs
        with self.assertRaises(ValueError) as context:
            table.get_previous_player(Dino)
        self.assertEqual(context.exception.args[0], messages.msg_player_not_in_table.format(Dino.name))

        # Edge cases

        table = structures.Table([Andy := structures.Player('Andy', 10)])
        self.assertEqual(table.get_previous_active_player(Andy), Andy)


if __name__ == '__main__':
    main()