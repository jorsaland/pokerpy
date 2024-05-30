"""
Defines unit tests on alternate_players function.
"""


import sys
sys.path.insert(0, '.')


from unittest import main, TestCase


import pokerpy as pk


class TestBettingRoundAlternatePlayersFunction(TestCase):


    """
    Runs unit tests on alternate_players function.
    """


    def test_active_players(self):


        """
        Runs test cases to check only active players take action.
        """


        all_players = [
            Andy := pk.Player('Andy'),
            Boa := pk.Player('Boa'),
            Coral := pk.Player('Coral'),
            Dino := pk.Player('Dino'),
            Epa := pk.Player('Epa'),
            Fomi := pk.Player('Fomi'),
        ]


        # All players are active

        def activate_all_players():

            table = pk.Table(all_players)
            table.activate_all_players()

            generator = pk.managers.alternate_players(table)
            awaited_players: list[pk.Player] = []

            player = next(generator) # Andy
            player.request(pk.ACTION_CHECK)
            awaited_players.append(player)

            player = next(generator) # Boa
            player.request(pk.ACTION_CHECK)
            awaited_players.append(player)

            player = next(generator) # Coral
            player.request(pk.ACTION_CHECK)
            awaited_players.append(player)

            player = next(generator) # Dino
            player.request(pk.ACTION_CHECK)
            awaited_players.append(player)

            player = next(generator) # Epa
            player.request(pk.ACTION_CHECK)
            awaited_players.append(player)

            player = next(generator) # Fomi
            player.request(pk.ACTION_CHECK)
            awaited_players.append(player)

            # End iteration
            try:
                next(generator) # No more players
            except StopIteration:
                return awaited_players

        self.assertEqual(activate_all_players(), all_players)


        # No player is active

        def deactivate_all_players():

            table = pk.Table(all_players)

            generator = pk.managers.alternate_players(table)
            awaited_players: list[pk.Player] = []

            # End iteration
            try:
                next(generator) # No more players
            except StopIteration:
                awaited_player_names = [player.name for player in awaited_players]
                return awaited_player_names

        self.assertEqual(deactivate_all_players(), [])


        # Only first player and last player are active

        first_and_last_players = [Andy, Fomi]
        
        def only_activate_first_and_last_player():

            table = pk.Table(all_players)
            for player in first_and_last_players:
                table.activate_player(player)

            generator = pk.managers.alternate_players(table)
            awaited_players: list[pk.Player] = []

            player = next(generator) # Andy
            player.request(pk.ACTION_CHECK)
            awaited_players.append(player)

            player = next(generator) # Fomi
            player.request(pk.ACTION_CHECK)
            awaited_players.append(player)

            # End iteration
            try:
                next(generator) # No more players
            except StopIteration:
                return awaited_players

        self.assertEqual(only_activate_first_and_last_player(), first_and_last_players)


        # All players are active, except for the first one and last one

        all_players_but_first_and_last = [Boa, Coral, Dino, Epa]

        def only_deactivate_first_and_last_player():

            table = pk.Table(all_players)
            for player in all_players_but_first_and_last:
                table.activate_player(player)

            generator = pk.managers.alternate_players(table)
            awaited_players: list[pk.Player] = []

            player = next(generator) # Boa
            player.request(pk.ACTION_CHECK)
            awaited_players.append(player)

            player = next(generator) # Coral
            player.request(pk.ACTION_CHECK)
            awaited_players.append(player)

            player = next(generator) # Dino
            player.request(pk.ACTION_CHECK)
            awaited_players.append(player)

            player = next(generator) # Epa
            player.request(pk.ACTION_CHECK)
            awaited_players.append(player)

            # End iteration
            try:
                next(generator) # No more players
            except StopIteration:
                return awaited_players

        self.assertEqual(only_deactivate_first_and_last_player(), all_players_but_first_and_last)


        # Some interspersed players are active

        interspersed_players = [Andy, Coral, Epa]

        def activate_interspersed_players():

            table = pk.Table(all_players)
            for player in interspersed_players:
                table.activate_player(player)

            generator = pk.managers.alternate_players(table)
            awaited_players: list[pk.Player] = []

            player = next(generator) # Andy
            player.request(pk.ACTION_CHECK)
            awaited_players.append(player)

            player = next(generator) # Coral
            player.request(pk.ACTION_CHECK)
            awaited_players.append(player)

            player = next(generator) # Epa
            player.request(pk.ACTION_CHECK)
            awaited_players.append(player)

            # End iteration
            try:
                next(generator) # No more players
            except StopIteration:
                return awaited_players

        self.assertEqual(activate_interspersed_players(), interspersed_players)


    def test_parsing(self):


        """
        Runs test cases to check actions are correctly parsed into the generator object.
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

            generator = pk.managers.alternate_players(table)
            awaited_players: list[pk.Player] = []

            player = next(generator) # Andy
            player.request(pk.ACTION_CHECK)
            awaited_players.append(player)

            player = next(generator) # Boa
            player.request(pk.ACTION_CHECK)
            awaited_players.append(player)

            player = next(generator) # Coral
            player.request(pk.ACTION_CHECK)
            awaited_players.append(player)

            player = next(generator) # Dino
            player.request(pk.ACTION_CHECK)
            awaited_players.append(player)

            return awaited_players

        self.assertEqual(parse_as_many_actions_as_expected(), all_players)


        def parse_less_actions_than_expected():

            table = pk.Table(all_players)
            table.activate_all_players()

            generator = pk.managers.alternate_players(table)
            awaited_players: list[pk.Player] = []

            player = next(generator) # Andy
            player.request(pk.ACTION_CHECK)
            awaited_players.append(player)

            player = next(generator) # Boa
            player.request(pk.ACTION_CHECK)
            awaited_players.append(player)

            player = next(generator) # Coral
            player.request(pk.ACTION_CHECK)
            awaited_players.append(player)

            # Dino is missing

            return awaited_players

        self.assertEqual(parse_less_actions_than_expected(), [Andy, Boa, Coral])


        def parse_more_actions_than_expected():

            table = pk.Table(all_players)
            table.activate_all_players()
            
            generator = pk.managers.alternate_players(table)
            awaited_players: list[pk.Player] = []

            player = next(generator) # Andy
            player.request(pk.ACTION_CHECK)
            awaited_players.append(player)

            player = next(generator) # Boa
            player.request(pk.ACTION_CHECK)
            awaited_players.append(player)

            player = next(generator) # Coral
            player.request(pk.ACTION_CHECK)
            awaited_players.append(player)

            player = next(generator) # Dino
            player.request(pk.ACTION_CHECK)
            awaited_players.append(player)

            player = next(generator) # Unexpected action
            player.request(pk.ACTION_CHECK)
            awaited_players.append(player)

            return awaited_players

        with self.assertRaises(StopIteration):
            parse_more_actions_than_expected()


    def test_betting_round_must_end_detection(self):


        """
        Runs test cases to check the function correctly detects whether round must stop or not.
        """


        all_players = [
            Andy := pk.Player('Andy'),
            Boa := pk.Player('Boa'),
            Coral := pk.Player('Coral'),
            Dino := pk.Player('Dino'),
        ]


        def end_if_single_player_remaining():

            table = pk.Table(all_players)
            table.activate_player(Andy)
            
            table.become_under_bet()

            generator = pk.managers.alternate_players(table)

            # End iteration and retrieve returned value
            try:
                next(generator) # Andy
            except StopIteration as ex:
                return ex.value

        self.assertTrue(end_if_single_player_remaining())


        def end_if_first_player_is_the_last_aggressive_one():

            table = pk.Table(all_players)
            table.activate_all_players()

            table.set_last_aggressive_player(Andy)
            table.become_under_bet()

            generator = pk.managers.alternate_players(table)

            # End iteration and retrieve returned value
            try:
                next(generator) # Andy
            except StopIteration as ex:
                return ex.value

        self.assertTrue(end_if_first_player_is_the_last_aggressive_one())


        def end_if_intermediate_position_player_is_the_last_aggressive_one():

            table = pk.Table(all_players)
            table.activate_all_players()

            table.set_last_aggressive_player(Coral)
            table.become_under_bet()

            generator = pk.managers.alternate_players(table)

            player = next(generator) # Andy
            player.request(pk.ACTION_CALL)

            player = next(generator) # Boa
            player.request(pk.ACTION_CALL)

            # End iteration and retrieve returned value
            try:
                next(generator) # Coral
            except StopIteration as ex:
                return ex.value

        self.assertTrue(end_if_intermediate_position_player_is_the_last_aggressive_one())


        def end_if_last_player_is_the_last_aggressive_one():

            table = pk.Table(all_players)
            table.activate_all_players()

            table.set_last_aggressive_player(Dino)
            table.become_under_bet()

            generator = pk.managers.alternate_players(table)

            player = next(generator) # Andy
            player.request(pk.ACTION_CALL)

            player = next(generator) # Boa
            player.request(pk.ACTION_CALL)

            player = next(generator) # Coral
            player.request(pk.ACTION_CALL)

            # End iteration and retrieve returned value
            try:
                next(generator) # Dino
            except StopIteration as ex:
                return ex.value

        self.assertTrue(end_if_last_player_is_the_last_aggressive_one())


        def continue_if_round_starts_not_under_bet():

            table = pk.Table(all_players)
            table.activate_all_players()

            generator = pk.managers.alternate_players(table)

            player = next(generator) # Andy
            player.request(pk.ACTION_CHECK)

            player = next(generator) # Boa
            player.request(pk.ACTION_BET)

            player = next(generator) # Coral
            player.request(pk.ACTION_RAISE)

            player = next(generator) # Dino
            player.request(pk.ACTION_CALL)

            # End iteration and retrieve returned value
            try:
                next(generator) # Andy
            except StopIteration as ex:
                return ex.value

        self.assertFalse(continue_if_round_starts_not_under_bet())


if __name__ == '__main__':
    main()