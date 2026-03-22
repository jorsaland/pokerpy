"""
Defines functions that return class instances with standard values for the mandatory parameters.
This to avoid having to update code in many places when new mandatory parameters come up.
"""


import sys
sys.path.insert(0, '.')


from pokerpy import structures


def create_standard_player(name: str):

    """
    Creates a standard player with a custom value for the mandatory fields.
    """

    return structures.Player(name, stack=1000000)