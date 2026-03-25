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
Defines the methods that deal cards.
"""


import secrets
from typing import TYPE_CHECKING


from pokerpy.logger import get_logger
from pokerpy.messages import msg_not_int


if TYPE_CHECKING:
    from ._betting_round import BettingRound


logger = get_logger()


def method_deal_cards_to_players(self: "BettingRound", cards_count: int):

    """
    Deals cards to players in equal amounts.
    """

    if not isinstance(cards_count, int):
        raise TypeError(msg_not_int.format(type(cards_count).__name__))

    for _ in range(cards_count):
        for player in self.table.players_in_hand:
            card = secrets.choice(self.table.deck)
            self.table.remove_card_from_deck(card)
            player.deal_card(card)
            logger.info(f'Dealer deals card {card} to {player.name}.')


def method_deal_common_cards(self: "BettingRound", cards_count: int):

    """
    Deals common cards to table.
    """

    if not isinstance(cards_count, int):
        raise TypeError(msg_not_int.format(type(cards_count).__name__))

    for _ in range(cards_count):
        card = secrets.choice(self.table.deck)
        self.table.remove_card_from_deck(card)
        self.table.deal_common_card(card)
    
    logger.info(f'Dealer deals common cards: {"".join(str(card) for card in self.table.common_cards[-cards_count:])}.')