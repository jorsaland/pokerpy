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
Defines the function that retrieves the pot split into main and side pots.
"""


def get_split_pot(total_pot: int, players_amounts: list[int]):

    """
    Retrieves the pot split into main and side pots.
    """

    assert total_pot >= sum(amount for amount in players_amounts)
    splitted_pot: list[int] = []

    if len(set(players_amounts)) == 1:
        splitted_pot.append(total_pot)
        return splitted_pot

    min_amount = min(amount for amount in players_amounts)
    main_pot = 0
    remaining_amounts: list[int] = []

    for amount in players_amounts:
        main_pot += min_amount
        if amount > min_amount:
            remaining_amounts.append(amount - min_amount)

    remaining_pot = total_pot - main_pot
    splitted_pot.extend([main_pot, *get_split_pot(remaining_pot, remaining_amounts)])
    return splitted_pot