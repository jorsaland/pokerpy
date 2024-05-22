"""
Runs unit tests on managers section.
"""


import sys
sys.path.insert(0, '.')


from unittest import main, TestCase


import pokerpy as pk


class TestBettingRound(TestCase):


    """
    Runs unit tests on class BettingRound.
    """


    # Resources


    player_names = ['Andy', 'Boa', 'Coral', 'Dino']
    players = [pk.Player(name) for name in player_names]
    table = pk.Table(players)


    def test_iterator_object(self):


        """
        Runs test cases to check if the context manager opens an iterator object.
        """


        def run_iterator_on_for_loop():

            self.table.activate_all_players()
            awaited_players: list[pk.Player] = []

            with pk.BettingRound(name='round', table=self.table) as betting_round:

                for player in betting_round:
                    player.request(pk.ACTION_CHECK)
                    awaited_players.append(player)

            awaited_player_names = [player.name for player in awaited_players]
            return awaited_player_names

        self.assertEqual(run_iterator_on_for_loop(), ['Andy', 'Boa', 'Coral', 'Dino'])


        def run_iterator_on_next_function():

            self.table.activate_all_players()
            awaited_players: list[pk.Player] = []

            with pk.BettingRound(name='round', table=self.table) as betting_round:

                player = next(betting_round) # Andy
                player.request(pk.ACTION_CHECK)
                awaited_players.append(player)

                player = next(betting_round) # Boa
                player.request(pk.ACTION_CHECK)
                awaited_players.append(player)

                player = next(betting_round) # Coral
                player.request(pk.ACTION_CHECK)
                awaited_players.append(player)

                player = next(betting_round) # Dino
                player.request(pk.ACTION_CHECK)
                awaited_players.append(player)

            awaited_player_names = [player.name for player in awaited_players]
            return awaited_player_names

        self.assertEqual(run_iterator_on_next_function(), ['Andy', 'Boa', 'Coral', 'Dino'])


    def test_parsing(self):


        """
        Runs test cases to check actions are correctly parsed into the context manager.
        """


        def parse_as_many_actions_as_expected():

            self.table.activate_all_players()
            awaited_players: list[pk.Player] = []

            with pk.BettingRound(name='round', table=self.table) as betting_round:

                player = next(betting_round) # Andy
                player.request(pk.ACTION_CHECK)
                awaited_players.append(player)

                player = next(betting_round) # Boa
                player.request(pk.ACTION_CHECK)
                awaited_players.append(player)

                player = next(betting_round) # Coral
                player.request(pk.ACTION_CHECK)
                awaited_players.append(player)

                player = next(betting_round) # Dino
                player.request(pk.ACTION_CHECK)
                awaited_players.append(player)

            awaited_player_names = [player.name for player in awaited_players]
            return awaited_player_names

        self.assertEqual(parse_as_many_actions_as_expected(), ['Andy', 'Boa', 'Coral', 'Dino'])


        def parse_less_actions_than_expected():

            self.table.activate_all_players()
            awaited_players: list[pk.Player] = []

            with pk.BettingRound(name='round', table=self.table) as betting_round:

                player = next(betting_round) # Andy
                player.request(pk.ACTION_CHECK)
                awaited_players.append(player)

                player = next(betting_round) # Boa
                player.request(pk.ACTION_CHECK)
                awaited_players.append(player)

                player = next(betting_round) # Coral
                player.request(pk.ACTION_CHECK)
                awaited_players.append(player)

                # Dino is missing

            awaited_player_names = [player.name for player in awaited_players]
            print(f'{awaited_player_names = }')
            return awaited_player_names

        with self.assertRaises(RuntimeError) as cm:
            parse_less_actions_than_expected()
        self.assertEqual(cm.exception.args[0], pk.messages.exiting_unended_betting_round_message)


        def parse_more_actions_than_expected():

            self.table.activate_all_players()
            awaited_players: list[pk.Player] = []

            with pk.BettingRound(name='round', table=self.table) as betting_round:

                player = next(betting_round) # Andy
                player.request(pk.ACTION_CHECK)
                awaited_players.append(player)

                player = next(betting_round) # Boa
                player.request(pk.ACTION_CHECK)
                awaited_players.append(player)

                player = next(betting_round) # Coral
                player.request(pk.ACTION_CHECK)
                awaited_players.append(player)

                player = next(betting_round) # Dino
                player.request(pk.ACTION_CHECK)
                awaited_players.append(player)

                player = next(betting_round) # Unexpected action
                player.request(pk.ACTION_CHECK)
                awaited_players.append(player)

            awaited_player_names = [player.name for player in awaited_players]
            print(f'{awaited_player_names = }')
            return awaited_player_names

        with self.assertRaises(RuntimeError) as cm:
            parse_more_actions_than_expected()
        self.assertEqual(cm.exception.args[0], pk.messages.overloaded_betting_round_message)


class TestActionIsValid(TestCase):


    """
    Runs unit tests on function action_is_valid.
    """


    def test_unexpected_action(self):

        """
        Runs test cases where non-defined actions are parsed.
        """

        with self.assertRaises(ValueError):
            pk.action_is_valid(action='drinks', is_under_bet=True)
        with self.assertRaises(ValueError):
            pk.action_is_valid(action='drinks', is_under_bet=False)


    def test_actions_under_bet(self):

        """
        Runs test cases where a betting round is under bet.
        """

        # Valid actions under bet
        self.assertTrue(pk.action_is_valid(action=pk.ACTION_FOLD, is_under_bet=True))
        self.assertTrue(pk.action_is_valid(action=pk.ACTION_CALL, is_under_bet=True))
        self.assertTrue(pk.action_is_valid(action=pk.ACTION_RAISE, is_under_bet=True))

        # Invalid actions under bet
        self.assertFalse(pk.action_is_valid(action=pk.ACTION_CHECK, is_under_bet=True))
        self.assertFalse(pk.action_is_valid(action=pk.ACTION_BET, is_under_bet=True))


    def test_actions_under_no_bet(self):

        """
        Runs test cases where a betting round is not under bet.
        """

        pk.switches.ONLY_ALLOW_FOLDING_UNDER_BET = True

        # Valid actions under no bet, folding forbidden
        self.assertTrue(pk.action_is_valid(action=pk.ACTION_CHECK, is_under_bet=False))
        self.assertTrue(pk.action_is_valid(action=pk.ACTION_BET, is_under_bet=False))

        # Valid actions under no bet, folding forbidden
        self.assertFalse(pk.action_is_valid(action=pk.ACTION_FOLD, is_under_bet=False))
        self.assertFalse(pk.action_is_valid(action=pk.ACTION_CALL, is_under_bet=False))
        self.assertFalse(pk.action_is_valid(action=pk.ACTION_RAISE, is_under_bet=False))

        pk.switches.ONLY_ALLOW_FOLDING_UNDER_BET = False

        # Valid actions under no bet, folding allowed
        self.assertTrue(pk.action_is_valid(action=pk.ACTION_CHECK, is_under_bet=False))
        self.assertTrue(pk.action_is_valid(action=pk.ACTION_BET, is_under_bet=False))
        self.assertTrue(pk.action_is_valid(action=pk.ACTION_FOLD, is_under_bet=False))

        # Valid actions under no bet, folding allowed
        self.assertFalse(pk.action_is_valid(action=pk.ACTION_CALL, is_under_bet=False))
        self.assertFalse(pk.action_is_valid(action=pk.ACTION_RAISE, is_under_bet=False))


if __name__ == '__main__':
    main()