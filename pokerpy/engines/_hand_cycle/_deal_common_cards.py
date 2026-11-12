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


"Defines the function that Deals common cards to table."


from typing import TYPE_CHECKING


from pokerpy.logger import logger, wrap_internal_log
from pokerpy.states import CommonDealingAwait
from pokerpy.validations import (
    validate_card_in_deck,
    validate_int_positive,
    validate_iterable_has_n_cards,
    validate_iterable_not_repeated_cards,
    validate_type_int,
)


if TYPE_CHECKING:
    from ._hand_cycle import HandCycle


def deal_common_cards(hand_cycle: "HandCycle", cards_count: int):

    "Deals common cards to table."

    validate_type_int(cards_count)
    validate_int_positive(cards_count)

    yield (await_state := CommonDealingAwait(count=cards_count, deck=hand_cycle.table.deck))
    chosen_cards = await_state.dealt_cards

    validate_iterable_has_n_cards(chosen_cards, cards_count)
    validate_iterable_not_repeated_cards(chosen_cards)
    for card in chosen_cards:
        validate_card_in_deck(card, hand_cycle.table.deck)

    for card in chosen_cards:
        hand_cycle.table.remove_card_from_deck(card)
        hand_cycle.table.assign_common_card(card)
    logger.info(f'Dealer deals common cards: {"".join(str(card) for card in chosen_cards)}.')

    logger.info(wrap_internal_log())