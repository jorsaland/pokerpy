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
Defines the methods that affect money attributes.
"""


from typing import TYPE_CHECKING


from pokerpy.messages import msg_not_int, msg_not_positive_value


if TYPE_CHECKING:
    from ._betting_round import BettingRound


def method_overwrite_smallest_raise_amount(self: "BettingRound", amount: int):

    """
    Overwrites the smallest amount expected to make a raise.
    """

    if not isinstance(amount, int):
        raise TypeError(msg_not_int.format(type(amount).__name__))
    
    if amount <= 0:
        raise ValueError(msg_not_positive_value.format(amount))

    self._smallest_raise_amount = amount