
"Defines the function that validates types."


from collections.abc import Iterable


from pokerpy import messages


def validate_all_type_card(sequence: Iterable):

    "Validates all elements in a sequence are type Card."

    from pokerpy.structures._card import Card

    if not all(isinstance(item, Card) for item in sequence):
        raise TypeError(messages.msg_not_all_card_instances)


def validate_all_type_player(sequence: Iterable):

    "Validates all elements in a sequence are type Player."

    from pokerpy.structures._player import Player

    if not all(isinstance(item, Player) for item in sequence):
        raise TypeError(messages.msg_not_all_player_instances)


def validate_type_action(obj):

    "Validates an object is of type Action."

    from pokerpy.structures._action import Action

    if not isinstance(obj, Action):
        raise TypeError(messages.msg_not_action_instance.format(type(obj).__name__))


def validate_type_card(obj):

    "Validates an object is of type Card."

    from pokerpy.structures._card import Card

    if not isinstance(obj, Card):
        raise TypeError(messages.msg_not_card_instance.format(type(obj).__name__))


def validate_type_hand(obj):

    "Validates an object is of type Hand."

    from pokerpy.structures._hand._hand import Hand

    if not isinstance(obj, Hand):
        raise TypeError(messages.msg_not_hand_instance.format(type(obj).__name__))


def validate_type_int(obj):

    "Validates an object is of type integer."

    if not isinstance(obj, int):
        raise TypeError(messages.msg_not_int.format(type(obj).__name__))


def validate_type_iterable(obj):

    "Validates an object is iterable."

    if not isinstance(obj, Iterable):
        raise TypeError(messages.msg_not_iterable_object.format(type(obj).__name__))


def validate_type_list(obj):

    "Validates an object is a list."

    if not isinstance(obj, list):
        raise TypeError(messages.msg_not_list.format(type(obj).__name__))


def validate_type_player(obj):

    "Validates an object is of type Player."

    from pokerpy.structures._player import Player

    if not isinstance(obj, Player):
        raise TypeError(messages.msg_not_player_instance.format(type(obj).__name__))


def validate_type_str(obj):

    "Validates an object is of type string."

    if not isinstance(obj, str):
        raise TypeError(messages.msg_not_str.format(type(obj).__name__))


def validate_type_table(obj):

    "Validates an object is of type Table."

    from pokerpy.structures._table import Table

    if not isinstance(obj, Table):
        raise TypeError(messages.msg_not_table_instance.format(type(obj).__name__))