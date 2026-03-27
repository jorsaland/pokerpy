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
            structures.Player('Andy', 10),
            structures.Player('Boa', 10),
            structures.Player('Coral', 10),
        ])


        # Type errors

        # Invalid table
        with self.assertRaises(TypeError) as cm:
            structures.Table('Wood')
        self.assertEqual(cm.exception.args[0], messages.msg_not_list.format(str.__name__))

        # Invalid player in table
        with self.assertRaises(TypeError) as cm:
            structures.Table([structures.Player('Andy', 10), 'Boa'])
        self.assertEqual(cm.exception.args[0], messages.msg_not_all_player_instances)

        # Invalid smallest bet
        with self.assertRaises(TypeError) as cm:
            structures.Table([structures.Player('Andy', 10)], smallest_bet_amount='zero')
        self.assertEqual(cm.exception.args[0], messages.msg_not_int.format(str.__name__))

        # Invalid starting player
        with self.assertRaises(TypeError) as cm:
            structures.Table([structures.Player('Andy', 10)], starting_player='Andy')
        self.assertEqual(cm.exception.args[0], messages.msg_not_player_instance.format(str.__name__))

        # Invalid stopping player
        with self.assertRaises(TypeError) as cm:
            structures.Table([structures.Player('Andy', 10)], stopping_player='Andy')
        self.assertEqual(cm.exception.args[0], messages.msg_not_player_instance.format(str.__name__))

        # Value errors

        # Empty table
        with self.assertRaises(ValueError) as cm:
            structures.Table([])
        self.assertEqual(cm.exception.args[0], messages.msg_no_players_in_table)

        # Zero smallest bet
        with self.assertRaises(ValueError) as cm:
            structures.Table([structures.Player('Andy', 10)], smallest_bet_amount=0)
        self.assertEqual(cm.exception.args[0], messages.msg_not_positive_value.format(0))

        # Negative smallest bet
        with self.assertRaises(ValueError) as cm:
            structures.Table([structures.Player('Andy', 10)], smallest_bet_amount=-1)
        self.assertEqual(cm.exception.args[0], messages.msg_not_positive_value.format(-1))

        # Starting player not in table
        with self.assertRaises(ValueError) as cm:
            structures.Table([structures.Player('Andy', 10)], starting_player=structures.Player('Boa', 10))
        self.assertEqual(cm.exception.args[0], messages.msg_player_not_in_table.format('Boa'))

        # Stopping player not in table
        with self.assertRaises(ValueError) as cm:
            structures.Table([structures.Player('Andy', 10)], stopping_player=structures.Player('Boa', 10))
        self.assertEqual(cm.exception.args[0], messages.msg_player_not_in_table.format('Boa'))


    def test_remove_card_from_deck_method(self):


        """
        Runs test cases on remove_card_from_deck method.
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


        # Invalid inputs

        with self.assertRaises(TypeError) as cm:
            table.remove_card_from_deck('7c')
        self.assertEqual(cm.exception.args[0], messages.msg_not_card_instance.format(str.__name__))

        with self.assertRaises(ValueError) as cm:
            table.remove_card_from_deck(structures.Card('7', 'c'))
        self.assertEqual(cm.exception.args[0], messages.msg_card_not_in_deck)


    def test_assign_common_card_method(self):


        """
        Runs test cases on assign_common_card method.
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


        # Invalid inputs

        with self.assertRaises(TypeError) as cm:
            table.assign_common_card('7c')
        self.assertEqual(cm.exception.args[0], messages.msg_not_card_instance.format(str.__name__))

        with self.assertRaises(ValueError) as cm:
            table.assign_common_card(structures.Card('7', 'c'))
        self.assertEqual(cm.exception.args[0], messages.msg_repeated_cards)


    def test_add_to_current_amount_method(self):


        """
        Runs test cases on add_to_current_amount method.
        """


        table = structures.Table([
            structures.Player('Andy', 10),
            structures.Player('Boa', 10),
            structures.Player('Coral', 10),
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
            structures.Player('Andy', 10),
            structures.Player('Boa', 10),
            structures.Player('Coral', 10),
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
        Andy.fold()
        self.assertEqual(table.get_previous_active_player(Andy), Coral)
        self.assertEqual(table.get_previous_active_player(Boa), Coral)
        self.assertEqual(table.get_previous_active_player(Coral), Boa)

        # One folded and one all-in
        Boa.remove_from_stack(10)
        self.assertEqual(table.get_previous_active_player(Andy), Coral)
        self.assertEqual(table.get_previous_active_player(Boa), Coral)
        self.assertEqual(table.get_previous_active_player(Coral), Coral)

        # Nobody active
        Coral.fold()
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



    def test_reset_betting_round_states_method(self):


        """
        Runs test cases on reset_betting_round_states method.
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
        Andy.fold()

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

        table.reset_betting_round_states()
        for player in table.players:
            player.reset_betting_round_states()

        # Evaluate after states

        self.assertEqual(Andy.requested_action, None)
        self.assertEqual(Andy.current_amount, 0)
        self.assertTupleEqual(Andy.cards, tuple(player_cards))
        self.assertEqual(Andy.hand, hand)
        self.assertTrue(Andy.is_folded)

        self.assertTupleEqual(table.players_in_hand, tuple(player for player in table.players if player != Andy))
        self.assertEqual(table.current_amount, 0)
        self.assertEqual(table.central_pot, 500)
        self.assertTupleEqual(table.common_cards, tuple(common_cards))
        self.assertSetEqual(set(table.deck), set(card for card in deck if card not in (*player_cards, *common_cards)))
    

    def test_reset_cycle_states_method(self):


        """
        Runs test cases on reset_cycle_states method.
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
        Andy.fold()

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

        table.reset_cycle_states()
        for player in table.players:
            player.reset_cycle_states()

        # Evaluate after states

        self.assertEqual(Andy.requested_action, None)
        self.assertEqual(Andy.current_amount, 0)
        self.assertTupleEqual(Andy.cards, ())
        self.assertEqual(Andy.hand, None)
        self.assertFalse(Andy.is_folded)

        self.assertTupleEqual(table.players_in_hand, table.players)
        self.assertEqual(table.current_amount, 0)
        self.assertEqual(table.central_pot, 0)
        self.assertTupleEqual(table.common_cards, ())
        self.assertSetEqual(set(table.deck), set(deck))


if __name__ == '__main__':
    main()