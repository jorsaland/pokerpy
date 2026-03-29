"""
Defines unit tests on set_action_effects function.
"""


import sys
sys.path.insert(0, '.')


from unittest import main, TestCase


from pokerpy import constants, engines, structures


class TestBettingRoundSetActionEffectsFunction(TestCase):


    """
    Runs unit tests on set_action_effects function.
    """


    def test_parse_a_fold(self):

        """
        Runs test cases where a fold is parsed.
        """
        
        table = structures.Table(players = [
            structures.Player('Andy', 10),
            Boa := structures.Player('Boa', 10),
            structures.Player('Coral', 10),
            Dino := structures.Player('Dino', 10),
            structures.Player('Epa', 10),            
        ])
        table.add_to_current_amount(1)

        action = structures.Action(constants.ACTION_FOLD)

        betting_round = engines.BettingRound('test round', table, stopping_player=Dino)

        # States before

        self.assertEqual(Boa.stack, 10)
        self.assertEqual(Boa.current_amount, 0)
        self.assertFalse(Boa.is_folded)

        self.assertEqual(table.current_amount, 1)

        self.assertEqual(betting_round.table.smallest_raise_amount, 1)
        self.assertEqual(betting_round.table.stopping_player, Dino)

        # Run function

        engines.set_action_effects(
            betting_round = betting_round,
            player = Boa,
            action = action,
        )

        # States after

        self.assertEqual(Boa.stack, 10)
        self.assertEqual(Boa.current_amount, 0)
        self.assertTrue(Boa.is_folded)

        self.assertEqual(table.current_amount, 1)

        self.assertEqual(betting_round.table.smallest_raise_amount, 1)
        self.assertEqual(betting_round.table.stopping_player, Dino)


    def test_parse_a_check(self):

        """
        Runs test cases where a check is parsed.
        """
        
        table = structures.Table(players = [
            structures.Player('Andy', 10),
            Boa := structures.Player('Boa', 10),
            structures.Player('Coral', 10),
            Dino := structures.Player('Dino', 10),
            structures.Player('Epa', 10),            
        ])

        action = structures.Action(constants.ACTION_CHECK)

        betting_round = engines.BettingRound('test round', table, stopping_player=Dino)

        # States before

        self.assertEqual(Boa.stack, 10)
        self.assertEqual(Boa.current_amount, 0)
        self.assertFalse(Boa.is_folded)

        self.assertEqual(table.current_amount, 0)

        self.assertEqual(betting_round.table.smallest_raise_amount, 1)
        self.assertEqual(betting_round.table.stopping_player, Dino)

        # Run function

        engines.set_action_effects(
            betting_round = betting_round,
            player = Boa,
            action = action,
        )

        # States after

        self.assertEqual(Boa.stack, 10)
        self.assertEqual(Boa.current_amount, 0)
        self.assertFalse(Boa.is_folded)

        self.assertEqual(table.current_amount, 0)

        self.assertEqual(betting_round.table.smallest_raise_amount, 1)
        self.assertEqual(betting_round.table.stopping_player, Dino)


    def test_parse_a_call_smaller_than_a_full_call(self):

        """
        Runs test cases where a call smaller than a full call is parsed (all-in).
        """
        
        table = structures.Table(players = [
            structures.Player('Andy', 10),
            Boa := structures.Player('Boa', 1),
            structures.Player('Coral', 10),
            Dino := structures.Player('Dino', 10),
            structures.Player('Epa', 10),
        ])
        table.add_to_current_amount(2)

        action = structures.Action(constants.ACTION_CALL, 1)

        betting_round = engines.BettingRound('test round', table, stopping_player=Dino, smallest_bet_amount=2)

        # States before

        self.assertEqual(Boa.stack, 1)
        self.assertEqual(Boa.current_amount, 0)
        self.assertFalse(Boa.is_folded)

        self.assertEqual(table.current_amount, 2)

        self.assertEqual(betting_round.table.smallest_raise_amount, 2)
        self.assertEqual(betting_round.table.stopping_player, Dino)

        # Run function

        engines.set_action_effects(
            betting_round = betting_round,
            player = Boa,
            action = action,
        )

        # States after

        self.assertEqual(Boa.stack, 0)
        self.assertEqual(Boa.current_amount, 1)
        self.assertFalse(Boa.is_folded)

        self.assertEqual(table.current_amount, 2)

        self.assertEqual(betting_round.table.smallest_raise_amount, 2)
        self.assertEqual(betting_round.table.stopping_player, Dino)


    def test_parse_a_call_equal_to_a_full_call(self):

        """
        Runs test cases where a call equal to a full call is parsed.
        """
        
        table = structures.Table(players = [
            structures.Player('Andy', 10),
            Boa := structures.Player('Boa', 10),
            structures.Player('Coral', 10),
            Dino := structures.Player('Dino', 10),
            structures.Player('Epa', 10),
        ])
        table.add_to_current_amount(2)

        action = structures.Action(constants.ACTION_CALL, 2)

        betting_round = engines.BettingRound('test round', table, stopping_player=Dino, smallest_bet_amount=2)

        # States before

        self.assertEqual(Boa.stack, 10)
        self.assertEqual(Boa.current_amount, 0)
        self.assertFalse(Boa.is_folded)

        self.assertEqual(table.current_amount, 2)

        self.assertEqual(betting_round.table.smallest_raise_amount, 2)
        self.assertEqual(betting_round.table.stopping_player, Dino)

        # Run function

        engines.set_action_effects(
            betting_round = betting_round,
            player = Boa,
            action = action,
        )

        # States after

        self.assertEqual(Boa.stack, 8)
        self.assertEqual(Boa.current_amount, 2)
        self.assertFalse(Boa.is_folded)

        self.assertEqual(table.current_amount, 2)

        self.assertEqual(betting_round.table.smallest_raise_amount, 2)
        self.assertEqual(betting_round.table.stopping_player, Dino)


    def test_parse_a_bet_smaller_than_a_full_bet(self):

        """
        Runs test cases where a bet smaller than a full bet is parsed (all-in).
        """

        table = structures.Table(players = [
            Andy := structures.Player('Andy', 10),
            Boa := structures.Player('Boa', 1),
            structures.Player('Coral', 10),
            Dino := structures.Player('Dino', 10),
            structures.Player('Epa', 10),    
        ])

        action = structures.Action(constants.ACTION_BET, 1)

        betting_round = engines.BettingRound('test round', table, stopping_player=Dino, smallest_bet_amount=2)

        # States before

        self.assertEqual(Boa.stack, 1)
        self.assertEqual(Boa.current_amount, 0)
        self.assertFalse(Boa.is_folded)

        self.assertEqual(table.current_amount, 0)

        self.assertEqual(betting_round.table.smallest_raise_amount, 2)
        self.assertEqual(betting_round.table.stopping_player, Dino)

        # Run function

        engines.set_action_effects(
            betting_round = betting_round,
            player = Boa,
            action = action,
        )

        # States after

        self.assertEqual(Boa.stack, 0)
        self.assertEqual(Boa.current_amount, 1)
        self.assertFalse(Boa.is_folded)

        self.assertEqual(table.current_amount, 1)

        self.assertEqual(betting_round.table.smallest_raise_amount, 2)
        self.assertEqual(betting_round.table.stopping_player, Andy)


    def test_parse_a_bet_equal_to_a_full_bet(self):

        """
        Runs test cases where a bet equal to a full bet is parsed.
        """

        table = structures.Table(players = [
            Andy := structures.Player('Andy', 10),
            Boa := structures.Player('Boa', 10),
            structures.Player('Coral', 10),
            Dino := structures.Player('Dino', 10),
            structures.Player('Epa', 10),    
        ])

        action = structures.Action(constants.ACTION_BET, 2)

        betting_round = engines.BettingRound('test round', table, stopping_player=Dino, smallest_bet_amount=2)

        # States before

        self.assertEqual(Boa.stack, 10)
        self.assertEqual(Boa.current_amount, 0)
        self.assertFalse(Boa.is_folded)

        self.assertEqual(table.current_amount, 0)

        self.assertEqual(betting_round.table.smallest_raise_amount, 2)
        self.assertEqual(betting_round.table.stopping_player, Dino)

        # Run function

        engines.set_action_effects(
            betting_round = betting_round,
            player = Boa,
            action = action,
        )

        # States after

        self.assertEqual(Boa.stack, 8)
        self.assertEqual(Boa.current_amount, 2)
        self.assertFalse(Boa.is_folded)

        self.assertEqual(table.current_amount, 2)

        self.assertEqual(betting_round.table.smallest_raise_amount, 2)
        self.assertEqual(betting_round.table.stopping_player, Andy)


    def test_parse_a_bet_larger_than_a_full_bet(self):

        """
        Runs test cases where a bet larger than a full bet is parsed.
        """

        table = structures.Table(players = [
            Andy := structures.Player('Andy', 10),
            Boa := structures.Player('Boa', 10),
            structures.Player('Coral', 10),
            Dino := structures.Player('Dino', 10),
            structures.Player('Epa', 10),    
        ])

        action = structures.Action(constants.ACTION_BET, 3)

        betting_round = engines.BettingRound('test round', table, stopping_player=Dino, smallest_bet_amount=2)

        # States before

        self.assertEqual(Boa.stack, 10)
        self.assertEqual(Boa.current_amount, 0)
        self.assertFalse(Boa.is_folded)

        self.assertEqual(table.current_amount, 0)

        self.assertEqual(betting_round.table.smallest_raise_amount, 2)
        self.assertEqual(betting_round.table.stopping_player, Dino)

        # Run function

        engines.set_action_effects(
            betting_round = betting_round,
            player = Boa,
            action = action,
        )

        # States after

        self.assertEqual(Boa.stack, 7)
        self.assertEqual(Boa.current_amount, 3)
        self.assertFalse(Boa.is_folded)

        self.assertEqual(table.current_amount, 3)

        self.assertEqual(betting_round.table.smallest_raise_amount, 3)
        self.assertEqual(betting_round.table.stopping_player, Andy)


    def test_parse_a_raise_smaller_than_a_full_raise(self):

        """
        Runs test cases where a raise with an amount smaller than a full raise is parsed (all-in).
        """

        table = structures.Table(players = [
            Andy := structures.Player('Andy', 10),
            Boa := structures.Player('Boa', 7),
            structures.Player('Coral', 10),
            Dino := structures.Player('Dino', 10),
            structures.Player('Epa', 10),    
        ])
        table.add_to_current_amount(5)

        action = structures.Action(constants.ACTION_RAISE, 7)

        betting_round = engines.BettingRound('test round', table, stopping_player=Dino, smallest_bet_amount=2)
        betting_round.table.set_smallest_raise_amount(3)

        # States before

        self.assertEqual(Boa.stack, 7)
        self.assertEqual(Boa.current_amount, 0)
        self.assertFalse(Boa.is_folded)

        self.assertEqual(table.current_amount, 5)

        self.assertEqual(betting_round.table.smallest_raise_amount, 3)
        self.assertEqual(betting_round.table.stopping_player, Dino)

        # Run function

        engines.set_action_effects(
            betting_round = betting_round,
            player = Boa,
            action = action,
        )

        # States after

        self.assertEqual(Boa.stack, 0)
        self.assertEqual(Boa.current_amount, 7)
        self.assertFalse(Boa.is_folded)

        self.assertEqual(table.current_amount, 7)

        self.assertEqual(betting_round.table.smallest_raise_amount, 3)
        self.assertEqual(betting_round.table.stopping_player, Andy)


    def test_parse_a_raise_equal_to_a_full_raise(self):

        """
        Runs test cases where a raise with an amount equal to a full raise is parsed.
        """

        table = structures.Table(players = [
            Andy := structures.Player('Andy', 10),
            Boa := structures.Player('Boa', 10),
            structures.Player('Coral', 10),
            Dino := structures.Player('Dino', 10),
            structures.Player('Epa', 10),    
        ])
        table.add_to_current_amount(5)

        action = structures.Action(constants.ACTION_RAISE, 8)

        betting_round = engines.BettingRound('test round', table, stopping_player=Dino, smallest_bet_amount=2)
        betting_round.table.set_smallest_raise_amount(3)

        # States before

        self.assertEqual(Boa.stack, 10)
        self.assertEqual(Boa.current_amount, 0)
        self.assertFalse(Boa.is_folded)

        self.assertEqual(table.current_amount, 5)

        self.assertEqual(betting_round.table.smallest_raise_amount, 3)
        self.assertEqual(betting_round.table.stopping_player, Dino)

        # Run function

        engines.set_action_effects(
            betting_round = betting_round,
            player = Boa,
            action = action,
        )

        # States after

        self.assertEqual(Boa.stack, 2)
        self.assertEqual(Boa.current_amount, 8)
        self.assertFalse(Boa.is_folded)

        self.assertEqual(table.current_amount, 8)

        self.assertEqual(betting_round.table.smallest_raise_amount, 3)
        self.assertEqual(betting_round.table.stopping_player, Andy)


    def test_parse_a_raise_larger_than_a_full_raise(self):

        """
        Runs test cases where a raise with an amount larger than a full raise is parsed.
        """

        table = structures.Table(players = [
            Andy := structures.Player('Andy', 10),
            Boa := structures.Player('Boa', 10),
            structures.Player('Coral', 10),
            Dino := structures.Player('Dino', 10),
            structures.Player('Epa', 10),    
        ])
        table.add_to_current_amount(5)

        action = structures.Action(constants.ACTION_RAISE, 9)

        betting_round = engines.BettingRound('test round', table, stopping_player=Dino, smallest_bet_amount=2)
        betting_round.table.set_smallest_raise_amount(3)

        # States before

        self.assertEqual(Boa.stack, 10)
        self.assertEqual(Boa.current_amount, 0)
        self.assertFalse(Boa.is_folded)

        self.assertEqual(table.current_amount, 5)

        self.assertEqual(betting_round.table.smallest_raise_amount, 3)
        self.assertEqual(betting_round.table.stopping_player, Dino)

        # Run function

        engines.set_action_effects(
            betting_round = betting_round,
            player = Boa,
            action = action,
        )

        # States after

        self.assertEqual(Boa.stack, 1)
        self.assertEqual(Boa.current_amount, 9)
        self.assertFalse(Boa.is_folded)

        self.assertEqual(table.current_amount, 9)

        self.assertEqual(betting_round.table.smallest_raise_amount, 4)
        self.assertEqual(betting_round.table.stopping_player, Andy)


if __name__ == '__main__':
    main()