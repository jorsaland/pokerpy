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


"Defines the function that runs the big blind placing event."


from pokerpy.logger import logger, wrap_internal_log
from pokerpy.structures import Player, Table


def place_big_blind(*, table: Table, extra_big_blind_players: list[Player], big_blind: int):

    "Runs the big blind placing event."

    big_blind_player = table.big_blind_player

    if big_blind_player in extra_big_blind_players:
        extra_big_blind_players.remove(big_blind_player)

    if not big_blind_player.stack:
        logger.info(f"{big_blind_player.name} IS ALL-IN, CANNOT PLACE BIG BLIND")
    else:
        amount = (
            big_blind
            if big_blind_player.stack > big_blind
            else big_blind_player.stack
        )
        big_blind_player.decrease_stack(amount)
        big_blind_player.increase_bet_level(amount)
        logger.info(
            f"{big_blind_player.name} PLACES BIG BLIND {amount} "
            f"({big_blind_player.name}'s bet level: {big_blind_player.bet_level} | "
            f"stack: {big_blind_player.stack})"
        )

    table.set_bet_level(big_blind)
    table.set_full_bet_level(big_blind)
    logger.info(f'TABLE CURRENT LEVEL: {table.bet_level}')
    logger.info(wrap_internal_log())