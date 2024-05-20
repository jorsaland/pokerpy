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


    def test_action_chain(self):


        """
        Runs test cases to check a betting round can correctly chain multiple actions.
        """


        def all_check():

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

        self.assertEqual(all_check(), ['Andy', 'Boa', 'Coral', 'Dino'])


        def bet_and_folds():

            self.table.activate_all_players()
            awaited_players: list[pk.Player] = []

            with pk.BettingRound(name='round', table=self.table) as betting_round:

                player = next(betting_round) # Andy
                player.request(pk.ACTION_BET)
                awaited_players.append(player)

                player = next(betting_round) # Boa, responding to Andy
                player.request(pk.ACTION_FOLD)
                awaited_players.append(player)

                player = next(betting_round) # Coral, responding to Andy
                player.request(pk.ACTION_FOLD)
                awaited_players.append(player)

                player = next(betting_round) # Dino, responding to Andy
                player.request(pk.ACTION_FOLD)
                awaited_players.append(player)

            awaited_player_names = [player.name for player in awaited_players]
            return awaited_player_names

        self.assertEqual(bet_and_folds(), ['Andy', 'Boa', 'Coral', 'Dino'])


        def bet_and_calls():

            self.table.activate_all_players()
            awaited_players: list[pk.Player] = []

            with pk.BettingRound(name='round', table=self.table) as betting_round:

                player = next(betting_round) # Andy
                player.request(pk.ACTION_BET)
                awaited_players.append(player)

                player = next(betting_round) # Boa, responding to Andy
                player.request(pk.ACTION_CALL)
                awaited_players.append(player)

                player = next(betting_round) # Coral, responding to Andy
                player.request(pk.ACTION_CALL)
                awaited_players.append(player)

                player = next(betting_round) # Dino, responding to Andy
                player.request(pk.ACTION_CALL)
                awaited_players.append(player)

            awaited_player_names = [player.name for player in awaited_players]
            return awaited_player_names

        self.assertEqual(bet_and_calls(), ['Andy', 'Boa', 'Coral', 'Dino'])


        def bet_raises_and_folds():

            self.table.activate_all_players()
            awaited_players: list[pk.Player] = []

            with pk.BettingRound(name='round', table=self.table) as betting_round:

                player = next(betting_round) # Andy
                player.request(pk.ACTION_BET)
                awaited_players.append(player)

                player = next(betting_round) # Boa, responding to Andy
                player.request(pk.ACTION_RAISE)
                awaited_players.append(player)

                player = next(betting_round) # Coral, responding to Boa
                player.request(pk.ACTION_FOLD)
                awaited_players.append(player)

                player = next(betting_round) # Dino, responding to Boa
                player.request(pk.ACTION_RAISE)
                awaited_players.append(player)

                player = next(betting_round) # Andy, responding to Dino
                player.request(pk.ACTION_FOLD)
                awaited_players.append(player)

                player = next(betting_round) # Boa, responding to Dino
                player.request(pk.ACTION_RAISE)
                awaited_players.append(player)

                # Coral already folded

                player = next(betting_round) # Dino, responding to Boa
                player.request(pk.ACTION_FOLD)
                awaited_players.append(player)

                # Andy already folded

                # Boa is the only remaining player

            awaited_player_names = [player.name for player in awaited_players]
            return awaited_player_names

        self.assertEqual(bet_raises_and_folds(), ['Andy', 'Boa', 'Coral', 'Dino', 'Andy', 'Boa', 'Dino'])


        def bet_raises_and_calls():

            self.table.activate_all_players()
            awaited_players: list[pk.Player] = []

            with pk.BettingRound(name='round', table=self.table) as betting_round:

                player = next(betting_round) # Andy
                player.request(pk.ACTION_BET)
                awaited_players.append(player)

                player = next(betting_round) # Boa, responding to Andy
                player.request(pk.ACTION_RAISE)
                awaited_players.append(player)

                player = next(betting_round) # Coral, responding to Boa
                player.request(pk.ACTION_CALL)
                awaited_players.append(player)

                player = next(betting_round) # Dino, responding to Boa
                player.request(pk.ACTION_RAISE)
                awaited_players.append(player)

                player = next(betting_round) # Andy, responding to Dino
                player.request(pk.ACTION_CALL)
                awaited_players.append(player)

                player = next(betting_round) # Boa, responding to Dino
                player.request(pk.ACTION_RAISE)
                awaited_players.append(player)

                player = next(betting_round) # Coral, responding to Boa
                player.request(pk.ACTION_CALL)
                awaited_players.append(player)

                player = next(betting_round) # Dino, responding to Boa
                player.request(pk.ACTION_CALL)
                awaited_players.append(player)

                player = next(betting_round) # Andy, responding to Boa
                player.request(pk.ACTION_CALL)
                awaited_players.append(player)

                # Every player has responded to Boa

            awaited_player_names = [player.name for player in awaited_players]
            return awaited_player_names

        self.assertEqual(bet_raises_and_calls(), ['Andy', 'Boa', 'Coral', 'Dino', 'Andy', 'Boa', 'Coral', 'Dino', 'Andy'])


        def bet_raises_folds_and_calls():

            self.table.activate_all_players()
            awaited_players: list[pk.Player] = []

            with pk.BettingRound(name='round', table=self.table) as betting_round:

                player = next(betting_round) # Andy
                player.request(pk.ACTION_BET)
                awaited_players.append(player)

                player = next(betting_round) # Boa, responding to Andy
                player.request(pk.ACTION_RAISE)
                awaited_players.append(player)

                player = next(betting_round) # Coral, responding to Boa
                player.request(pk.ACTION_FOLD)
                awaited_players.append(player)

                player = next(betting_round) # Dino, responding to Boa
                player.request(pk.ACTION_RAISE)
                awaited_players.append(player)

                player = next(betting_round) # Andy, responding to Dino
                player.request(pk.ACTION_CALL)
                awaited_players.append(player)

                player = next(betting_round) # Boa, responding to Dino
                player.request(pk.ACTION_RAISE)
                awaited_players.append(player)

                # Coral already folded
                
                player = next(betting_round) # Dino, responding to Boa
                player.request(pk.ACTION_FOLD)
                awaited_players.append(player)

                player = next(betting_round) # Andy, responding to Boa
                player.request(pk.ACTION_CALL)
                awaited_players.append(player)

                # Every remaining player has responded to Boa

            awaited_player_names = [player.name for player in awaited_players]
            return awaited_player_names

        self.assertEqual(bet_raises_folds_and_calls(), ['Andy', 'Boa', 'Coral', 'Dino', 'Andy', 'Boa', 'Dino', 'Andy'])


if __name__ == '__main__':
    main()