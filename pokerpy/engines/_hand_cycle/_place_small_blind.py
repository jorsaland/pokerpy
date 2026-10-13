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


"Defines the function that runs the small blind placing event."


from pokerpy.logger import logger
from pokerpy.structures import Player, Table


def place_small_blind(*, table: Table, extra_big_blind_players: list[Player], small_blind: int):

    "Runs the small blind placing event."

    small_blind_player = table.small_blind_player

    if small_blind_player in extra_big_blind_players:
        extra_big_blind_players.remove(small_blind_player)

    if not small_blind_player.stack:
        logger.info(f"{small_blind_player.name} IS ALL-IN, CANNOT PLACE SMALL BLIND")

    if small_blind_player.stack:
        amount = (
            small_blind
            if small_blind_player.stack > small_blind
            else small_blind_player.stack
        )
        small_blind_player.decrease_stack(amount)
        small_blind_player.increase_bet_level(amount)
        logger.info(
            f"{small_blind_player.name} PLACES SMALL BLIND {amount} "
            f"({small_blind_player.name}'s bet level: {small_blind_player.bet_level} | "
            f"stack: {small_blind_player.stack})"
        )