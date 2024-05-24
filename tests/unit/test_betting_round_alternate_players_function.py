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


        def reset_cycle_states():

            player_names = ['Andy', 'Boa', 'Coral', 'Dino', 'Epa', 'Fomi']
            player_by_name = {name: pk.Player(name) for name in player_names}
            table = pk.Table(player_by_name.values())

            table.reset_cycle_states()
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
                awaited_player_names = [player.name for player in awaited_players]
                return awaited_player_names

        self.assertEqual(reset_cycle_states(), ['Andy', 'Boa', 'Coral', 'Dino', 'Epa', 'Fomi'])


        def dereset_cycle_states():

            player_names = ['Andy', 'Boa', 'Coral', 'Dino', 'Epa', 'Fomi']
            player_by_name = {name: pk.Player(name) for name in player_names}
            table = pk.Table(player_by_name.values())

            generator = pk.managers.alternate_players(table)
            awaited_players: list[pk.Player] = []

            # End iteration
            try:
                next(generator) # No more players
            except StopIteration:
                awaited_player_names = [player.name for player in awaited_players]
                return awaited_player_names

        self.assertEqual(dereset_cycle_states(), [])


        def only_activate_first_and_last_player():

            player_names = ['Andy', 'Boa', 'Coral', 'Dino', 'Epa', 'Fomi']
            player_by_name = {name: pk.Player(name) for name in player_names}
            table = pk.Table(player_by_name.values())

            active_player_names = ['Andy', 'Fomi']
            table.active_players.clear()
            table.active_players.extend([player for name, player in player_by_name.items() if name in active_player_names])

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
                awaited_player_names = [player.name for player in awaited_players]
                return awaited_player_names

        self.assertEqual(only_activate_first_and_last_player(), ['Andy', 'Fomi'])


        def only_deactivate_first_and_last_player():

            player_names = ['Andy', 'Boa', 'Coral', 'Dino', 'Epa', 'Fomi']
            player_by_name = {name: pk.Player(name) for name in player_names}
            table = pk.Table(player_by_name.values())

            active_player_names = ['Boa', 'Coral', 'Dino', 'Epa']
            table.active_players.clear()
            table.active_players.extend([player for name, player in player_by_name.items() if name in active_player_names])

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
                awaited_player_names = [player.name for player in awaited_players]
                return awaited_player_names

        self.assertEqual(only_deactivate_first_and_last_player(), ['Boa', 'Coral', 'Dino', 'Epa'])


        def activate_interspersed_players():

            player_names = ['Andy', 'Boa', 'Coral', 'Dino', 'Epa', 'Fomi']
            player_by_name = {name: pk.Player(name) for name in player_names}
            table = pk.Table(player_by_name.values())

            active_player_names = ['Andy', 'Coral', 'Epa']
            table.active_players.clear()
            table.active_players.extend([player for name, player in player_by_name.items() if name in active_player_names])

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
                awaited_player_names = [player.name for player in awaited_players]
                return awaited_player_names

        self.assertEqual(activate_interspersed_players(), ['Andy', 'Coral', 'Epa'])


    def test_parsing(self):


        """
        Runs test cases to check actions are correctly parsed into the generator object.
        """


        def parse_as_many_actions_as_expected():

            player_names = ['Andy', 'Boa', 'Coral', 'Dino']
            players = [pk.Player(name) for name in player_names]
            table = pk.Table(players)

            table.reset_cycle_states()
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

            awaited_player_names = [player.name for player in awaited_players]
            return awaited_player_names

        self.assertEqual(parse_as_many_actions_as_expected(), ['Andy', 'Boa', 'Coral', 'Dino'])


        def parse_less_actions_than_expected():

            player_names = ['Andy', 'Boa', 'Coral', 'Dino']
            players = [pk.Player(name) for name in player_names]
            table = pk.Table(players)

            table.reset_cycle_states()
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

            awaited_player_names = [player.name for player in awaited_players]
            return awaited_player_names

        self.assertEqual(parse_less_actions_than_expected(), ['Andy', 'Boa', 'Coral'])


        def parse_more_actions_than_expected():

            player_names = ['Andy', 'Boa', 'Coral', 'Dino']
            players = [pk.Player(name) for name in player_names]
            table = pk.Table(players)

            table.reset_cycle_states()
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

            awaited_player_names = [player.name for player in awaited_players]
            print(f'{awaited_player_names = }')
            return awaited_player_names

        with self.assertRaises(StopIteration):
            parse_more_actions_than_expected()


    def test_betting_round_must_end_detection(self):


        """
        Runs test cases to check the function correctly detects whether round must stop or not.
        """


        def end_if_single_player_remaining():

            player_names = ['Andy', 'Boa', 'Coral', 'Dino']
            players = [pk.Player(name) for name in player_names]
            table = pk.Table(players)

            table.active_players.clear()
            table.active_players.append(players[0])
            table.is_under_bet = True

            generator = pk.managers.alternate_players(table)

            # End iteration and retrieve returned value
            try:
                next(generator) # Andy
            except StopIteration as ex:
                return ex.value

        self.assertTrue(end_if_single_player_remaining())


        def end_if_first_player_is_the_last_aggressive_one():

            player_names = ['Andy', 'Boa', 'Coral', 'Dino']
            players = [pk.Player(name) for name in player_names]
            table = pk.Table(players)

            table.reset_cycle_states()
            table.last_aggressive_player = players[0]
            table.is_under_bet = True

            generator = pk.managers.alternate_players(table)

            # End iteration and retrieve returned value
            try:
                next(generator) # Andy
            except StopIteration as ex:
                return ex.value

        self.assertTrue(end_if_first_player_is_the_last_aggressive_one())


        def end_if_intermediate_position_player_is_the_last_aggressive_one():

            player_names = ['Andy', 'Boa', 'Coral', 'Dino']
            players = [pk.Player(name) for name in player_names]
            table = pk.Table(players)

            table.reset_cycle_states()
            table.last_aggressive_player = players[2]
            table.is_under_bet = True

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

            player_names = ['Andy', 'Boa', 'Coral', 'Dino']
            players = [pk.Player(name) for name in player_names]
            table = pk.Table(players)

            table.reset_cycle_states()
            table.last_aggressive_player = players[-1]
            table.is_under_bet = True

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

            player_names = ['Andy', 'Boa', 'Coral', 'Dino']
            players = [pk.Player(name) for name in player_names]
            table = pk.Table(players)

            table.reset_cycle_states()

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