"""
Defines unit tests on BettingRound class.
"""


import sys
sys.path.insert(0, '.')


from collections.abc import Generator
from unittest import main, TestCase


from pokerpy import constants, engines, messages, structures


class TestBettingRoundBasicMethods(TestCase):


    """
    Run unit tests on BettingRound basic methods.
    """


    def test_instantiation(self):


        """
        Runs test cases on class instantiation
        """


        table = structures.Table([
            Andy := structures.Player('Andy', 10),
            Boa := structures.Player('Boa', 10),
            Coral := structures.Player('Coral', 10),
            Dino := structures.Player('Dino', 10),
        ])
        Epa = structures.Player('Epa', 10)

        # Valid instantiation

        betting_round = engines.BettingRound('test round', table)
        self.assertEqual(betting_round.name, 'test round')
        self.assertEqual(betting_round.table, table)
        self.assertEqual(betting_round.lap_counts, 0)
        self.assertEqual(betting_round.table.starting_player, Andy)
        self.assertEqual(betting_round.table.stopping_player, Dino)
        self.assertEqual(betting_round.table.smallest_bet_amount, 1)
        self.assertFalse(betting_round.is_completed)
        self.assertFalse(betting_round.open_fold_allowed)
        self.assertTrue(betting_round.ignore_invalid_actions)

        betting_round = engines.BettingRound(
            'test round',
            table,
            smallest_bet_amount = 10,
            starting_player = Coral,
            stopping_player = Boa,
            open_fold_allowed = True,
            ignore_invalid_actions = False,
        )
        self.assertEqual(betting_round.name, 'test round')
        self.assertEqual(betting_round.table, table)
        self.assertEqual(betting_round.lap_counts, 0)
        self.assertEqual(betting_round.table.starting_player, Coral)
        self.assertEqual(betting_round.table.stopping_player, Boa)
        self.assertEqual(betting_round.table.smallest_bet_amount, 10)
        self.assertFalse(betting_round.is_completed)
        self.assertTrue(betting_round.open_fold_allowed)
        self.assertFalse(betting_round.ignore_invalid_actions)

        betting_round = engines.BettingRound(
            'test round',
            table,
            open_fold_allowed = 1, ## expected boolean, but not enforced
            ignore_invalid_actions = 0, ## expected boolean, but not enforced
        )
        self.assertEqual(betting_round.open_fold_allowed, 1)
        self.assertFalse(betting_round.ignore_invalid_actions)

        # Type errors

        # Invalid name
        with self.assertRaises(TypeError) as context:
            engines.BettingRound(123456, table)
        self.assertEqual(context.exception.args[0], messages.msg_not_str.format(int.__name__))

        # Invalid table
        with self.assertRaises(TypeError) as context:
            engines.BettingRound('test round', 'wood')
        self.assertEqual(context.exception.args[0], messages.msg_not_table_instance.format(str.__name__))

        # Invalid smallest bet
        with self.assertRaises(TypeError) as context:
            engines.BettingRound('test round', table, smallest_bet_amount='zero')
        self.assertEqual(context.exception.args[0], messages.msg_not_int.format(str.__name__))

        # Invalid starting player
        with self.assertRaises(TypeError) as context:
            engines.BettingRound('test round', table, starting_player='first')
        self.assertEqual(context.exception.args[0], messages.msg_not_player_instance.format(str.__name__))

        # Invalid stopping player
        with self.assertRaises(TypeError) as context:
            engines.BettingRound('test round', table, stopping_player='last')
        self.assertEqual(context.exception.args[0], messages.msg_not_player_instance.format(str.__name__))

        # Value errors

        # Zero smallest bet
        with self.assertRaises(ValueError) as context:
            engines.BettingRound('test round', table, smallest_bet_amount=0)
        self.assertEqual(context.exception.args[0], messages.msg_not_positive_value.format(0))

        # Negative smallest bet
        with self.assertRaises(ValueError) as context:
            engines.BettingRound('test round', table, smallest_bet_amount=-1)
        self.assertEqual(context.exception.args[0], messages.msg_not_positive_value.format(-1))

        # Starting player not in table
        with self.assertRaises(ValueError) as context:
            engines.BettingRound('test round', table, starting_player=Epa)
        self.assertEqual(context.exception.args[0], messages.msg_player_not_in_table.format(Epa.name))

        # Stopping player not in table
        with self.assertRaises(ValueError) as context:
            engines.BettingRound('test round', table, stopping_player=Epa)
        self.assertEqual(context.exception.args[0], messages.msg_player_not_in_table.format(Epa.name))


    def test_simple_methods(self):


        """
        Runs test cases on methods that do not have much complexity.
        """


        table = structures.Table([
            Andy := structures.Player('Andy', 10),
            Boa := structures.Player('Boa', 10),
            Coral := structures.Player('Coral', 10),
            Dino := structures.Player('Dino', 10),
        ])

        betting_round = engines.BettingRound('test round', table)

        # Listen

        self.assertIsInstance(betting_round.listen(), Generator)

        # Counter

        self.assertEqual(betting_round.lap_counts, 0)

        betting_round.increase_counter()
        self.assertEqual(betting_round.lap_counts, 1)

        betting_round.increase_counter()
        self.assertEqual(betting_round.lap_counts, 2)

        # Stopping player

        self.assertEqual(betting_round.table.stopping_player, Dino)

        betting_round.table.set_stopping_player(Boa)
        self.assertEqual(betting_round.table.stopping_player, Boa)

        betting_round.table.set_stopping_player(Andy)
        self.assertEqual(betting_round.table.stopping_player, Andy)

        # Smallest raise amount

        self.assertEqual(betting_round.table.smallest_raise_amount, 1)

        betting_round.table.set_smallest_raise_amount(3)
        self.assertEqual(betting_round.table.smallest_raise_amount, 3)

        betting_round.table.set_smallest_raise_amount(5)
        self.assertEqual(betting_round.table.smallest_raise_amount, 5)


    def test_dealing_methods(self):


        """
        Runs test cases on methods related to dealing cards.
        """


        # Deal common cards

        table = structures.Table([
            structures.Player('Andy', 10),
            structures.Player('Boa', 10),
            structures.Player('Coral', 10),
            structures.Player('Dino', 10),
        ])

        betting_round = engines.BettingRound('test round', table)

        self.assertEqual(len(table.deck), 52)
        self.assertEqual(len(betting_round.table.common_cards), 0)

        betting_round.deal_common_cards(3)
        self.assertEqual(len(table.deck), 49)
        self.assertEqual(len(betting_round.table.common_cards), 3)

        betting_round.deal_common_cards(2)
        self.assertEqual(len(table.deck), 47)
        self.assertEqual(len(betting_round.table.common_cards), 5)

        # Deal cards to players

        table = structures.Table([
            structures.Player('Andy', 10),
            structures.Player('Boa', 10),
            structures.Player('Coral', 10),
            structures.Player('Dino', 10),
        ])

        betting_round = engines.BettingRound('test round', table)

        self.assertEqual(len(table.deck), 52)
        for player in betting_round.table.players:
            self.assertEqual(len(player.cards), 0)

        betting_round.deal_cards_to_players(3)
        self.assertEqual(len(table.deck), 40)
        for player in betting_round.table.players:
            self.assertEqual(len(player.cards), 3)

        betting_round.deal_cards_to_players(2)
        self.assertEqual(len(table.deck), 32)
        for player in betting_round.table.players:
            self.assertEqual(len(player.cards), 5)

class TestResetBettingRoundStatesFunction(TestCase):


    """
    Runs unit tests on reset_betting_round static method.
    """


    def test_invalid_input(self):


        """
        Runs test cases on reset_betting_round static method with an invalid input.
        """


        with self.assertRaises(TypeError) as context:
            engines.BettingRound.reset_betting_round_states('Wood')
        self.assertEqual(context.exception.args[0], messages.msg_not_table_instance.format(str.__name__))

    
    def test_reset_betting_round_states_function(self):


        """
        Runs test cases on reset_betting_round_states function effects.
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
        Andy.mark_is_folded()

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

        engines.BettingRound.reset_betting_round_states(table)

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


class TestBettingRoundListener(TestCase):


    """
    Run unit tests on BettingRound listener.
    """


    def test_successful_parses_and_closure_with_function_next(self):


        """
        Runs test cases where the amount of parsed actions is just the amount needed, and the betting round is closed successfully, using the function next to iterate.
        """


        table = structures.Table([
            Andy := structures.Player('Andy', 10),
            Boa := structures.Player('Boa', 10),
            Coral := structures.Player('Coral', 10),
            Dino := structures.Player('Dino', 10),
        ])

        betting_round = engines.BettingRound('test round', table)
        listener = betting_round.listen()

        # Before states

        self.assertEqual(table.central_pot, 0)
        self.assertEqual(betting_round.lap_counts, 0)
        self.assertEqual(next(listener), Andy)

        # Actions

        self.assertEqual(betting_round.table.stopping_player, Dino)
        Andy.request_action(structures.Action(constants.ACTION_BET, 1))
        self.assertEqual(next(listener), Boa)

        self.assertEqual(betting_round.table.stopping_player, Dino)
        Boa.request_action(structures.Action(constants.ACTION_RAISE, 2))
        self.assertEqual(next(listener), Coral)

        self.assertEqual(betting_round.table.stopping_player, Andy)
        Coral.request_action(structures.Action(constants.ACTION_RAISE, 4))
        self.assertEqual(next(listener), Dino)

        self.assertEqual(betting_round.table.stopping_player, Boa)
        Dino.request_action(structures.Action(constants.ACTION_FOLD))
        self.assertEqual(next(listener), Andy)

        self.assertEqual(betting_round.table.stopping_player, Boa)
        Andy.request_action(structures.Action(constants.ACTION_CALL, 3))
        self.assertEqual(next(listener), Boa)

        self.assertEqual(betting_round.table.stopping_player, Boa)
        Boa.request_action(structures.Action(constants.ACTION_CALL, 2))
        
        # After states

        self.assertIsNone(betting_round.close())
        self.assertEqual(table.central_pot, 12)
        self.assertEqual(table.current_amount, 0)

        self.assertEqual(Andy.current_amount, 0)
        self.assertEqual(Boa.current_amount, 0)
        self.assertEqual(Coral.current_amount, 0)
        self.assertEqual(Dino.current_amount, 0)


    def test_successful_parses_and_closure_with_for_loop(self):


        """
        Runs test cases where the amount of parsed actions is just the amount needed, and the betting round is closed successfully, using a for loop to iterate.
        """


        table = structures.Table([
            Andy := structures.Player('Andy', 10),
            Boa := structures.Player('Boa', 10),
            Coral := structures.Player('Coral', 10),
            Dino := structures.Player('Dino', 10),
        ])

        betting_round = engines.BettingRound('test round', table)

        actions_to_parse = [
            structures.Action(constants.ACTION_BET, 1),
            structures.Action(constants.ACTION_RAISE, 2),
            structures.Action(constants.ACTION_RAISE, 4),
            structures.Action(constants.ACTION_FOLD),
            structures.Action(constants.ACTION_CALL, 3),
            structures.Action(constants.ACTION_CALL, 2),
        ]

        # Before states

        self.assertEqual(table.central_pot, 0)
        self.assertEqual(betting_round.lap_counts, 0)

        # Actions

        for action, player in zip(actions_to_parse, betting_round.listen()):
            player.request_action(action)

        # After states

        self.assertIsNone(betting_round.close())
        self.assertEqual(table.central_pot, 12)
        self.assertEqual(table.current_amount, 0)

        self.assertEqual(Andy.current_amount, 0)
        self.assertEqual(Boa.current_amount, 0)
        self.assertEqual(Coral.current_amount, 0)
        self.assertEqual(Dino.current_amount, 0)


    def test_closing_before_completion_with_function_next(self):


        """
        Runs test cases where the amount of parsed actions is less than the amount needed, but is closed anyway, using the function next to iterate.
        """


        table = structures.Table([
            Andy := structures.Player('Andy', 10),
            Boa := structures.Player('Boa', 10),
            Coral := structures.Player('Coral', 10),
            Dino := structures.Player('Dino', 10),
        ])

        betting_round = engines.BettingRound('test round', table)
        listener = betting_round.listen()

        # Before states

        self.assertEqual(table.central_pot, 0)
        self.assertEqual(betting_round.lap_counts, 0)
        self.assertEqual(next(listener), Andy)

        # Actions

        self.assertEqual(betting_round.table.stopping_player, Dino)
        Andy.request_action(structures.Action(constants.ACTION_BET, 1))
        self.assertEqual(next(listener), Boa)

        self.assertEqual(betting_round.table.stopping_player, Dino)
        Boa.request_action(structures.Action(constants.ACTION_RAISE, 2))
        self.assertEqual(next(listener), Coral)

        self.assertEqual(betting_round.table.stopping_player, Andy)
        Coral.request_action(structures.Action(constants.ACTION_RAISE, 4))
        self.assertEqual(next(listener), Dino)

        self.assertEqual(betting_round.table.stopping_player, Boa)
        Dino.request_action(structures.Action(constants.ACTION_FOLD))
        self.assertEqual(next(listener), Andy)

        self.assertEqual(betting_round.table.stopping_player, Boa)
        Andy.request_action(structures.Action(constants.ACTION_CALL, 3))
        self.assertEqual(next(listener), Boa)

        # Missing Boa's action
        
        with self.assertRaises(RuntimeError) as context:
            betting_round.close()
        self.assertEqual(context.exception.args[0], messages.msg_betting_round_was_not_completed)
        self.assertEqual(table.central_pot, 0)
        self.assertEqual(table.current_amount, 0)

        self.assertEqual(Andy.current_amount, 0)
        self.assertEqual(Boa.current_amount, 0)
        self.assertEqual(Coral.current_amount, 0)
        self.assertEqual(Dino.current_amount, 0)


    def test_closing_before_completion_with_for_loop(self):


        """
        Runs test cases where the amount of parsed actions is less than the amount needed, but is closed anyway, using a for loop to iterate.
        """


        table = structures.Table([
            Andy := structures.Player('Andy', 10),
            Boa := structures.Player('Boa', 10),
            Coral := structures.Player('Coral', 10),
            Dino := structures.Player('Dino', 10),
        ])

        betting_round = engines.BettingRound('test round', table)

        actions_to_parse = [
            structures.Action(constants.ACTION_BET, 1),
            structures.Action(constants.ACTION_RAISE, 2),
            structures.Action(constants.ACTION_RAISE, 4),
            structures.Action(constants.ACTION_FOLD),
            structures.Action(constants.ACTION_CALL, 3),
            # Missing Boa's action
        ]


        # Before states

        self.assertEqual(table.central_pot, 0)
        self.assertEqual(betting_round.lap_counts, 0)

        # Actions

        for action, player in zip(actions_to_parse, betting_round.listen()):
            player.request_action(action)

        # After states

        with self.assertRaises(RuntimeError) as context:
            betting_round.close()
        self.assertEqual(context.exception.args[0], messages.msg_betting_round_was_not_completed)
        self.assertEqual(table.central_pot, 0)
        self.assertEqual(table.current_amount, 0)

        self.assertEqual(Andy.current_amount, 0)
        self.assertEqual(Boa.current_amount, 0)
        self.assertEqual(Coral.current_amount, 0)
        self.assertEqual(Dino.current_amount, 0)


    def test_unclosed_round_with_function_next(self):


        """
        Runs test cases where the betting round is not closed successfully, using the function next to iterate.
        """


        table = structures.Table([
            Andy := structures.Player('Andy', 10),
            Boa := structures.Player('Boa', 10),
            Coral := structures.Player('Coral', 10),
            Dino := structures.Player('Dino', 10),
        ])

        betting_round = engines.BettingRound('test round', table)
        listener = betting_round.listen()

        # Before states

        self.assertEqual(table.central_pot, 0)
        self.assertEqual(betting_round.lap_counts, 0)
        self.assertEqual(next(listener), Andy)

        # Actions

        self.assertEqual(betting_round.table.stopping_player, Dino)
        Andy.request_action(structures.Action(constants.ACTION_BET, 1))
        self.assertEqual(next(listener), Boa)

        self.assertEqual(betting_round.table.stopping_player, Dino)
        Boa.request_action(structures.Action(constants.ACTION_RAISE, 2))
        self.assertEqual(next(listener), Coral)

        self.assertEqual(betting_round.table.stopping_player, Andy)
        Coral.request_action(structures.Action(constants.ACTION_RAISE, 4))
        self.assertEqual(next(listener), Dino)

        self.assertEqual(betting_round.table.stopping_player, Boa)
        Dino.request_action(structures.Action(constants.ACTION_FOLD))
        self.assertEqual(next(listener), Andy)

        self.assertEqual(betting_round.table.stopping_player, Boa)
        Andy.request_action(structures.Action(constants.ACTION_CALL, 3))
        self.assertEqual(next(listener), Boa)

        self.assertEqual(betting_round.table.stopping_player, Boa)
        Boa.request_action(structures.Action(constants.ACTION_CALL, 2))
        with self.assertRaises(StopIteration) as context:
            next(listener)
        self.assertIsNone(context.exception.value)

        # After states

        self.assertEqual(table.central_pot, 12)
        self.assertEqual(table.current_amount, 4)

        self.assertEqual(Andy.current_amount, 4)
        self.assertEqual(Boa.current_amount, 4)
        self.assertEqual(Coral.current_amount, 4)
        self.assertEqual(Dino.current_amount, 0)


    def test_unclosed_round_with_for_loop(self):


        """
        Runs test cases where the betting round is not closed successfully, using the a for loop to iterate.
        """


        table = structures.Table([
            Andy := structures.Player('Andy', 10),
            Boa := structures.Player('Boa', 10),
            Coral := structures.Player('Coral', 10),
            Dino := structures.Player('Dino', 10),
        ])

        betting_round = engines.BettingRound('test round', table)

        actions_to_parse = [
            structures.Action(constants.ACTION_BET, 1),
            structures.Action(constants.ACTION_RAISE, 2),
            structures.Action(constants.ACTION_RAISE, 4),
            structures.Action(constants.ACTION_FOLD),
            structures.Action(constants.ACTION_CALL, 3),
            structures.Action(constants.ACTION_CALL, 2),
        ]

        # Before states

        self.assertEqual(table.central_pot, 0)
        self.assertEqual(betting_round.lap_counts, 0)

        # Actions

        for action, player in zip(actions_to_parse, betting_round.listen()):
            player.request_action(action)

        # After states

        self.assertEqual(table.central_pot, 0)
        self.assertEqual(table.current_amount, 4)

        self.assertEqual(Andy.current_amount, 4)
        self.assertEqual(Boa.current_amount, 2) # the last action was not actually parsed
        self.assertEqual(Coral.current_amount, 4)
        self.assertEqual(Dino.current_amount, 0)


class TestBettingRoundContextManager(TestCase):


    """
    Run unit tests on BettingRound context manager.
    """


    def test_successful_parses_and_closure_with_function_next(self):


        """
        Runs test cases where the amount of parsed actions is just the amount needed, and the betting round is closed successfully, using the function next to iterate.
        """


        table = structures.Table([
            Andy := structures.Player('Andy', 10),
            Boa := structures.Player('Boa', 10),
            Coral := structures.Player('Coral', 10),
            Dino := structures.Player('Dino', 10),
        ])

        # Before states

        self.assertEqual(table.central_pot, 0)
        self.assertEqual(table.current_amount, 0)

        # Actions

        with engines.BettingRound('test round', table) as betting_round:

            next(betting_round.listen())
            Andy.request_action(structures.Action(constants.ACTION_BET, 1))

            next(betting_round.listen())
            Boa.request_action(structures.Action(constants.ACTION_RAISE, 2))

            next(betting_round.listen())
            Coral.request_action(structures.Action(constants.ACTION_RAISE, 4))

            next(betting_round.listen())
            Dino.request_action(structures.Action(constants.ACTION_FOLD))

            next(betting_round.listen())
            Andy.request_action(structures.Action(constants.ACTION_CALL, 3))

            next(betting_round.listen())
            Boa.request_action(structures.Action(constants.ACTION_CALL, 2))

        # After states

        self.assertEqual(table.central_pot, 12)
        self.assertEqual(table.current_amount, 0)

        self.assertEqual(Andy.current_amount, 0)
        self.assertEqual(Boa.current_amount, 0)
        self.assertEqual(Coral.current_amount, 0)
        self.assertEqual(Dino.current_amount, 0)


    def test_successful_parses_and_closure_with_for_loop(self):


        """
        Runs test cases where the amount of parsed actions is just the amount needed, and the betting round is closed successfully, using a for loop to iterate.
        """


        table = structures.Table([
            Andy := structures.Player('Andy', 10),
            Boa := structures.Player('Boa', 10),
            Coral := structures.Player('Coral', 10),
            Dino := structures.Player('Dino', 10),
        ])

        actions_to_parse = [
            structures.Action(constants.ACTION_BET, 1),
            structures.Action(constants.ACTION_RAISE, 2),
            structures.Action(constants.ACTION_RAISE, 4),
            structures.Action(constants.ACTION_FOLD),
            structures.Action(constants.ACTION_CALL, 3),
            structures.Action(constants.ACTION_CALL, 2),
        ]

        # Before states

        self.assertEqual(table.central_pot, 0)
        self.assertEqual(table.current_amount, 0)

        # Actions

        with engines.BettingRound('test round', table) as betting_round:
            for action, player in zip(actions_to_parse, betting_round.listen()):
                player.request_action(action)

        # After states

        self.assertEqual(table.central_pot, 12)
        self.assertEqual(table.current_amount, 0)

        self.assertEqual(Andy.current_amount, 0)
        self.assertEqual(Boa.current_amount, 0)
        self.assertEqual(Coral.current_amount, 0)
        self.assertEqual(Dino.current_amount, 0)


    def test_parse_less_actions_than_required_with_function_next(self):


        """
        Runs test cases where the amount of parsed actions is less than the amount needed, but is closed anyway, using the function next to iterate.
        """


        table = structures.Table([
            Andy := structures.Player('Andy', 10),
            Boa := structures.Player('Boa', 10),
            Coral := structures.Player('Coral', 10),
            Dino := structures.Player('Dino', 10),
        ])

        # Before states

        self.assertEqual(table.central_pot, 0)
        self.assertEqual(table.current_amount, 0)

        # Actions

        with self.assertRaises(RuntimeError) as context:

            with engines.BettingRound('test round', table) as betting_round:

                next(betting_round.listen())
                Andy.request_action(structures.Action(constants.ACTION_BET, 1))

                next(betting_round.listen())
                Boa.request_action(structures.Action(constants.ACTION_RAISE, 2))

                next(betting_round.listen())
                Coral.request_action(structures.Action(constants.ACTION_RAISE, 4))

                next(betting_round.listen())
                Dino.request_action(structures.Action(constants.ACTION_FOLD))

                next(betting_round.listen())
                Andy.request_action(structures.Action(constants.ACTION_CALL, 3))

                # Missing Boa's action

        # After states

        self.assertEqual(context.exception.args[0], messages.msg_betting_round_was_not_completed)

        self.assertEqual(table.central_pot, 0)
        self.assertEqual(table.current_amount, 0)

        self.assertEqual(Andy.current_amount, 0)
        self.assertEqual(Boa.current_amount, 0)
        self.assertEqual(Coral.current_amount, 0)
        self.assertEqual(Dino.current_amount, 0)


    def test_parse_less_actions_than_required_with_for_loop(self):


        """
        Runs test cases where the amount of parsed actions is less than the amount needed, but is closed anyway, using a for loop to iterate.
        """


        table = structures.Table([
            Andy := structures.Player('Andy', 10),
            Boa := structures.Player('Boa', 10),
            Coral := structures.Player('Coral', 10),
            Dino := structures.Player('Dino', 10),
        ])

        actions_to_parse = [
            structures.Action(constants.ACTION_BET, 1),
            structures.Action(constants.ACTION_RAISE, 2),
            structures.Action(constants.ACTION_RAISE, 4),
            structures.Action(constants.ACTION_FOLD),
            structures.Action(constants.ACTION_CALL, 3),
            # Missing Boa's action
        ]

        # Before states

        self.assertEqual(table.central_pot, 0)
        self.assertEqual(table.current_amount, 0)

        # Actions

        with self.assertRaises(RuntimeError) as context:

            with engines.BettingRound('test round', table) as betting_round:
                for action, player in zip(actions_to_parse, betting_round.listen()):
                    player.request_action(action)

        self.assertEqual(context.exception.args[0], messages.msg_betting_round_was_not_completed)

        # After states

        self.assertEqual(table.central_pot, 0)
        self.assertEqual(table.current_amount, 0)

        self.assertEqual(Andy.current_amount, 0)
        self.assertEqual(Boa.current_amount, 0)
        self.assertEqual(Coral.current_amount, 0)
        self.assertEqual(Dino.current_amount, 0)


    def test_parse_more_actions_than_required_with_function_next(self):


        """
        Runs test cases where the amount of parsed actions is more than the amount needed, using the function next to iterate.
        """


        table = structures.Table([
            Andy := structures.Player('Andy', 10),
            Boa := structures.Player('Boa', 10),
            Coral := structures.Player('Coral', 10),
            Dino := structures.Player('Dino', 10),
        ])

        # Before states

        self.assertEqual(table.central_pot, 0)
        self.assertEqual(table.current_amount, 0)

        # Actions

        with self.assertRaises(RuntimeError) as context:

            with engines.BettingRound('test round', table) as betting_round:

                next(betting_round.listen())
                Andy.request_action(structures.Action(constants.ACTION_BET, 1))

                next(betting_round.listen())
                Boa.request_action(structures.Action(constants.ACTION_RAISE, 2))

                next(betting_round.listen())
                Coral.request_action(structures.Action(constants.ACTION_RAISE, 4))

                next(betting_round.listen())
                Dino.request_action(structures.Action(constants.ACTION_FOLD))

                next(betting_round.listen())
                Andy.request_action(structures.Action(constants.ACTION_CALL, 3))

                next(betting_round.listen())
                Boa.request_action(structures.Action(constants.ACTION_CALL, 2))

                next(betting_round.listen())
                Coral.request_action(structures.Action(constants.ACTION_BET, 4))

        self.assertEqual(context.exception.args[0], messages.msg_overloaded_betting_round_message)

        # After states

        self.assertEqual(table.central_pot, 12)
        self.assertEqual(table.current_amount, 0)

        self.assertEqual(Andy.current_amount, 0)
        self.assertEqual(Boa.current_amount, 0)
        self.assertEqual(Coral.current_amount, 0)
        self.assertEqual(Dino.current_amount, 0)


    def test_parse_more_actions_than_required_with_for_loop(self):


        """
        Runs test cases where the amount of parsed actions is more than the amount needed, using a for loop to iterate.
        """


        table = structures.Table([
            Andy := structures.Player('Andy', 10),
            Boa := structures.Player('Boa', 10),
            Coral := structures.Player('Coral', 10),
            Dino := structures.Player('Dino', 10),
        ])

        actions_to_parse = [
            structures.Action(constants.ACTION_BET, 1),
            structures.Action(constants.ACTION_RAISE, 2),
            structures.Action(constants.ACTION_RAISE, 4),
            structures.Action(constants.ACTION_FOLD),
            structures.Action(constants.ACTION_CALL, 3),
            structures.Action(constants.ACTION_CALL, 2),
            structures.Action(constants.ACTION_BET, 4), ## not parsed because the betting round has already ended
        ]

        # Before states

        self.assertEqual(table.central_pot, 0)
        self.assertEqual(table.current_amount, 0)

        # Actions

        with self.assertRaises(RuntimeError) as context:

            with engines.BettingRound('test round', table) as betting_round:
                for action, player in zip(actions_to_parse, betting_round.listen()):
                    player.request_action(action)
                next(betting_round.listen()) ## try to parse the last action

        self.assertEqual(context.exception.args[0], messages.msg_overloaded_betting_round_message)

        # After states

        self.assertEqual(table.central_pot, 12)
        self.assertEqual(table.current_amount, 0)

        self.assertEqual(Andy.current_amount, 0)
        self.assertEqual(Boa.current_amount, 0)
        self.assertEqual(Coral.current_amount, 0)
        self.assertEqual(Dino.current_amount, 0)


if __name__ == '__main__':
    main()