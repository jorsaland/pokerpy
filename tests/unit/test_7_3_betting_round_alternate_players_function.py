"""
Defines unit tests on alternate_players function.
"""


import sys
sys.path.insert(0, '.')


from unittest import main, TestCase


from pokerpy import constants, managers, structures


class TestBettingRoundAlternatePlayersFunction(TestCase):


    """
    Runs unit tests on alternate_players function.
    """


    def test_active_players(self):


        """
        Runs test cases to check only active players take action.
        """


        all_players = [
            Andy := structures.Player('Andy'),
            Boa := structures.Player('Boa'),
            Coral := structures.Player('Coral'),
            Dino := structures.Player('Dino'),
            Epa := structures.Player('Epa'),
            Fomi := structures.Player('Fomi'),
        ]


        # All players are active

        def activate_all_players():

            table = structures.Table(all_players)
            table.reset_cycle_states()

            generator = managers.alternate_players(table=table, ignore_invalid_actions=False)
            awaited_players: list[structures.Player] = []

            player = next(generator) # Andy
            player.request_action(structures.Action(constants.ACTION_CHECK))
            awaited_players.append(player)

            player = next(generator) # Boa
            player.request_action(structures.Action(constants.ACTION_CHECK))
            awaited_players.append(player)

            player = next(generator) # Coral
            player.request_action(structures.Action(constants.ACTION_CHECK))
            awaited_players.append(player)

            player = next(generator) # Dino
            player.request_action(structures.Action(constants.ACTION_CHECK))
            awaited_players.append(player)

            player = next(generator) # Epa
            player.request_action(structures.Action(constants.ACTION_CHECK))
            awaited_players.append(player)

            player = next(generator) # Fomi
            player.request_action(structures.Action(constants.ACTION_CHECK))
            awaited_players.append(player)

            # End iteration
            try:
                next(generator) # No more players
            except StopIteration:
                return awaited_players

        self.assertListEqual(activate_all_players(), all_players)


        # No player is active

        def deactivate_all_players():

            table = structures.Table(all_players)

            generator = managers.alternate_players(table=table, ignore_invalid_actions=False)
            awaited_players: list[structures.Player] = []

            # End iteration
            try:
                next(generator) # No more players
            except StopIteration:
                return awaited_players

        self.assertListEqual(deactivate_all_players(), [])


        # Only first player and last player are active

        first_and_last_players = [Andy, Fomi]
        
        def only_activate_first_and_last_player():

            table = structures.Table(all_players)
            for player in first_and_last_players:
                table.activate_player(player)

            generator = managers.alternate_players(table=table, ignore_invalid_actions=False)
            awaited_players: list[structures.Player] = []

            player = next(generator) # Andy
            player.request_action(structures.Action(constants.ACTION_CHECK))
            awaited_players.append(player)

            player = next(generator) # Fomi
            player.request_action(structures.Action(constants.ACTION_CHECK))
            awaited_players.append(player)

            # End iteration
            try:
                next(generator) # No more players
            except StopIteration:
                return awaited_players

        self.assertEqual(only_activate_first_and_last_player(), first_and_last_players)


        # All players are active, except for the first one and last one

        all_players_but_first_and_last = [Boa, Coral, Dino, Epa]

        def activate_all_but_first_and_last_player():

            table = structures.Table(all_players)
            for player in all_players_but_first_and_last:
                table.activate_player(player)

            generator = managers.alternate_players(table=table, ignore_invalid_actions=False)
            awaited_players: list[structures.Player] = []

            player = next(generator) # Boa
            player.request_action(structures.Action(constants.ACTION_CHECK))
            awaited_players.append(player)

            player = next(generator) # Coral
            player.request_action(structures.Action(constants.ACTION_CHECK))
            awaited_players.append(player)

            player = next(generator) # Dino
            player.request_action(structures.Action(constants.ACTION_CHECK))
            awaited_players.append(player)

            player = next(generator) # Epa
            player.request_action(structures.Action(constants.ACTION_CHECK))
            awaited_players.append(player)

            # End iteration
            try:
                next(generator) # No more players
            except StopIteration:
                return awaited_players

        self.assertEqual(activate_all_but_first_and_last_player(), all_players_but_first_and_last)


        # Some interspersed players are active

        interspersed_players = [Andy, Coral, Epa]

        def activate_interspersed_players():

            table = structures.Table(all_players)
            for player in interspersed_players:
                table.activate_player(player)

            generator = managers.alternate_players(table=table, ignore_invalid_actions=False)
            awaited_players: list[structures.Player] = []

            player = next(generator) # Andy
            player.request_action(structures.Action(constants.ACTION_CHECK))
            awaited_players.append(player)

            player = next(generator) # Coral
            player.request_action(structures.Action(constants.ACTION_CHECK))
            awaited_players.append(player)

            player = next(generator) # Epa
            player.request_action(structures.Action(constants.ACTION_CHECK))
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
            Andy := structures.Player('Andy'),
            Boa := structures.Player('Boa'),
            Coral := structures.Player('Coral'),
            Dino := structures.Player('Dino'),
        ]


        def parse_as_many_actions_as_expected():

            table = structures.Table(all_players)
            table.reset_cycle_states()

            generator = managers.alternate_players(table=table, ignore_invalid_actions=False)
            awaited_players: list[structures.Player] = []

            player = next(generator) # Andy
            player.request_action(structures.Action(constants.ACTION_CHECK))
            awaited_players.append(player)

            player = next(generator) # Boa
            player.request_action(structures.Action(constants.ACTION_CHECK))
            awaited_players.append(player)

            player = next(generator) # Coral
            player.request_action(structures.Action(constants.ACTION_CHECK))
            awaited_players.append(player)

            player = next(generator) # Dino
            player.request_action(structures.Action(constants.ACTION_CHECK))
            awaited_players.append(player)

            return awaited_players

        self.assertEqual(parse_as_many_actions_as_expected(), all_players)


        def parse_less_actions_than_expected():

            table = structures.Table(all_players)
            table.reset_cycle_states()

            generator = managers.alternate_players(table=table, ignore_invalid_actions=False)
            awaited_players: list[structures.Player] = []

            player = next(generator) # Andy
            player.request_action(structures.Action(constants.ACTION_CHECK))
            awaited_players.append(player)

            player = next(generator) # Boa
            player.request_action(structures.Action(constants.ACTION_CHECK))
            awaited_players.append(player)

            player = next(generator) # Coral
            player.request_action(structures.Action(constants.ACTION_CHECK))
            awaited_players.append(player)

            # Dino is missing

            return awaited_players

        self.assertEqual(parse_less_actions_than_expected(), [Andy, Boa, Coral])


        def parse_more_actions_than_expected():

            table = structures.Table(all_players)
            table.reset_cycle_states()
            
            generator = managers.alternate_players(table=table, ignore_invalid_actions=False)
            awaited_players: list[structures.Player] = []

            player = next(generator) # Andy
            player.request_action(structures.Action(constants.ACTION_CHECK))
            awaited_players.append(player)

            player = next(generator) # Boa
            player.request_action(structures.Action(constants.ACTION_CHECK))
            awaited_players.append(player)

            player = next(generator) # Coral
            player.request_action(structures.Action(constants.ACTION_CHECK))
            awaited_players.append(player)

            player = next(generator) # Dino
            player.request_action(structures.Action(constants.ACTION_CHECK))
            awaited_players.append(player)

            player = next(generator) # Unexpected action
            player.request_action(structures.Action(constants.ACTION_CHECK))
            awaited_players.append(player)

            return awaited_players

        with self.assertRaises(StopIteration):
            parse_more_actions_than_expected()


    def test_betting_round_must_end_detection(self):


        """
        Runs test cases to check the function correctly detects whether round must stop or not.
        """


        all_players = [
            Andy := structures.Player('Andy'),
            Boa := structures.Player('Boa'),
            Coral := structures.Player('Coral'),
            Dino := structures.Player('Dino'),
        ]


        def end_if_single_player_remaining():

            table = structures.Table(all_players)
            table.activate_player(Andy)
            
            table.add_to_current_amount(100)

            generator = managers.alternate_players(table=table, ignore_invalid_actions=False)

            # End iteration and retrieve returned value
            try:
                next(generator) # Andy
            except StopIteration as ex:
                return ex.value

        self.assertTrue(end_if_single_player_remaining())


        def end_if_first_player_is_the_stopping_player():

            table = structures.Table(all_players)
            table.reset_cycle_states()

            table.set_stopping_player(Andy)
            table.add_to_current_amount(100)

            generator = managers.alternate_players(table=table, ignore_invalid_actions=False)

            player = next(generator) # Andy
            self.assertEqual(player, Andy)
            player.request_action(structures.Action(constants.ACTION_CALL, 100))

            # End iteration and retrieve returned value
            try:
                next(generator) # Boa (should not be reached)
            except StopIteration as ex:
                return ex.value

        self.assertTrue(end_if_first_player_is_the_stopping_player())


        def end_if_intermediate_position_player_is_the_stopping_player():

            table = structures.Table(all_players)
            table.reset_cycle_states()

            table.set_stopping_player(Boa)
            table.add_to_current_amount(100)

            generator = managers.alternate_players(table=table, ignore_invalid_actions=False)

            player = next(generator) # Andy
            self.assertEqual(player, Andy)
            player.request_action(structures.Action(constants.ACTION_CALL, 100))

            player = next(generator) # Boa
            self.assertEqual(player, Boa)
            player.request_action(structures.Action(constants.ACTION_CALL, 100))

            # End iteration and retrieve returned value
            try:
                next(generator) # Coral (should not be reached)
            except StopIteration as ex:
                return ex.value

        self.assertTrue(end_if_intermediate_position_player_is_the_stopping_player())


        def end_if_last_player_is_the_stopping_player():

            table = structures.Table(all_players)
            table.reset_cycle_states()

            table.set_stopping_player(Dino)
            table.add_to_current_amount(100)

            generator = managers.alternate_players(table=table, ignore_invalid_actions=False)

            player = next(generator) # Andy
            player.request_action(structures.Action(constants.ACTION_CALL, 100))

            player = next(generator) # Boa
            player.request_action(structures.Action(constants.ACTION_CALL, 100))

            player = next(generator) # Coral
            player.request_action(structures.Action(constants.ACTION_CALL, 100))

            player = next(generator) # Dino
            player.request_action(structures.Action(constants.ACTION_CALL, 100))

            # End iteration and retrieve returned value
            try:
                next(generator) # Andy (should not be reached)
            except StopIteration as ex:
                return ex.value

        self.assertTrue(end_if_last_player_is_the_stopping_player())


if __name__ == '__main__':
    main()