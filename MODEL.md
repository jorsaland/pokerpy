# Properties of structures


### Card (`Card`)

- **Value (`value`):** Rank of the card (numbers from 2 to 10, jacks, queens, kings and aces).

- **Suit (`suit`):** Symbol paired with the value (clubs, diamonds, hearts and spades).


### Hand (`Hand`)

- **Cards (`cards`):** Set of five cards that make up the hand.

- **Category (`category`):** Rank of the hand (high card, pair, two pair, three of a kind, straight, flush, full house, four of a kind, straight flush and royal flush).


### Action (`Action`)

- **Category (`category`):** Name of the action (fold, check, call, bet and raise).

- **Amount (`amount`):** Amount of chips placed in front during the action.


### Player (`Player`)

- **Name (`name`):** Player's identifier, unique within the table.

- **Cards (`cards`):** Cards dealt to the player.

- **Hand (`hand`):** Hand the player holds, according to the game rules.

- **Requested action (`requested_action`):** Action the player has requested in a betting round.

- **Stack (`stack`):** Chips the player has available to play.

- **Amount (`amount`):** Amount of chips the player has placed in front during the current betting round.

- **Pot participation (`pot_participation`):** Total amount of chips the player has placed in the pot during the current hand cycle.

- **Is folded (`is_folded`):** Whether the player has already folded in the current hand cycle.

- **Has played (`has_played`):** Whether the player has already taken a voluntary action during the current betting round (not including forced bets).


### Table (`Table`)

- **Deck (`deck`):** Cards still available to be dealt.

- **Common cards (`common_cards`):** Cards dealt as common to all players.

- **Players (`players`):** Players sitting at the table, in their respective order.

- **Participating players (`participating_players`):** Players still playing for the pot during a hand cycle.

- **Active players (`active_players`):** Players still playing for the pot and not all-in during a hand cycle.

- **Starting player (`starting_player`):** Player who acts first in the betting round. Defaults to the first player in the players list.

- **Stopping player (`stopping_player`):** Player who acts last in the betting round. This may be updated during the betting round, depending on the actions taken by other players. Defaults to the player before the starting player.

- **Current player (`current_player`):** Player who is being awaited to play. Defaults to the starting player.

- **Amount level (`amount_level`):** Largest amount of chips a player has placed in front during the current betting round, which other players must match in order to call.

- **Full bet (`full_bet`):** Minimum amount to bet.

- **Full amount level (`full_amount_level`):** Part of the amount level considered a full bet or raise. It may be smaller than a full bet when a player goes all-in for less. In that case, other players can complete the full bet (in addition to folding, calling or raising).

- **Full raise increase (`full_raise_increase`):** Minimum amount by which to increase the full amount level.

- **Pot (`pot`):** Total amount of chips being played for in the betting round.

- **Split pot (`split_pot`):** Pot split into main pot and side pots.


# Properties of engines


### Betting round (`BettingRound`)

- **Name (`name`):** Betting round's identifier, unique within the hand cycle.

- **Table (`table`):** Table in which the betting round takes place.

- **Lap counts (`lap_counts`):** Number of times the action passes through the starting player (even if folded or all-in).

- **Open fold allowed (`open_fold_allowed`):** *[modifiable]* Whether folding is allowed when there is no bet or raise to respond to.

- **Is completed (`is_completed`):** Whether the betting round already ended.

- **Raise invalid actions (`raise_invalid_actions`):** Whether an exception should be raised when an invalid action is chosen, or the player should be prompted again.


# Communication model


```mermaid
flowchart LR


    %% Legend

    subgraph " "
        i1(class)@{ shape: circle }
        i2(class)@{ shape: circle }
        m1(method)@{ shape: text }
        m2(helper method)@{ shape: text }
        i1 --> |calls| m1
        m1 --> |from| i2
        m1 -.-> |uses| m2
        m2 --> |from| i2
    end


    %% Classes and methods
    
    BR(BettingRound)@{ shape: circle }
    BR.close(close)@{ shape: text } -->  BR
    BR.listen(listen)@{ shape: text } -->  BR
    BR.reset_betting_round_states(reset_betting_round_states)@{ shape: text } -->  BR
    BR.increase_counter(increase_counter)@{ shape: text } -->  BR
    BR.set_current_player(set_current_player)@{ shape: text } -->  BR
    BR.get_action_ranges(get_action_ranges)@{ shape: text } --> BR

    T(Table)@{ shape: circle }
    T.remove_card_from_deck(remove_card_from_deck)@{ shape: text } --> T
    T.assign_common_card(assign_common_card)@{ shape: text } --> T
    T.set_full_bet(set_full_bet)@{ shape: text } --> T
    T.set_full_raise_increase(set_full_raise_increase)@{ shape: text } --> T
    T.set_current_level(set_current_level)@{ shape: text } --> T
    T.set_complete_current_level(set_complete_current_level)@{ shape: text } --> T
    T.increase_central_pot(increase_central_pot)@{ shape: text } --> T
    T.set_starting_player(set_starting_player)@{ shape: text } --> T
    T.set_stopping_player(set_stopping_player)@{ shape: text } --> T
    T.get_previous_player(get_previous_player)@{ shape: text } --> T
    T.get_next_player(get_next_player)@{ shape: text } --> T
    T.iter_players(iter_players)@{ shape: text } --> T
    T.get_previous_active_player(get_previous_active_player)@{ shape: text } --> T

    C(Controller)@{ shape: cloud }

    P(Player)@{ shape: circle }
    P.request_action(request_action)@{ shape: text } --> P
    P.reset_action(reset_action)@{ shape: text } --> P
    P.assign_card(assign_card)@{ shape: text } --> P
    P.increase_amount(increase_amount)@{ shape: text } --> P
    P.increase_pot_participation(increase_pot_participation)@{ shape: text } --> P
    P.decrease_stack(decrease_stack)@{ shape: text } --> P
    P.mark_has_played(mark_has_played)@{ shape: text } --> P
    P.unmark_has_played(unmark_has_played)@{ shape: text } --> P
    P.mark_is_folded(mark_is_folded)@{ shape: text } --> P

    H(Hand)@{ shape: circle }

    Cd(Card)@{ shape: circle }
    Cd.get_deck_position(get_deck_position)@{ shape: text } --> Cd


    %% Class to method relations

    C --> BR.close
    C --> BR.listen
    C --> BR.get_action_ranges

    C --> P.request_action

    BR --> T.remove_card_from_deck
    BR --> T.assign_common_card
    BR --> T.set_full_bet
    BR --> T.set_full_raise_increase
    BR --> T.set_current_level
    BR --> T.set_complete_current_level
    BR --> T.increase_central_pot
    BR --> T.set_starting_player
    BR --> T.set_stopping_player
    BR --> T.get_previous_active_player
    BR --> T.iter_players
    BR --> T.get_previous_player

    BR --> P.reset_action
    BR --> P.assign_card
    BR --> P.increase_amount
    BR --> P.increase_pot_participation
    BR --> P.decrease_stack
    BR --> P.mark_has_played
    BR --> P.unmark_has_played
    BR --> P.mark_is_folded

    H --> Cd.get_deck_position


    %% Helper method relations

    BR.close -.-> BR.reset_betting_round_states
    BR.close -.-> BR.listen

    BR.listen -.-> BR.reset_betting_round_states
    BR.listen -.-> BR.increase_counter
    BR.listen -.-> BR.set_current_player

    T.get_previous_active_player -.-> T.iter_players
    T.get_previous_active_player -.-> T.get_previous_player

    T.iter_players -.-> T.get_next_player
    T.iter_players -.-> T.get_previous_player
```
