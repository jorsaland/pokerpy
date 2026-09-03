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


from pokerpy.constants import ACTION_CHECK, ACTION_FOLD
from pokerpy.validations import (
    validate_str_action_category,
    validate_int_positive,
    validate_int_zero,
    validate_type_int,
    validate_type_str,
)


class Action:


    """
    Represents an action taken by a player within a betting round.
    """


    def __init__(self, category: str, amount: int = 0):

        validate_type_str(category)
        validate_type_int(amount)

        validate_str_action_category(category)
        
        if category in (ACTION_FOLD, ACTION_CHECK):
            validate_int_zero(amount)
        else:
            validate_int_positive(amount)

        self._category = category
        self._amount = amount


    @property
    def category(self):
        "Name of the action (fold, check, call, bet and raise)."
        return self._category
    
    @property
    def amount(self):
        "Amount of chips placed in front during the action."
        return self._amount


    def __repr__(self):
        return f'Action(name={self.category}, amount={self.amount})'
    

    def __eq__(self, other):

        if not isinstance(other, Action):
            return NotImplemented

        return (self.category == other.category) and (self.amount == other.amount)