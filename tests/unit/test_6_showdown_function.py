"""
Defines unit tests on functions that are part of the engines module.
"""


import sys
sys.path.insert(0, '.')


from unittest import main, TestCase


from pokerpy import engines, messages, structures


class TestInput(TestCase):


    """
    Runs unit tests on showdown function related to its input.
    """


    def test_invalid_input(self):


        """
        Runs test cases on showdown function with an invalid input.
        """


        with self.assertRaises(TypeError) as context:
            engines.reset_cycle_states('Wood')
        self.assertEqual(context.exception.args[0], messages.msg_not_table_instance.format(str.__name__))


class TestShowdownOneWinner(TestCase):


    """
    Runs unit tests on showdown function when there is only one winner.
    """


    def test_one_remaining_player(self):

        """
        Runs test cases on showdown function when one player is remaining (no showdown).
        """

        table = structures.Table([
            Andy := structures.Player('Andy', 10),
            Boa := structures.Player('Boa', 10),
            Coral := structures.Player('Coral', 10),
            Dino := structures.Player('Coral', 10),
        ])
        table.add_to_central_pot(5)

        Andy.assign_hand(structures.Hand([
            structures.Card('A', 's'),
            structures.Card('K', 's'),
            structures.Card('Q', 's'),
            structures.Card('J', 's'),
            structures.Card('T', 's'),
        ]))
        Boa.mark_is_folded()
        Coral.mark_is_folded()
        Dino.mark_is_folded()

        # Before states
        self.assertEqual(Andy.stack, 10)
        self.assertEqual(Boa.stack, 10)
        self.assertEqual(Coral.stack, 10)
        self.assertEqual(Dino.stack, 10)

        engines.showdown(table)

        # After states
        self.assertEqual(Andy.stack, 15)
        self.assertEqual(Boa.stack, 10)
        self.assertEqual(Coral.stack, 10)
        self.assertEqual(Dino.stack, 10)


    def test_two_remaining_players(self):

        """
        Runs test cases on showdown function when two players are remaining.
        """

        table = structures.Table([
            Andy := structures.Player('Andy', 10),
            Boa := structures.Player('Boa', 10),
            Coral := structures.Player('Coral', 10),
            Dino := structures.Player('Coral', 10),
        ])
        table.add_to_central_pot(5)

        Andy.assign_hand(structures.Hand([
            structures.Card('A', 's'),
            structures.Card('K', 's'),
            structures.Card('Q', 's'),
            structures.Card('J', 's'),
            structures.Card('T', 's'),
        ]))
        Boa.assign_hand(structures.Hand([
            structures.Card('A', 's'),
            structures.Card('A', 'h'),
            structures.Card('A', 'd'),
            structures.Card('2', 's'),
            structures.Card('2', 'h'),
        ]))
        Coral.mark_is_folded()
        Dino.mark_is_folded()

        # Before states
        self.assertEqual(Andy.stack, 10)
        self.assertEqual(Boa.stack, 10)
        self.assertEqual(Coral.stack, 10)
        self.assertEqual(Dino.stack, 10)

        engines.showdown(table)

        # After states
        self.assertEqual(Andy.stack, 15)
        self.assertEqual(Boa.stack, 10)
        self.assertEqual(Coral.stack, 10)
        self.assertEqual(Dino.stack, 10)


    def test_more_remaining_players(self):

        """
        Runs test cases on showdown function when more than two players are remaining.
        """

        table = structures.Table([
            Andy := structures.Player('Andy', 10),
            Boa := structures.Player('Boa', 10),
            Coral := structures.Player('Coral', 10),
            Dino := structures.Player('Coral', 10),
        ])
        table.add_to_central_pot(5)

        Andy.assign_hand(structures.Hand([
            structures.Card('A', 's'),
            structures.Card('K', 's'),
            structures.Card('Q', 's'),
            structures.Card('J', 's'),
            structures.Card('T', 's'),
        ]))
        Boa.assign_hand(structures.Hand([
            structures.Card('A', 's'),
            structures.Card('A', 'h'),
            structures.Card('A', 'd'),
            structures.Card('2', 's'),
            structures.Card('2', 'h'),
        ]))
        Coral.assign_hand(structures.Hand([
            structures.Card('A', 's'),
            structures.Card('K', 'h'),
            structures.Card('Q', 'd'),
            structures.Card('J', 'c'),
            structures.Card('T', 's'),
        ]))
        Dino.assign_hand(structures.Hand([
            structures.Card('A', 's'),
            structures.Card('Q', 'h'),
            structures.Card('T', 'd'),
            structures.Card('8', 'c'),
            structures.Card('6', 's'),
        ]))

        # Before states
        self.assertEqual(Andy.stack, 10)
        self.assertEqual(Boa.stack, 10)
        self.assertEqual(Coral.stack, 10)
        self.assertEqual(Dino.stack, 10)

        engines.showdown(table)

        # After states
        self.assertEqual(Andy.stack, 15)
        self.assertEqual(Boa.stack, 10)
        self.assertEqual(Coral.stack, 10)
        self.assertEqual(Dino.stack, 10)


class TestShowdownTie(TestCase):


    """
    Runs unit tests on showdown function when there is a tie.
    """


    def test_two_winners_with_exact_split(self):

        """
        Runs test cases on showdown function when two players tie and money can be split in equal amounts.
        """

        table = structures.Table([
            Andy := structures.Player('Andy', 10),
            Boa := structures.Player('Boa', 10),
            Coral := structures.Player('Coral', 10),
            Dino := structures.Player('Coral', 10),
        ])
        table.add_to_central_pot(10)

        Andy.assign_hand(structures.Hand([
            structures.Card('A', 's'),
            structures.Card('K', 's'),
            structures.Card('Q', 's'),
            structures.Card('J', 's'),
            structures.Card('T', 's'),
        ]))
        Boa.assign_hand(structures.Hand([
            structures.Card('A', 's'),
            structures.Card('K', 's'),
            structures.Card('Q', 's'),
            structures.Card('J', 's'),
            structures.Card('T', 's'),
        ]))
        Coral.assign_hand(structures.Hand([
            structures.Card('A', 's'),
            structures.Card('K', 'h'),
            structures.Card('Q', 'd'),
            structures.Card('J', 'c'),
            structures.Card('T', 's'),
        ]))
        Dino.assign_hand(structures.Hand([
            structures.Card('A', 's'),
            structures.Card('Q', 'h'),
            structures.Card('T', 'd'),
            structures.Card('8', 'c'),
            structures.Card('6', 's'),
        ]))

        # Before states
        self.assertEqual(Andy.stack, 10)
        self.assertEqual(Boa.stack, 10)
        self.assertEqual(Coral.stack, 10)
        self.assertEqual(Dino.stack, 10)

        engines.showdown(table)

        # After states
        self.assertEqual(Andy.stack, 15)
        self.assertEqual(Boa.stack, 15)
        self.assertEqual(Coral.stack, 10)
        self.assertEqual(Dino.stack, 10)


    def test_two_winners_with_inexact_split(self):

        """
        Runs test cases on showdown function when two players tie and money cannot be split in equal amounts.
        """

        table = structures.Table([
            Andy := structures.Player('Andy', 10),
            Boa := structures.Player('Boa', 10),
            Coral := structures.Player('Coral', 10),
            Dino := structures.Player('Coral', 10),
        ])
        table.add_to_central_pot(9)

        Andy.assign_hand(structures.Hand([
            structures.Card('A', 's'),
            structures.Card('K', 's'),
            structures.Card('Q', 's'),
            structures.Card('J', 's'),
            structures.Card('T', 's'),
        ]))
        Boa.assign_hand(structures.Hand([
            structures.Card('A', 's'),
            structures.Card('K', 's'),
            structures.Card('Q', 's'),
            structures.Card('J', 's'),
            structures.Card('T', 's'),
        ]))
        Coral.assign_hand(structures.Hand([
            structures.Card('A', 's'),
            structures.Card('K', 'h'),
            structures.Card('Q', 'd'),
            structures.Card('J', 'c'),
            structures.Card('T', 's'),
        ]))
        Dino.assign_hand(structures.Hand([
            structures.Card('A', 's'),
            structures.Card('Q', 'h'),
            structures.Card('T', 'd'),
            structures.Card('8', 'c'),
            structures.Card('6', 's'),
        ]))

        # Before states
        self.assertEqual(Andy.stack, 10)
        self.assertEqual(Boa.stack, 10)
        self.assertEqual(Coral.stack, 10)
        self.assertEqual(Dino.stack, 10)

        engines.showdown(table)

        # After states
        self.assertEqual(Andy.stack, 15)
        self.assertEqual(Boa.stack, 14)
        self.assertEqual(Coral.stack, 10)
        self.assertEqual(Dino.stack, 10)


    def test_multiple_winners_with_exact_split(self):

        """
        Runs test cases on showdown function when more than two players tie and money can be split in equal amounts.
        """

        table = structures.Table([
            Andy := structures.Player('Andy', 10),
            Boa := structures.Player('Boa', 10),
            Coral := structures.Player('Coral', 10),
            Dino := structures.Player('Coral', 10),
        ])
        table.add_to_central_pot(20)

        Andy.assign_hand(structures.Hand([
            structures.Card('A', 's'),
            structures.Card('K', 's'),
            structures.Card('Q', 's'),
            structures.Card('J', 's'),
            structures.Card('T', 's'),
        ]))
        Boa.assign_hand(structures.Hand([
            structures.Card('A', 's'),
            structures.Card('K', 's'),
            structures.Card('Q', 's'),
            structures.Card('J', 's'),
            structures.Card('T', 's'),
        ]))
        Coral.assign_hand(structures.Hand([
            structures.Card('A', 's'),
            structures.Card('K', 's'),
            structures.Card('Q', 's'),
            structures.Card('J', 's'),
            structures.Card('T', 's'),
        ]))
        Dino.assign_hand(structures.Hand([
            structures.Card('A', 's'),
            structures.Card('K', 's'),
            structures.Card('Q', 's'),
            structures.Card('J', 's'),
            structures.Card('T', 's'),
        ]))

        # Before states
        self.assertEqual(Andy.stack, 10)
        self.assertEqual(Boa.stack, 10)
        self.assertEqual(Coral.stack, 10)
        self.assertEqual(Dino.stack, 10)

        engines.showdown(table)

        # After states
        self.assertEqual(Andy.stack, 15)
        self.assertEqual(Boa.stack, 15)
        self.assertEqual(Coral.stack, 15)
        self.assertEqual(Dino.stack, 15)


    def test_multiple_winners_with_inexact_split(self):

        """
        Runs test cases on showdown function when more than two players tie and money cannot be split in equal amounts.
        """

        table = structures.Table([
            Andy := structures.Player('Andy', 10),
            Boa := structures.Player('Boa', 10),
            Coral := structures.Player('Coral', 10),
            Dino := structures.Player('Coral', 10),
        ])
        table.add_to_central_pot(18)

        Andy.assign_hand(structures.Hand([
            structures.Card('A', 's'),
            structures.Card('K', 's'),
            structures.Card('Q', 's'),
            structures.Card('J', 's'),
            structures.Card('T', 's'),
        ]))
        Boa.assign_hand(structures.Hand([
            structures.Card('A', 's'),
            structures.Card('K', 's'),
            structures.Card('Q', 's'),
            structures.Card('J', 's'),
            structures.Card('T', 's'),
        ]))
        Coral.assign_hand(structures.Hand([
            structures.Card('A', 's'),
            structures.Card('K', 's'),
            structures.Card('Q', 's'),
            structures.Card('J', 's'),
            structures.Card('T', 's'),
        ]))
        Dino.assign_hand(structures.Hand([
            structures.Card('A', 's'),
            structures.Card('K', 's'),
            structures.Card('Q', 's'),
            structures.Card('J', 's'),
            structures.Card('T', 's'),
        ]))

        # Before states
        self.assertEqual(Andy.stack, 10)
        self.assertEqual(Boa.stack, 10)
        self.assertEqual(Coral.stack, 10)
        self.assertEqual(Dino.stack, 10)

        engines.showdown(table)

        # After states
        self.assertEqual(Andy.stack, 15)
        self.assertEqual(Boa.stack, 15)
        self.assertEqual(Coral.stack, 14)
        self.assertEqual(Dino.stack, 14)


if __name__ == '__main__':
    main()