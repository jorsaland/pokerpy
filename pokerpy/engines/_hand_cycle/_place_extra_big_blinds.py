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


"Defines the function that runs the event for placing extra big blinds."


from collections.abc import Iterable


from pokerpy.logger import logger, wrap_internal_log
from pokerpy.structures import Player


def place_extra_big_blinds(blind_amount: int, eligible_players: Iterable[Player]):

    "Runs the event for placing extra big blinds."

    for player in eligible_players:

        yield player

        if not player.is_extra_blind or not player.stack:
            continue

        amount = blind_amount if player.stack > blind_amount else player.stack

        player.decrease_stack(amount)
        player.increase_bet_level(amount)

        logger.info(
            f"{player.name} PLACES OPTIONAL BIG BLIND {amount} "
            f"({player.name}'s bet level: {player.bet_level} | stack: {player.stack})"
        )
        logger.info(wrap_internal_log())