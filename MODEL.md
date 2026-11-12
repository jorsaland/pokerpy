# Properties of structures


### Action (`Action`)

- **Category (`category`):** Name of the action (fold, check, call, bet and raise).

- **Amount (`amount`):** Amount of chips placed in front during the action.


### Card (`Card`)

- **Value (`value`):** Rank of the card (numbers from 2 to 10, jacks, queens, kings and aces).

- **Suit (`suit`):** Symbol paired with the value (clubs, diamonds, hearts and spades).


### Hand (`Hand`)

- **Cards (`cards`):** Set of five cards that make up the hand.

- **Category (`category`):** Rank of the hand (high card, pair, two pair, three of a kind, straight, flush, full house, four of a kind, straight flush and royal flush).


### Player (`Player`)

- **Name (`name`):** Player's identifier, unique within the table.

- **Cards (`cards`):** Cards dealt to the player.

- **Hand (`hand`):** Hand the player holds, according to the game rules.

- **Requested action (`requested_action`):** Action the player has requested in a betting round.

- **Is extra blind (`is_extra_blind`):** Whether the player has requested to place an extra blind.

- **Stack (`stack`):** Chips the player has available to play.

- **Bet level (`bet_level`):** Amount of chips the player has placed in front during the current betting round.

- **Is folded (`is_folded`):** Whether the player has already folded in the current hand cycle.

- **Has played (`has_played`):** Whether the player has already taken a voluntary action during the current betting round (not including forced bets).

- **Pot index (`pot_index`):** Index of the deepest pot the player is playing for, being 0 the main pot.


### Table (`Table`)

- **Deck (`deck`):** Cards still available to be dealt.

- **Common cards (`common_cards`):** Cards dealt as common to all players.

- **Players (`players`):** Players sitting at the table, in their respective order.

- **Live players (`live_players`):** Players still playing for the pot during a hand cycle.

- **Actionable players (`actionable_players`):** Players still playing for the pot and not all-in during a hand cycle.

- **Bettor players (`bettor_players`):** Players who have placed chips in front to gather into the pot.

- **Starting player (`starting_player`):** Player who acts first in the betting round. Defaults to the first player in the players list.

- **Stopping player (`stopping_player`):** Player who acts last in the betting round. This may be updated during the betting round, depending on the actions taken by other players. Defaults to the player before the starting player.

- **Button player (`button_player`):** Player that holds the button.

- **Ante (`ante`):** Ante amount.

- **Small blind (`small_blind`):** Small blind amount.

- **Small blind player (`small_blind_player`):** Small blind player.

- **Big blind (`big_blind`):** Big blind amount.

- **Big blind player (`big_blind_player`):** Big blind player.

- **Current player (`current_player`):** Player who is being awaited to play. Defaults to the starting player.

- **Bet level (`bet_level`):** Largest amount of chips a player has placed in front during the current betting round, which other players must match in order to call.

- **Full bet level (`full_bet_level`):** Part of the bet level matching the last full bet or raise. When a player goes all-in for less than a full bet or raise, it stays the same. Only when a player completes the bet or raise, it is increased.

- **Minimum bet (`min_bet`):** Minimum amount to bet.

- **Minimum raise increase (`min_raise_increase`):** Minimum amount by which to increase the full chip level.

- **Pot (`pot`):** Total amount of chips being played for in the betting round.

- **Split central pot (`split_central_pot`):** "Part of the pot that is already placed at the center of the table, split into main and side pots."


# Properties of engines


### Betting round (`BettingRound`)

- **Name (`name`):** Betting round's identifier, unique within the hand cycle.

- **Table (`table`):** Table in which the betting round takes place.

- **Lap counts (`lap_counts`):** Number of times the action passes through the starting player (even if folded or all-in).

- **Is completed (`is_completed`):** Whether the betting round already ended.

- **Was reseted at closure (`was_reseted_at_closure`):** Whether the betting round states were reseted at closure (helps to track closure behaviour in unit tests).

- **Open fold allowed (`open_fold_allowed`):** Whether folding is allowed when there is no bet or raise to respond to.

- **Raise invalid actions (`raise_invalid_actions`):** Whether an exception should be raised when an invalid action is chosen, or the player should be prompted again.


### Hand cycle (`HandCycle`)

- **Name (`name`):** Hand cycle's identifier, unique within the game.

- **Table (`table`):** Table in which the hand cycle takes place.

- **Betting round (`betting_round`):** Betting round taking place.

- **In extra big blinds phase (`in_extra_big_blinds_phase`):** Whether the hand cycle is in the phase of placing extra big blinds.

- **Is completed (`is_completed`):** Whether the hand cycle already ended.

- **Was reseted at closure (`was_reseted_at_closure`):** Whether the hand cycle states were reseted at closure (helps to track closure behaviour in unit tests).

- **Open fold allowed (`open_fold_allowed`):** Whether folding is allowed when there is no bet or raise to respond to.

- **Raise invalid actions (`raise_invalid_actions`):** Whether an exception should be raised when an invalid action is chosen, or the player should be prompted again.


# Communication model


### Legend

```mermaid
flowchart LR

        i1(instance)@{ shape: circle }
        i2(instance)@{ shape: circle }
        m1(method)@{ shape: text }
        m2(method)@{ shape: text }

        i1 ===> |CONTAINS| i2
        i1 --> |calls| m1
        m1 --> |from| i2
        m1 -.-> |calls| m2
        m2 --> |from| i2

```


### From controller

```mermaid
flowchart LR


    %% Classes

    C(Controller)@{ shape: cloud }

    HC(HandCycle)@{ shape: circle }
    BR(BettingRound)@{ shape: circle }
    T(Table)@{ shape: circle }
    P(Player)@{ shape: circle }
    H(Hand)@{ shape: circle }
    Cd(Card)@{ shape: circle }
    A(Action)@{ shape: circle }


    %% Container relations

    T ===> |CONTAINS| P
    T ===> |CONTAINS| Cd
    P ===> |CONTAINS| H
    P ===> |CONTAINS| Cd
    P ===> |CONTAINS| A
    H ===> |CONTAINS| Cd


    %% Methods

    HC.listen(listen)@{ shape: text } -->  HC
    HC.close(close)@{ shape: text } -->  HC
    HC.deal_cards_to_players(deal_cards_to_players)@{ shape: text } -->  HC
    HC.deal_common_cards(deal_common_cards)@{ shape: text } -->  HC
    HC.reset_hand_cycle_states(reset_hand_cycle_states)@{ shape: text } -->  HC

    BR.get_action_ranges(get_action_ranges)@{ shape: text } --> BR

    T.set_ante(set_ante)@{ shape: text } --> T
    T.set_small_blind(set_small_blind)@{ shape: text } --> T
    T.set_big_blind(set_big_blind)@{ shape: text } --> T
    T.set_button_player(set_button_player)@{ shape: text } --> T
    T.set_small_blind_player(set_small_blind_player)@{ shape: text } --> T
    T.set_big_blind_player(set_big_blind_player)@{ shape: text } --> T
    T.get_next_player(get_next_player)@{ shape: text } --> T
    T.iter_players(iter_players)@{ shape: text } --> T

    P.decrease_bet_level(decrease_bet_level)@{ shape: text } --> P
    P.increase_stack(increase_stack)@{ shape: text } --> P
    P.increase_pot_index(increase_pot_index)@{ shape: text } --> P

    Cd.get_deck_position(get_deck_position)@{ shape: text } --> Cd


    %% Class to method relations
    H --> Cd.get_deck_position

    C --> HC.listen
    C --> HC.close

    C --> BR.get_action_ranges

    C --> T.set_ante
    C --> T.set_small_blind
    C --> T.set_big_blind
    C --> T.set_button_player
    C --> T.set_small_blind_player
    C --> T.set_big_blind_player
    C --> T.get_next_player
    C --> T.iter_players

    T --> P.decrease_bet_level
    T --> P.increase_stack
    T --> P.increase_pot_index


    %% Helper method relations

    HC.listen -.-> HC.close
    HC.listen -.-> HC.deal_cards_to_players
    HC.listen -.-> HC.deal_common_cards
    HC.listen -.-> HC.reset_hand_cycle_states

    HC.close -.-> HC.reset_hand_cycle_states


```


### From hand cycle

```mermaid
flowchart LR


    %% Classes

    HC(HandCycle)@{ shape: circle }
    BR(BettingRound)@{ shape: circle }
    T(Table)@{ shape: circle }
    P(Player)@{ shape: circle }
    H(Hand)@{ shape: circle }
    Cd(Card)@{ shape: circle }
    A(Action)@{ shape: circle }


    %% Container relations

    HC ===> |CONTAINS| BR
    T ===> |CONTAINS| P
    T ===> |CONTAINS| Cd
    P ===> |CONTAINS| H
    P ===> |CONTAINS| Cd
    P ===> |CONTAINS| A
    H ===> |CONTAINS| Cd


    %% Methods

    BR.close(close)@{ shape: text } -->  BR
    BR.listen(listen)@{ shape: text } -->  BR
    BR.reset_betting_round_states(reset_betting_round_states)@{ shape: text } -->  BR

    T.remove_card_from_deck(remove_card_from_deck)@{ shape: text } --> T
    T.reset_deck(reset_deck)@{ shape: text } --> T
    T.assign_common_card(assign_common_card)@{ shape: text } --> T
    T.reset_common_cards(reset_common_cards)@{ shape: text } --> T
    T.set_min_bet(set_min_bet)@{ shape: text } --> T
    T.set_bet_level(set_bet_level)@{ shape: text } --> T
    T.set_full_bet_level(set_full_bet_level)@{ shape: text } --> T
    T.increase_central_pot(increase_central_pot)@{ shape: text } --> T
    T.add_side_pot(add_side_pot)@{ shape: text } --> T
    T.clear_central_pot(clear_central_pot)@{ shape: text } --> T
    T.set_starting_player(set_starting_player)@{ shape: text } --> T
    T.set_button_player(set_button_player)@{ shape: text } --> T
    T.get_next_player(get_next_player)@{ shape: text } --> T
    T.get_previous_player(get_previous_player)@{ shape: text } --> T
    T.gather_pot(gather_pot)@{ shape: text } --> T
    T.refund_excess(refund_excess)@{ shape: text } --> T
    T.iter_players(iter_players)@{ shape: text } --> T

    P.assign_card(assign_card)@{ shape: text } --> P
    P.reset_cards(reset_cards)@{ shape: text } --> P
    P.assign_hand(assign_hand)@{ shape: text } --> P
    P.clear_hand(clear_hand)@{ shape: text } --> P
    P.increase_bet_level(increase_bet_level)@{ shape: text } --> P
    P.decrease_bet_level(decrease_bet_level)@{ shape: text } --> P
    P.increase_stack(increase_stack)@{ shape: text } --> P
    P.decrease_stack(decrease_stack)@{ shape: text } --> P
    P.increase_pot_index(increase_pot_index)@{ shape: text } --> P
    P.reset_pot_index(reset_pot_index)@{ shape: text } --> P
    P.mark_is_folded(mark_is_folded)@{ shape: text } --> P
    P.unmark_is_folded(unmark_is_folded)@{ shape: text } --> P

    Cd.get_deck_position(get_deck_position)@{ shape: text } --> Cd


    %% Class to method relations
    H --> Cd.get_deck_position

    HC --> BR.listen
    HC --> BR.close

    HC --> T.remove_card_from_deck
    HC --> T.reset_deck
    HC --> T.assign_common_card
    HC --> T.reset_common_cards
    HC --> T.set_min_bet
    HC --> T.set_bet_level
    HC --> T.set_full_bet_level
    HC --> T.clear_central_pot
    HC --> T.set_starting_player
    HC --> T.set_button_player
    HC --> T.get_next_player
    HC --> T.gather_pot
    HC --> T.iter_players

    HC --> P.assign_card
    HC --> P.reset_cards
    HC --> P.assign_hand
    HC --> P.clear_hand
    HC --> P.increase_bet_level
    HC --> P.increase_stack
    HC --> P.decrease_stack
    HC --> P.reset_pot_index
    HC --> P.mark_is_folded
    HC --> P.unmark_is_folded

    T --> P.decrease_bet_level
    T --> P.increase_stack
    T --> P.increase_pot_index


    %% Helper method relations

    BR.listen -.-> BR.reset_betting_round_states

    BR.close -.-> BR.listen
    BR.close -.-> BR.reset_betting_round_states

    T.gather_pot -.-> T.increase_central_pot
    T.gather_pot -.-> T.add_side_pot

    T.iter_players -.-> T.get_next_player
    T.iter_players -.-> T.get_previous_player


```


### From betting round

```mermaid
flowchart LR


    %% Classes

    BR(BettingRound)@{ shape: circle }
    T(Table)@{ shape: circle }
    P(Player)@{ shape: circle }
    H(Hand)@{ shape: circle }
    Cd(Card)@{ shape: circle }
    A(Action)@{ shape: circle }


    %% Container relations

    BR ===> |CONTAINS| T
    T ===> |CONTAINS| P
    T ===> |CONTAINS| Cd
    P ===> |CONTAINS| H
    P ===> |CONTAINS| Cd
    P ===> |CONTAINS| A
    H ===> |CONTAINS| Cd


    %% Methods

    T.set_min_bet(set_min_bet)@{ shape: text } --> T
    T.set_min_raise_increase(set_min_raise_increase)@{ shape: text } --> T
    T.set_bet_level(set_bet_level)@{ shape: text } --> T
    T.set_full_bet_level(set_full_bet_level)@{ shape: text } --> T
    T.increase_central_pot(increase_central_pot)@{ shape: text } --> T
    T.add_side_pot(add_side_pot)@{ shape: text } --> T
    T.set_starting_player(set_starting_player)@{ shape: text } --> T
    T.set_stopping_player(set_stopping_player)@{ shape: text } --> T
    T.set_current_player(set_current_player)@{ shape: text } --> T
    T.get_next_player(get_next_player)@{ shape: text } --> T
    T.get_previous_player(get_previous_player)@{ shape: text } --> T
    T.gather_pot(gather_pot)@{ shape: text } --> T
    T.refund_excess(refund_excess)@{ shape: text } --> T
    T.iter_players(iter_players)@{ shape: text } --> T

    P.clear_action(clear_action)@{ shape: text } --> P
    P.assign_card(assign_card)@{ shape: text } --> P
    P.assign_hand(assign_hand)@{ shape: text } --> P
    P.increase_bet_level(increase_bet_level)@{ shape: text } --> P
    P.decrease_bet_level(decrease_bet_level)@{ shape: text } --> P
    P.increase_stack(increase_stack)@{ shape: text } --> P
    P.decrease_stack(decrease_stack)@{ shape: text } --> P
    P.increase_pot_index(increase_pot_index)@{ shape: text } --> P
    P.mark_has_played(mark_has_played)@{ shape: text } --> P
    P.unmark_has_played(unmark_has_played)@{ shape: text } --> P
    P.mark_is_folded(mark_is_folded)@{ shape: text } --> P

    Cd.get_deck_position(get_deck_position)@{ shape: text } --> Cd


    %% Class to method relations

    H --> Cd.get_deck_position

    BR --> T.set_min_bet
    BR --> T.set_min_raise_increase
    BR --> T.set_bet_level
    BR --> T.set_full_bet_level
    BR --> T.increase_central_pot
    BR --> T.add_side_pot
    BR --> T.set_starting_player
    BR --> T.set_stopping_player
    BR --> T.set_current_player
    BR --> T.get_previous_player
    BR --> T.gather_pot
    BR --> T.refund_excess
    BR --> T.iter_players

    BR --> P.clear_action
    BR --> P.assign_card
    BR --> P.assign_hand
    BR --> P.increase_bet_level
    BR --> P.decrease_bet_level
    BR --> P.decrease_stack
    BR --> P.increase_pot_index
    BR --> P.mark_has_played
    BR --> P.unmark_has_played
    BR --> P.mark_is_folded

    T --> P.decrease_bet_level
    T --> P.increase_stack
    T --> P.increase_pot_index


    %% Helper method relations

    T.gather_pot -.-> T.increase_central_pot
    T.gather_pot -.-> T.add_side_pot

    T.iter_players -.-> T.get_next_player
    T.iter_players -.-> T.get_previous_player


```
