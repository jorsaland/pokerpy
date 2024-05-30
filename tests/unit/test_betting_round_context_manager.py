"""
Defines unit tests on BettingRound class when implemented as a context manager.
"""


import sys
sys.path.insert(0, '.')


from unittest import main, TestCase


import pokerpy as pk


class TestBettingRoundContextManager(TestCase):


    """
    Runs unit tests on BettingRound class when implemented as a context manager.
    """


    def test_instantiation(self):


        """
        Runs test cases on class instantiation.
        """


        table = pk.Table([
            pk.Player('Andy'),
            pk.Player('Boa'),
            pk.Player('Coral'),
            pk.Player('Dino'),
        ])


        # Valid inputs

        pk.BettingRound('round', table)


        # Invalid types

        with self.assertRaises(TypeError) as cm:
            pk.BettingRound(1975, table)
        self.assertEqual(cm.exception.args[0], pk.messages.not_str_betting_round_name_message.format(int.__name__))

        with self.assertRaises(TypeError) as cm:
            pk.BettingRound('round', 1975)
        self.assertEqual(cm.exception.args[0], pk.messages.not_table_instance_message.format(int.__name__))


    def test_exception_catching(self):


        """
        Runs test cases to check if the context manager works as expected.
        """


        all_players = [
            pk.Player('Andy'),
            pk.Player('Boa'),
            pk.Player('Coral'),
            pk.Player('Dino'),
        ]


        # Raising unexpected exception: ValueError

        value_error_message = 'some value error'

        def raise_value_error():
            table = pk.Table(all_players)
            with pk.BettingRound(name='round', table=table):
                raise ValueError(value_error_message)
            
        with self.assertRaises(ValueError) as cm:
            raise_value_error()
        
        self.assertEqual(cm.exception.args[0], value_error_message)


        # Raising unexpected exception: TypeError

        type_error_message = 'some type error'

        def raise_type_error():
            table = pk.Table(all_players)
            with pk.BettingRound(name='round', table=table):
                raise TypeError(type_error_message)
            
        with self.assertRaises(TypeError) as cm:
            raise_type_error()
        
        self.assertEqual(cm.exception.args[0], type_error_message)


        # Raising unexpected parent exception: Exception

        exception_error_message = 'parent exception'

        def raise_parent_exception():
            table = pk.Table(all_players)
            with pk.BettingRound(name='round', table=table):
                raise Exception(exception_error_message)
            
        with self.assertRaises(Exception) as cm:
            raise_parent_exception()
        
        self.assertEqual(cm.exception.args[0], exception_error_message)


        # Breaking round before time: StopIteration

        def raise_stop_iteration():
            table = pk.Table(all_players)
            with pk.BettingRound(name='round', table=table):
                raise StopIteration()
            
        with self.assertRaises(RuntimeError) as cm:
            raise_stop_iteration()

        self.assertEqual(cm.exception.args[0], pk.messages.overloaded_betting_round_message)


    def test_parsing(self):


        """
        Runs test cases to check actions are correctly parsed into the context manager.
        """


        all_players = [
            Andy := pk.Player('Andy'),
            Boa := pk.Player('Boa'),
            Coral := pk.Player('Coral'),
            Dino := pk.Player('Dino'),
        ]


        def parse_as_many_actions_as_expected():

            table = pk.Table(all_players)
            table.activate_all_players()

            awaited_players: list[pk.Player] = []

            with pk.BettingRound(name='round', table=table) as betting_round:

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

            return awaited_players

        self.assertEqual(parse_as_many_actions_as_expected(), all_players)


        def parse_less_actions_than_expected():

            table = pk.Table(all_players)
            table.activate_all_players()

            awaited_players: list[pk.Player] = []

            with pk.BettingRound(name='round', table=table) as betting_round:

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

            return awaited_players

        with self.assertRaises(RuntimeError) as cm:
            parse_less_actions_than_expected()

        self.assertEqual(cm.exception.args[0], pk.messages.exiting_unended_betting_round_message)


        def parse_more_actions_than_expected():

            table = pk.Table(all_players)
            table.activate_all_players()

            awaited_players: list[pk.Player] = []

            with pk.BettingRound(name='round', table=table) as betting_round:

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

            return awaited_players

        with self.assertRaises(RuntimeError) as cm:
            parse_more_actions_than_expected()
        
        self.assertEqual(cm.exception.args[0], pk.messages.overloaded_betting_round_message)


    def test_action_chain(self):


        """
        Runs test cases to check a betting round can correctly chain multiple actions.
        """


        def all_check():

            player_names = ['Andy', 'Boa', 'Coral', 'Dino']
            players = [pk.Player(name) for name in player_names]
            table = pk.Table(players)

            table.activate_all_players()
            awaited_players: list[pk.Player] = []

            with pk.BettingRound(name='round', table=table) as betting_round:

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

            player_names = ['Andy', 'Boa', 'Coral', 'Dino']
            players = [pk.Player(name) for name in player_names]
            table = pk.Table(players)

            table.activate_all_players()
            awaited_players: list[pk.Player] = []

            with pk.BettingRound(name='round', table=table) as betting_round:

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

            player_names = ['Andy', 'Boa', 'Coral', 'Dino']
            players = [pk.Player(name) for name in player_names]
            table = pk.Table(players)

            table.activate_all_players()
            awaited_players: list[pk.Player] = []

            with pk.BettingRound(name='round', table=table) as betting_round:

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

            player_names = ['Andy', 'Boa', 'Coral', 'Dino']
            players = [pk.Player(name) for name in player_names]
            table = pk.Table(players)

            table.activate_all_players()
            awaited_players: list[pk.Player] = []

            with pk.BettingRound(name='round', table=table) as betting_round:

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

            player_names = ['Andy', 'Boa', 'Coral', 'Dino']
            players = [pk.Player(name) for name in player_names]
            table = pk.Table(players)

            table.activate_all_players()
            awaited_players: list[pk.Player] = []

            with pk.BettingRound(name='round', table=table) as betting_round:

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

            player_names = ['Andy', 'Boa', 'Coral', 'Dino']
            players = [pk.Player(name) for name in player_names]
            table = pk.Table(players)

            table.activate_all_players()
            awaited_players: list[pk.Player] = []

            with pk.BettingRound(name='round', table=table) as betting_round:

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