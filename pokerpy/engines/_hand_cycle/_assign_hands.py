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
Defines the function that assigns the hands to the players.
"""


from itertools import combinations


from pokerpy.logger import get_logger
from pokerpy.structures import Hand, Table


logger = get_logger()


def assign_hands(table: Table):

    "Assigns the hands to the players."

    for player in table.players:

        cards = player.cards + table.common_cards
    
        if len(cards) < 5:
            continue
        
        if len(cards) == 5:
            hand = Hand(cards)
        else:
            hand = max(Hand(combination) for combination in combinations(cards, 5))

        player.assign_hand(hand)