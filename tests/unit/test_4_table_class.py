"""
Defines unit tests on Table class.
"""


import sys
sys.path.insert(0, '.')


from unittest import main, TestCase


from pokerpy import constants, messages, structures


class TestTableClassBasicMethods(TestCase):


    """
    Runs unit tests on Table class basic methods.
    """


    def test_instantiation(self):


        """
        Runs test cases on class instantiation.
        """


        # Valid inputs

        full_deck = tuple(structures.Card(value, suit) for value, suit in constants.full_sorted_values_and_suits)

        table = structures.Table([
            Andy := structures.Player('Andy', 10),
            Boa := structures.Player('Boa', 10),
            Coral := structures.Player('Coral', 10),
        ])
        self.assertTupleEqual(table.deck, full_deck)
        self.assertTupleEqual(table.common_cards, ())
        self.assertTupleEqual(table.players, (Andy, Boa, Coral))
        self.assertTupleEqual(table.participating_players, (Andy, Boa, Coral))
        self.assertTupleEqual(table.active_players, (Andy, Boa, Coral))
        self.assertEqual(table.starting_player, Andy)
        self.assertEqual(table.stopping_player, Coral)
        self.assertEqual(table.current_player, Andy)
        self.assertEqual(table.amount_level, 0)
        self.assertEqual(table.full_bet, 1)
        self.assertEqual(table.full_amount_level, 0)
        self.assertEqual(table.full_raise_increase, 1)
        self.assertEqual(table.pot, 0)
        self.assertEqual(table.central_pot, 0)
        self.assertEqual(table.central_pot, 0)
        self.assertTupleEqual(table.split_pot, (0,))

        table = structures.Table(
            players = [
                Andy := structures.Player('Andy', 10),
                Boa := structures.Player('Boa', 10),
                Coral := structures.Player('Coral', 10),
                Dino := structures.Player('Dino', 10),
            ],
            full_bet = 5,
            starting_player = Boa,
            stopping_player = Dino,
        )
        self.assertTupleEqual(table.deck, full_deck)
        self.assertTupleEqual(table.common_cards, ())
        self.assertTupleEqual(table.players, (Andy, Boa, Coral, Dino))
        self.assertTupleEqual(table.participating_players, (Andy, Boa, Coral, Dino))
        self.assertTupleEqual(table.active_players, (Andy, Boa, Coral, Dino))
        self.assertEqual(table.starting_player, Boa)
        self.assertEqual(table.stopping_player, Dino)
        self.assertEqual(table.current_player, Boa)
        self.assertEqual(table.amount_level, 0)
        self.assertEqual(table.full_bet, 5)
        self.assertEqual(table.full_amount_level, 0)
        self.assertEqual(table.full_raise_increase, 5)
        self.assertEqual(table.pot, 0)
        self.assertEqual(table.central_pot, 0)
        self.assertEqual(table.central_pot, 0)
        self.assertTupleEqual(table.split_pot, (0,))

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
            structures.Table([structures.Player('Andy', 10)], starting_player=structures.Player('Boa', 10))
        self.assertEqual(context.exception.args[0], messages.msg_player_not_in_table.format('Boa'))

        # Stopping player not in table
        with self.assertRaises(ValueError) as context:
            structures.Table([structures.Player('Andy', 10)], stopping_player=structures.Player('Boa', 10))
        self.assertEqual(context.exception.args[0], messages.msg_player_not_in_table.format('Boa'))


    def test_methods_for_deck(self):


        """
        Runs test cases on methods related to the deck.
        """


        full_deck = tuple(structures.Card(value, suit) for value, suit in constants.full_sorted_values_and_suits)

        table = structures.Table([
            structures.Player('Andy', 10),
            structures.Player('Boa', 10),
            structures.Player('Coral', 10),
        ])


        # Before and after effects

        self.assertTupleEqual(table.deck, full_deck)

        table.remove_card_from_deck(structures.Card('7', 'c'))
        table.remove_card_from_deck(structures.Card('T', 'd'))
        table.remove_card_from_deck(structures.Card('2', 's'))

        self.assertTupleEqual(table.deck, tuple(card for card in full_deck if (card.value, card.suit) not in (('7', 'c'), ('T', 'd'), ('2', 's'))))

        table.reset_deck()

        self.assertTupleEqual(table.deck, full_deck)


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
        Runs test cases on methods related to common cards.
        """


        table = structures.Table([
            structures.Player('Andy', 10),
            structures.Player('Boa', 10),
            structures.Player('Coral', 10),
        ])


        # Before and after effects

        self.assertTupleEqual(table.common_cards, ())

        table.assign_common_card(structures.Card('7', 'c'))
        table.assign_common_card(structures.Card('T', 'd'))
        table.assign_common_card(structures.Card('2', 's'))

        self.assertTupleEqual(table.common_cards, (structures.Card('7', 'c'), structures.Card('T', 'd'), structures.Card('2', 's')))

        table.reset_common_cards()

        self.assertTupleEqual(table.common_cards, ())


        # Invalid inputs

        with self.assertRaises(TypeError) as context:
            table.assign_common_card('7c')
        self.assertEqual(context.exception.args[0], messages.msg_not_card_instance.format(str.__name__))

        table.assign_common_card(structures.Card('7', 'c'))
        with self.assertRaises(ValueError) as context:
            table.assign_common_card(structures.Card('7', 'c'))
        self.assertEqual(context.exception.args[0], messages.msg_repeated_cards)


    def test_methods_for_money(self):


        """
        Runs test cases on methods related to money.
        """


        table = structures.Table([
            structures.Player('Andy', 10),
            structures.Player('Boa', 10),
            structures.Player('Coral', 10),
        ])


        # Valid inputs

        self.assertEqual(table.full_bet, 1)
        table.set_full_bet(5)
        self.assertEqual(table.full_bet, 5)
        table.set_full_bet(10)
        self.assertEqual(table.full_bet, 10)

        self.assertEqual(table.full_raise_increase, 1)
        table.set_full_raise_increase(5)
        self.assertEqual(table.full_raise_increase, 5)
        table.set_full_raise_increase(10)
        self.assertEqual(table.full_raise_increase, 10)

        self.assertEqual(table.amount_level, 0)
        table.set_amount_level(5)
        self.assertEqual(table.amount_level, 5)
        table.set_amount_level(10)
        self.assertEqual(table.amount_level, 10)

        self.assertEqual(table.full_amount_level, 0)
        table.set_full_amount_level(5)
        self.assertEqual(table.full_amount_level, 5)
        table.set_full_amount_level(10)
        self.assertEqual(table.full_amount_level, 10)

        self.assertEqual(table.central_pot, 0)
        table.increase_central_pot(0)
        self.assertEqual(table.central_pot, 0)
        table.increase_central_pot(5)
        self.assertEqual(table.central_pot, 5)
        table.increase_central_pot(10)
        self.assertEqual(table.central_pot, 15)

        table.clear_central_pot()
        self.assertEqual(table.central_pot, 0)


        # Type errors

        with self.assertRaises(TypeError) as context:
            table.set_full_bet('10')
        self.assertEqual(context.exception.args[0], messages.msg_not_int.format(str.__name__))

        with self.assertRaises(TypeError) as context:
            table.set_full_raise_increase('10')
        self.assertEqual(context.exception.args[0], messages.msg_not_int.format(str.__name__))

        with self.assertRaises(TypeError) as context:
            table.set_amount_level('10')
        self.assertEqual(context.exception.args[0], messages.msg_not_int.format(str.__name__))

        with self.assertRaises(TypeError) as context:
            table.set_full_amount_level('10')
        self.assertEqual(context.exception.args[0], messages.msg_not_int.format(str.__name__))

        with self.assertRaises(TypeError) as context:
            table.increase_central_pot('10')
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
            table.set_full_amount_level(-10)
        self.assertEqual(context.exception.args[0], messages.msg_not_positive_or_zero_value.format(-10))

        with self.assertRaises(ValueError) as context:
            table.set_full_amount_level(-10)
        self.assertEqual(context.exception.args[0], messages.msg_not_positive_or_zero_value.format(-10))

        with self.assertRaises(ValueError) as context:
            table.increase_central_pot(-10)
        self.assertEqual(context.exception.args[0], messages.msg_not_positive_or_zero_value.format(-10))


    def test_methods_for_players_setting(self):


        """
        Runs test cases on methods related to players setting.
        """


        table = structures.Table([
            Andy := structures.Player('Andy', 10),
            Boa := structures.Player('Boa', 10),
            Coral := structures.Player('Coral', 10),
            Dino := structures.Player('Dino', 10),
        ])


        # Valid inputs

        self.assertEqual(table.starting_player, Andy)
        table.set_starting_player(Andy)
        self.assertEqual(table.starting_player, Andy)
        table.set_starting_player(Boa)
        self.assertEqual(table.starting_player, Boa)

        self.assertEqual(table.stopping_player, Dino)
        table.set_stopping_player(Dino)
        self.assertEqual(table.stopping_player, Dino)
        table.set_stopping_player(Coral)
        self.assertEqual(table.stopping_player, Coral)

        self.assertEqual(table.current_player, Andy)
        table.set_current_player(Andy)
        self.assertEqual(table.current_player, Andy)
        table.set_current_player(Boa)
        self.assertEqual(table.current_player, Boa)


        # Type errors

        with self.assertRaises(TypeError) as context:
            table.set_starting_player('Andy')
        self.assertEqual(context.exception.args[0], messages.msg_not_player_instance.format(str.__name__))

        with self.assertRaises(TypeError) as context:
            table.set_stopping_player('Andy')
        self.assertEqual(context.exception.args[0], messages.msg_not_player_instance.format(str.__name__))

        with self.assertRaises(TypeError) as context:
            table.set_current_player('Andy')
        self.assertEqual(context.exception.args[0], messages.msg_not_player_instance.format(str.__name__))


        # Value errors

        with self.assertRaises(ValueError) as context:
            table.set_starting_player(structures.Player('Epa', 10))
        self.assertEqual(context.exception.args[0], messages.msg_player_not_in_table.format('Epa'))

        with self.assertRaises(ValueError) as context:
            table.set_stopping_player(structures.Player('Epa', 10))
        self.assertEqual(context.exception.args[0], messages.msg_player_not_in_table.format('Epa'))

        with self.assertRaises(ValueError) as context:
            table.set_current_player(structures.Player('Epa', 10))
        self.assertEqual(context.exception.args[0], messages.msg_player_not_in_table.format('Epa'))


    def test_methods_for_players_position(self):


        """
        Runs test cases on get_next_player method.
        """


        table = structures.Table([
            Andy := structures.Player('Andy', 10),
            Boa := structures.Player('Boa', 10),
            Coral := structures.Player('Coral', 10),
        ])


        # Valid inputs

        self.assertEqual(table.get_next_player(Andy), Boa)
        self.assertEqual(table.get_next_player(Boa), Coral)
        self.assertEqual(table.get_next_player(Coral), Andy)

        self.assertEqual(table.get_previous_player(Andy), Coral)
        self.assertEqual(table.get_previous_player(Boa), Andy)
        self.assertEqual(table.get_previous_player(Coral), Boa)


        # Type errors

        with self.assertRaises(TypeError) as context:
            table.get_next_player('Andy')
        self.assertEqual(context.exception.args[0], messages.msg_not_player_instance.format(str.__name__))

        with self.assertRaises(TypeError) as context:
            table.get_previous_player('Andy')
        self.assertEqual(context.exception.args[0], messages.msg_not_player_instance.format(str.__name__))


        # Value errors

        with self.assertRaises(ValueError) as context:
            table.get_next_player(structures.Player('Dino', 10))
        self.assertEqual(context.exception.args[0], messages.msg_player_not_in_table.format('Dino'))

        with self.assertRaises(ValueError) as context:
            table.get_previous_player(structures.Player('Dino', 10))
        self.assertEqual(context.exception.args[0], messages.msg_player_not_in_table.format('Dino'))


        # Edge cases

        small_table = structures.Table([Andy := structures.Player('Andy', 10)])
        self.assertEqual(small_table.get_next_player(Andy), Andy)
        self.assertEqual(small_table.get_previous_player(Andy), Andy)


    def test_get_previous_active_player_method(self):


        """
        Runs test cases on get_previous_active_player method
        """


        table = structures.Table([
            Andy := structures.Player('Andy', 10),
            Boa := structures.Player('Boa', 10),
            Coral := structures.Player('Coral', 10),
            Dino := structures.Player('Dino', 10),
        ])


        # Valid inputs

        # Everybody active
        self.assertEqual(table.get_previous_active_player(Andy), Dino)
        self.assertEqual(table.get_previous_active_player(Boa), Andy)
        self.assertEqual(table.get_previous_active_player(Coral), Boa)
        self.assertEqual(table.get_previous_active_player(Dino), Coral)

        # One is folded
        Andy.mark_is_folded()
        self.assertEqual(table.get_previous_active_player(Andy), Dino)
        self.assertEqual(table.get_previous_active_player(Boa), Dino)
        self.assertEqual(table.get_previous_active_player(Coral), Boa)
        self.assertEqual(table.get_previous_active_player(Dino), Coral)

        # One folded and one all-in
        Boa.decrease_stack(10)
        self.assertEqual(table.get_previous_active_player(Andy), Dino)
        self.assertEqual(table.get_previous_active_player(Boa), Dino)
        self.assertEqual(table.get_previous_active_player(Coral), Dino)
        self.assertEqual(table.get_previous_active_player(Dino), Coral)

        # Everyone folded or all-in
        Coral.mark_is_folded()
        Dino.decrease_stack(10)
        self.assertIsNone(table.get_previous_active_player(Andy))
        self.assertIsNone(table.get_previous_active_player(Boa))
        self.assertIsNone(table.get_previous_active_player(Coral))
        self.assertIsNone(table.get_previous_active_player(Dino))


        # Invalid inputs

        with self.assertRaises(TypeError) as context:
            table.get_previous_active_player('Andy')
        self.assertEqual(context.exception.args[0], messages.msg_not_player_instance.format(str.__name__))

        with self.assertRaises(ValueError) as context:
            table.get_next_player(structures.Player('Epa', 10))
        self.assertEqual(context.exception.args[0], messages.msg_player_not_in_table.format('Epa'))


        # Edge cases

        small_table = structures.Table([Andy := structures.Player('Andy', 10)])
        self.assertEqual(small_table.get_previous_active_player(Andy), Andy)


class TestTableClassSpecialPlayerAttributes(TestCase):


    """
    Runs unit tests on Table class special attributes related to players.
    """


    def test_when_players_go_all_in(self):


        """
        Runs test cases when players go all-in.
        """


        table = structures.Table([
            Andy := structures.Player('Andy', 10),
            Boa := structures.Player('Boa', 10),
            Coral := structures.Player('Coral', 10),
            Dino := structures.Player('Dino', 10),
        ])

        self.assertTupleEqual(table.participating_players, (Andy, Boa, Coral, Dino))
        self.assertTupleEqual(table.active_players, (Andy, Boa, Coral, Dino))

        Andy.decrease_stack(10)
        self.assertTupleEqual(table.participating_players, (Andy, Boa, Coral, Dino))
        self.assertTupleEqual(table.active_players, (Boa, Coral, Dino))

        Boa.decrease_stack(10)
        self.assertTupleEqual(table.participating_players, (Andy, Boa, Coral, Dino))
        self.assertTupleEqual(table.active_players, (Coral, Dino))

        Coral.decrease_stack(10)
        self.assertTupleEqual(table.participating_players, (Andy, Boa, Coral, Dino))
        self.assertTupleEqual(table.active_players, (Dino,))

        Dino.decrease_stack(10)
        self.assertTupleEqual(table.participating_players, (Andy, Boa, Coral, Dino))
        self.assertTupleEqual(table.active_players, ())


    def test_when_players_fold(self):


        """
        Runs test cases when players fold.
        """


        table = structures.Table([
            Andy := structures.Player('Andy', 10),
            Boa := structures.Player('Boa', 10),
            Coral := structures.Player('Coral', 10),
            Dino := structures.Player('Dino', 10),
        ])

        self.assertTupleEqual(table.participating_players, (Andy, Boa, Coral, Dino))
        self.assertTupleEqual(table.active_players, (Andy, Boa, Coral, Dino))

        Andy.mark_is_folded()
        self.assertTupleEqual(table.participating_players, (Boa, Coral, Dino))
        self.assertTupleEqual(table.active_players, (Boa, Coral, Dino))

        Boa.mark_is_folded()
        self.assertTupleEqual(table.participating_players, (Coral, Dino))
        self.assertTupleEqual(table.active_players, (Coral, Dino))

        Coral.mark_is_folded()
        self.assertTupleEqual(table.participating_players, (Dino,))
        self.assertTupleEqual(table.active_players, (Dino,))

        Dino.mark_is_folded()
        self.assertTupleEqual(table.participating_players, ())
        self.assertTupleEqual(table.active_players, ())


    def test_when_players_go_all_in_and_fold(self):


        """
        Runs test cases when players go all-in and fold.
        """


        table = structures.Table([
            Andy := structures.Player('Andy', 10),
            Boa := structures.Player('Boa', 10),
            Coral := structures.Player('Coral', 10),
            Dino := structures.Player('Dino', 10),
        ])

        self.assertTupleEqual(table.participating_players, (Andy, Boa, Coral, Dino))
        self.assertTupleEqual(table.active_players, (Andy, Boa, Coral, Dino))

        Andy.decrease_stack(10)
        self.assertTupleEqual(table.participating_players, (Andy, Boa, Coral, Dino))
        self.assertTupleEqual(table.active_players, (Boa, Coral, Dino))

        Boa.mark_is_folded()
        self.assertTupleEqual(table.participating_players, (Andy, Coral, Dino))
        self.assertTupleEqual(table.active_players, (Coral, Dino))

        Coral.decrease_stack(10)
        self.assertTupleEqual(table.participating_players, (Andy, Coral, Dino,))
        self.assertTupleEqual(table.active_players, (Dino,))

        Dino.mark_is_folded()
        self.assertTupleEqual(table.participating_players, (Andy, Coral))
        self.assertTupleEqual(table.active_players, ())


class TestTableClassSpecialPotAttributes(TestCase):


    """
    Runs unit tests on Table class special attributes related to the pot.
    """


    def test_when_players_end_being_active(self):


        """
        Runs test cases when players end being active.
        """


        table = structures.Table([
            Andy := structures.Player('Andy', 2),
            Boa := structures.Player('Boa', 3),
            Coral := structures.Player('Coral', 5),
            Dino := structures.Player('Dino', 10),
        ])


        Andy.decrease_stack(1)
        Andy.increase_amount(1)
        Andy.increase_pot_participation(1)
        self.assertEqual(table.pot, 1)

        Boa.decrease_stack(1)
        Boa.increase_amount(1)
        Boa.increase_pot_participation(1)
        self.assertEqual(table.pot, 2)

        Coral.decrease_stack(1)
        Coral.increase_amount(1)
        Coral.increase_pot_participation(1)
        self.assertEqual(table.pot, 3)

        Dino.decrease_stack(1)
        Dino.increase_amount(1)
        Dino.increase_pot_participation(1)
        self.assertEqual(table.pot, 4)

        self.assertTupleEqual(table.split_pot, (4,))


    def test_when_some_players_fold(self):


        """
        Runs test cases when some players fold.
        """


        table = structures.Table([
            Andy := structures.Player('Andy', 2),
            Boa := structures.Player('Boa', 3),
            Coral := structures.Player('Coral', 5),
            Dino := structures.Player('Dino', 10),
        ])


        Andy.decrease_stack(1)
        Andy.increase_amount(1)
        Andy.increase_pot_participation(1)
        self.assertEqual(table.pot, 1)

        Boa.mark_is_folded()
        self.assertEqual(table.pot, 1)

        Coral.decrease_stack(1)
        Coral.increase_amount(1)
        Coral.increase_pot_participation(1)
        self.assertEqual(table.pot, 2)

        Dino.mark_is_folded()
        self.assertEqual(table.pot, 2)

        self.assertTupleEqual(table.split_pot, (2,))


    def test_when_some_players_go_all_in(self):


        """
        Runs test cases when some players go all-in.
        """


        table = structures.Table([
            Andy := structures.Player('Andy', 2),
            Boa := structures.Player('Boa', 3),
            Coral := structures.Player('Coral', 5),
            Dino := structures.Player('Dino', 10),
        ])


        Andy.decrease_stack(2)
        Andy.increase_amount(2)
        Andy.increase_pot_participation(2)
        self.assertEqual(table.pot, 2)

        Boa.decrease_stack(3)
        Boa.increase_amount(3)
        Boa.increase_pot_participation(3)
        self.assertEqual(table.pot, 5)

        Coral.decrease_stack(4)
        Coral.increase_amount(4)
        Coral.increase_pot_participation(4)
        self.assertEqual(table.pot, 9)

        Dino.decrease_stack(4)
        Dino.increase_amount(4)
        Dino.increase_pot_participation(4)
        self.assertEqual(table.pot, 13)

        self.assertTupleEqual(table.split_pot, (8, 3, 2))


    def test_when_all_players_fold_or_go_all_in(self):


        """
        Runs test cases when all players fold or go all-in.
        """


        table = structures.Table([
            Andy := structures.Player('Andy', 2),
            Boa := structures.Player('Boa', 3),
            Coral := structures.Player('Coral', 5),
            Dino := structures.Player('Dino', 10),
        ])


        Andy.decrease_stack(2)
        Andy.increase_amount(2)
        Andy.increase_pot_participation(2)
        self.assertEqual(table.pot, 2)

        Boa.decrease_stack(3)
        Boa.increase_amount(3)
        Boa.increase_pot_participation(3)
        self.assertEqual(table.pot, 5)

        Coral.decrease_stack(5)
        Coral.increase_amount(5)
        Coral.increase_pot_participation(5)
        self.assertEqual(table.pot, 10)

        Dino.mark_is_folded()
        self.assertEqual(table.pot, 10)

        self.assertTupleEqual(table.split_pot, (6, 2, 2))


class TestTableClassPlayerIteration(TestCase):


    """
    Runs unit tests on Table class player iteration.
    """


    def test_iter_players_method_going_forward(self):


        """
        Runs test cases on iter_players method going forward.
        """


        table = structures.Table([
            Andy := structures.Player('Andy', 10),
            Boa := structures.Player('Boa', 10),
            Coral := structures.Player('Coral', 10),
        ])


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

        with self.assertRaises(TypeError) as context:
            table.iter_players('Dino')
        self.assertEqual(context.exception.args[0], messages.msg_not_player_instance.format(str.__name__))

        with self.assertRaises(ValueError) as context:
            table.iter_players(structures.Player('Dino', 10))
        self.assertEqual(context.exception.args[0], messages.msg_player_not_in_table.format('Dino'))


    def test_iter_players_method_going_backwards(self):


        """
        Runs test cases on iter_players method going backwards.
        """


        table = structures.Table([
            Andy := structures.Player('Andy', 10),
            Boa := structures.Player('Boa', 10),
            Coral := structures.Player('Coral', 10),
        ])


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

        with self.assertRaises(TypeError) as context:
            table.iter_players('Dino', reverse=True)
        self.assertEqual(context.exception.args[0], messages.msg_not_player_instance.format(str.__name__))

        with self.assertRaises(ValueError) as context:
            table.iter_players(structures.Player('Dino', 10), reverse=True)
        self.assertEqual(context.exception.args[0], messages.msg_player_not_in_table.format('Dino'))


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


if __name__ == '__main__':
    main()