"""
Defines unit tests on wait_for_player function.
"""


import sys
sys.path.insert(0, '.')


from unittest import main, TestCase


from pokerpy import constants, managers, structures


class TestBettingRoundWaitForPlayerFunction(TestCase):


    """
    Runs unit tests on wait_for_player function.
    """


    def test_under_bet_parsing(self):


        """
        Runs test cases to check actions are correctly parsed into the generator object when round is under bet.
        """


        valid_action = structures.Action(constants.ACTION_CALL, 100)
        def parse_single_valid_action():
        
            # Define table and current player
            all_players = [
                Andy := structures.Player('Andy'),
                structures.Player('Boa'),
                structures.Player('Coral'),
                structures.Player('Dino'),
            ]
            table = structures.Table(all_players)

            # Make the table to have an amount to be answered
            table.add_to_current_amount(100)

            # Request action
            generator = managers.wait_for_player(player=Andy, table=table, ignore_invalid_actions=True)
            player = next(generator)
            player.request_action(valid_action)

            # End iteration and retrieve returned value
            try:
                next(generator)
            except StopIteration as ex:
                return ex.value

        self.assertEqual(parse_single_valid_action(), valid_action)


        def parse_single_invalid_action():

            # Define table and current player
            all_players = [
                Andy := structures.Player('Andy'),
                structures.Player('Boa'),
                structures.Player('Coral'),
                structures.Player('Dino'),
            ]
            table = structures.Table(all_players)

            # Make the table to have an amount to be answered
            table.add_to_current_amount(100)

            # Request action
            generator = managers.wait_for_player(player=Andy, table=table, ignore_invalid_actions=True)
            player = next(generator)
            player.request_action(structures.Action(constants.ACTION_CHECK))

            # End iteration and retrieve returned value
            try:
                next(generator)
            except StopIteration as ex:
                return ex.value

        self.assertIsNone(parse_single_invalid_action())


        def parse_multiple_invalid_actions():

            # Define table and current player
            all_players = [
                Andy := structures.Player('Andy'),
                structures.Player('Boa'),
                structures.Player('Coral'),
                structures.Player('Dino'),
            ]
            table = structures.Table(all_players)

            # Make the table to have an amount to be answered
            table.add_to_current_amount(100)

            # Request action
            generator = managers.wait_for_player(player=Andy, table=table, ignore_invalid_actions=True)
            player = next(generator)
            player.request_action(structures.Action(constants.ACTION_CHECK))
            player = next(generator)
            player.request_action(structures.Action(constants.ACTION_BET, 100))
            player = next(generator)
            player.request_action(structures.Action(constants.ACTION_CHECK))
            player = next(generator)
            player.request_action(structures.Action(constants.ACTION_BET, 200))

            # End iteration and retrieve returned value
            try:
                next(generator)
            except StopIteration as ex:
                return ex.value

        self.assertIsNone(parse_multiple_invalid_actions())       


        valid_action = structures.Action(constants.ACTION_CALL, 100)
        def parse_multiple_invalid_actions_and_final_valid_action():

            # Define table and current player
            all_players = [
                Andy := structures.Player('Andy'),
                structures.Player('Boa'),
                structures.Player('Coral'),
                structures.Player('Dino'),
            ]
            table = structures.Table(all_players)

            # Make the table to have an amount to be answered
            table.add_to_current_amount(100)

            # Request action
            generator = managers.wait_for_player(player=Andy, table=table, ignore_invalid_actions=True)
            player = next(generator)
            player.request_action(structures.Action(constants.ACTION_CHECK))
            player = next(generator)
            player.request_action(structures.Action(constants.ACTION_BET, 100))
            player = next(generator)
            player.request_action(structures.Action(constants.ACTION_CHECK))
            player = next(generator)
            player.request_action(structures.Action(constants.ACTION_BET, 200))
            player = next(generator)
            player.request_action(structures.Action(constants.ACTION_BET, 150))
            player = next(generator)
            player.request_action(valid_action)

            # End iteration and retrieve returned value
            try:
                next(generator)
            except StopIteration as ex:
                return ex.value

        self.assertEqual(parse_multiple_invalid_actions_and_final_valid_action(), valid_action)


    def test_not_under_bet_parsing(self):


        """
        Runs test cases to check actions are correctly parsed into the generator object when round is not under bet.
        """

        valid_action = structures.Action(constants.ACTION_CHECK)
        def parse_single_valid_action():

            # Define table and current player
            all_players = [
                Andy := structures.Player('Andy'),
                structures.Player('Boa'),
                structures.Player('Coral'),
                structures.Player('Dino'),
            ]
            table = structures.Table(all_players)

            # Request action
            generator = managers.wait_for_player(player=Andy, table=table, ignore_invalid_actions=True)
            player = next(generator)
            player.request_action(valid_action)

            # End iteration and retrieve returned value
            try:
                next(generator)
            except StopIteration as ex:
                return ex.value

        self.assertEqual(parse_single_valid_action(), valid_action)        


        def parse_single_invalid_action():

            # Define table and current player
            all_players = [
                Andy := structures.Player('Andy'),
                structures.Player('Boa'),
                structures.Player('Coral'),
                structures.Player('Dino'),
            ]
            table = structures.Table(all_players)

            # Request action
            generator = managers.wait_for_player(player=Andy, table=table, ignore_invalid_actions=True)
            player = next(generator)
            player.request_action(structures.Action(constants.ACTION_RAISE, 100))

            # End iteration and retrieve returned value
            try:
                next(generator)
            except StopIteration as ex:
                return ex.value

        self.assertIsNone(parse_single_invalid_action())


        def parse_multiple_invalid_actions():

            # Define table and current player
            all_players = [
                Andy := structures.Player('Andy'),
                structures.Player('Boa'),
                structures.Player('Coral'),
                structures.Player('Dino'),
            ]
            table = structures.Table(all_players, open_fold_allowed=False)

            # Request action
            generator = managers.wait_for_player(player=Andy, table=table, ignore_invalid_actions=True)
            player = next(generator)
            player.request_action(structures.Action(constants.ACTION_RAISE, 100))
            player = next(generator)
            player.request_action(structures.Action(constants.ACTION_CALL, 100))
            player = next(generator)
            player.request_action(structures.Action(constants.ACTION_FOLD))
            player = next(generator)
            player.request_action(structures.Action(constants.ACTION_RAISE, 100))
            player = next(generator)
            player.request_action(structures.Action(constants.ACTION_CALL, 100))
            player = next(generator)
            player.request_action(structures.Action(constants.ACTION_FOLD))

            # End iteration and retrieve returned value
            try:
                next(generator)
            except StopIteration as ex:
                return ex.value

        self.assertIsNone(parse_multiple_invalid_actions())


        valid_action = structures.Action(constants.ACTION_CHECK)
        def parse_multiple_invalid_actions_and_final_valid_action():

            # Define table and current player
            all_players = [
                Andy := structures.Player('Andy'),
                structures.Player('Boa'),
                structures.Player('Coral'),
                structures.Player('Dino'),
            ]
            table = structures.Table(all_players, open_fold_allowed=False)

            # Request action
            generator = managers.wait_for_player(player=Andy, table=table, ignore_invalid_actions=True)
            player = next(generator)
            player.request_action(structures.Action(constants.ACTION_RAISE, 100))
            player = next(generator)
            player.request_action(structures.Action(constants.ACTION_CALL, 100))
            player = next(generator)
            player.request_action(structures.Action(constants.ACTION_FOLD))
            player = next(generator)
            player.request_action(structures.Action(constants.ACTION_RAISE, 100))
            player = next(generator)
            player.request_action(structures.Action(constants.ACTION_CALL, 100))
            player = next(generator)
            player.request_action(structures.Action(constants.ACTION_FOLD))
            player = next(generator)
            player.request_action(valid_action)

            # End iteration and retrieve returned value
            try:
                next(generator)
            except StopIteration as ex:
                return ex.value

        self.assertEqual(parse_multiple_invalid_actions_and_final_valid_action(), valid_action)


if __name__ == '__main__':
    main()