# Copyright 2026 Andrés Saldarriaga Jordan (jorsaland)

# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at

#     http://www.apache.org/licenses/LICENSE-2.0

# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.


"""
Defines the class that represents an action taken by a player within a betting round.
"""


from pokerpy.constants import (
    ACTION_CHECK,
    ACTION_FOLD,
    possible_action_names,
)
from pokerpy.messages import (
    msg_invalid_action_name,
    msg_not_int,
    msg_not_positive_value,
    msg_not_str,
    msg_not_zero_value,
)


class Action:


    """
    Represents an action taken by a player within a betting round.
    """


    def __init__(self, name: str, amount: int = 0):

        # Check types
        if not isinstance(name, str):
            raise TypeError(msg_not_str.format(type(name).__name__))
        if not isinstance(amount, int):
            raise TypeError(msg_not_int.format(type(amount).__name__))

        # Validate input
        if name not in possible_action_names:
            error_message = msg_invalid_action_name.format(', '.join(possible_action_names))
            raise ValueError(error_message)
        
        # Validate amount
        if name in (ACTION_FOLD, ACTION_CHECK):
            if amount != 0:
                raise ValueError(msg_not_zero_value.format(name, amount))
        else:
            if amount <= 0:
                raise ValueError(msg_not_positive_value.format(name, amount))

        # Fixed variables
        self._name = name
        self._amount = amount


    @property
    def name(self):
        "Name of the action."
        return self._name
    
    @property
    def amount(self):
        "Amount put by the player when performing the action."
        return self._amount


    def __repr__(self):
        return f'Action(name={self.name}, amount={self.amount})'
    

    def __eq__(self, other):

        if not isinstance(other, Action):
            return NotImplemented

        return (self.name == other.name) and (self.amount == other.amount)