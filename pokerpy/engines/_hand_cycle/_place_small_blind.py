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


from pokerpy.logger import logger, wrap_internal_log
from pokerpy.structures import Player


def place_small_blind(amount: int, player: Player):

    "Runs the small blind placing event."

    if not player.stack:
        logger.info(f"{player.name} IS ALL-IN, CANNOT PLACE SMALL BLIND")
        return

    amount = (
        amount
        if player.stack > amount
        else player.stack
    )
    player.decrease_stack(amount)
    player.increase_bet_level(amount)
    logger.info(
        f"{player.name} PLACES SMALL BLIND {amount} "
        f"({player.name}'s bet level: {player.bet_level} | "
        f"stack: {player.stack})"
    )
    logger.info(wrap_internal_log())