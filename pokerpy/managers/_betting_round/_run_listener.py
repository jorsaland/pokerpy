"""
Defines the function that starts the betting round generator that rotates the player turns.
"""


from typing import TYPE_CHECKING


from ._alternate_players import alternate_players
if TYPE_CHECKING:
    from ._betting_round import BettingRound


def run_listener(self: "BettingRound"):

    """
    Starts the betting round generator that rotates the player turns.
    """

    # Define state variables
    round_must_stop = False
    lap_counter = 0
            
    # Extend betting round until the last aggressive action has been responded
    while not round_must_stop:

        # Add to lap counter
        lap_counter += 1

        # All players are itered but only active ones are allowed to act
        round_must_stop = yield from alternate_players(self)

        # After the first lap, reset the starting player as the first one on the list
        self._starting_player = self.table.players[0]
    
    # Move chips to the center of the table
    for player in self.table.players:
        self.table.add_to_central_pot(player.current_amount)

    # Mark betting round as ended
    self._has_ended = True