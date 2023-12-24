from Deck import Deck

class LoveLetterGame:
    def __init__(self, players, verbose=False):
        # TODO: Add GUI support
        """
        Initialize a new LoveLetter game with the given players.

        :param players: A list of Player objects participating in the game.
        :param verbose: If True, the game will print detailed information about each turn.
        """
        self.players = players
        self.deck = Deck()
        self.deck.fill()
        self.deck.shuffle()
        self.target_points = 6 - max(0, len(players) - 2) if len(players) <= 5 else 3 # Points to win the game (6 for 2 players, 5 for 3 players, 4 for 4 players, 3 for 5-6 players)
        self.points = {player: 0 for player in players}
        self.active_player = players[0] # The player whose turn it is
        self.spy_count = 0 # Tracks the number of Spy cards played
        self.verbose = verbose
        self.discarded_cards = {}

        # Check if the number of players is valid
        if len(players) > 6 or len(players) < 2:
            raise ValueError("The number of players should be between 2 and 6.")


    def distribute_cards(self):
        """
        Distribute one card to each player from the deck at the start of the game.
        """
        for player in self.players:
            player.draw(self.deck.draw())

    def draw_memory(self, player, drawn_card):
        """
            :param player : the player who draws a card

            :param drawn_card : the card that were drawn

            Récupère dans la mémoire de l'autre joueur la 1ère carte du deck et l'ajoute à la memoire player
            Ensuite, pour chaque joueur, enlève la première valeur du tableau deck memory
        """
        op = self.get_other_player(player)
        if op.deck_memory:
            op.player_memory.append(drawn_card.name)
        for p in self.players:
            if p.deck_memory:
                p.deck_memory.pop(0)


    def get_other_player(self, player):
        return next(p for p in self.players if p != player)


    def play_turn(self):
        """
        Conduct a single turn in the game.
        """
        for current_player in self.players:
            self.active_player = current_player
            if self.is_round_end():
                self.end_of_round()
                break

            self.handle_player_turn(current_player)


    def is_round_end(self):
        """
        Check if the round should end based on the game state.

        :return: Boolean indicating if the round should end.
        """
        return len([player for player in self.players if player.hand]) <= 1 or not self.deck.draw_pile

    def is_round_over(self):
        """
        Check if the round is over based on the game state.
        """
        return len(self.deck.draw_pile) == 0 or len([p for p in self.players if p.hand]) == 1
    

    def handle_player_turn(self, player):
        """
        Handle the actions of a player during their turn.

        :param player: The current player.
        """
        if not player.reachable:
            player.reachable = True  # Make the player reachable again

        if player.hand and self.deck.draw_pile:
            self.execute_player_action(player)
        elif not self.deck.draw_pile:
            self.end_of_round()

    
    def execute_player_action(self, player):
        """
        Execute the action of the player, including drawing and playing a card.

        :param player: The current player.
        """
        # Player draws a card from the deck
        drawn_card = self.deck.draw()
        player.draw(drawn_card)
        self.draw_memory(player, drawn_card)
        if self.verbose:
            print(f"{player.name} draws a card.")

        # Handling the special case of the Countess card
        if player.countess():
            self.handle_countess_play(player)
        else:
            # Player chooses a card to play
            played_card = player.choose_card_to_play(self)
            if played_card:
                if self.verbose:
                    print(f"{player.name} plays the {played_card.name} card.")
                self.update_discarded_cards_count(played_card)
                self.resolve_effect(played_card)
                player.erase_memory(self.players, played_card)


    
    def handle_countess_play(self, player):
        """
        Handle the scenario where the player has the Countess card and needs to play it.

        :param player: The current player.
        """
        for card in player.hand:
            if card.name == "Countess":
                self.update_discarded_cards_count(player.hand.pop(player.hand.index(card)))
                player.erase_memory(self.players, card)
                if self.verbose:
                    print(f"{player.name} is forced to play the Countess card.")
                break


    def resolve_effect(self, card):
        """
        Resolve the effect of the played card.
        """
        effect_method = self.get_effect_method(card.name)
        if effect_method:
            effect_method()


    def get_effect_method(self, card_name):
        """
        Return the method corresponding to the card's effect.
        """
        return {
            "Spy": self.effect_spy,
            "Guard": self.effect_guard,
            "Priest": self.effect_priest,
            "Baron": self.effect_baron,
            "Handmaid": self.effect_handmaid,
            "Prince": self.effect_prince,
            "Chancellor": self.effect_chancellor,
            "King": self.effect_king,
            "Countess": self.effect_countess,
            "Princess": self.effect_princess
        }.get(card_name, None)
    

    def effect_spy(self):
        """
        Effect of the Spy card: no active effect.
        The only remaining player to have played or discarded a spy, if any, wins 1 bonus point.
        """

        current_player = self.active_player
        current_player.has_played_or_discarded_spy = True


    def effect_guard(self):
        """
        Effect of the Guard card: guess a character, if correct, the target player is eliminated from the round.
        """
        target_player = self.active_player.choose_target_player(self.players, self)
        if not target_player:
            self.log("No player is targetable, the card has no effect!")
            return

        guessed_character = self.active_player.choose_character(self)
        self.log(f"{self.active_player.name} chooses {target_player.name} as target and guesses {guessed_character}")

        if guessed_character in [c.name for c in target_player.hand]:
            self.log("The guess is correct. The target player is eliminated from the round.")
            target_player.hand = []
        else:
            self.log("The guess is incorrect. Nothing happens.")


    def effect_priest(self):
        """
        Effect of the Priest card: look at the target player's card.
        """
        target_player = self.active_player.choose_target_player(self.players, self)
        if target_player:
            self.log(f"{self.active_player.name} chooses {target_player.name} as target and looks at {target_player.card().name}")
            self.active_player.remember_player_card(target_player.card())
        else:
            self.log("No player is targetable, the card has no effect!")


    def effect_baron(self):
        """
        Effect of the Baron card: compare the target player's card with the current player's card.
        The player with the lower value card is eliminated from the round.
        """
        target_player = self.active_player.choose_target_player(self.players, self)
        if not target_player:
            self.log("No player is targetable, the card has no effect!")
            return

        current_player_card = self.active_player.card()
        target_player_card = target_player.card()
        self.log_duel_info(current_player_card, target_player_card)

        if current_player_card.value > target_player_card.value:
            self.eliminate_player(target_player)
        elif current_player_card.value < target_player_card.value:
            self.eliminate_player(self.active_player)
        else:
            self.log("Tie, no one loses the round.")


    def effect_handmaid(self):
        """
        Effect of the Handmaid card: the current player cannot be targeted by other players for a turn.
        """
        self.active_player.reachable = False
        self.log(f"{self.active_player.name} is not targetable for a turn!")


    def effect_prince(self):
        """
        Effect of the Prince card: the target player discards his/her card and draws a new one.
        """
        target_player = self.active_player.choose_target_player(self.players, self)
        if not target_player or not self.deck.draw_pile:
            self.log("No player is targetable, or deck is empty. The card has no effect!")
            return

        self.log(f"{self.active_player.name} chooses {target_player.name}")
        self.discard_and_draw(target_player)


    def effect_chancellor(self):
        """
        Effect of the Chancellor card: the current player draws 2 cards from the deck.
        One of the cards is kept, the others are returned to the deck.
        """
        if len(self.deck.draw_pile) < 2:
            self.log("Not enough cards in the deck to draw.")
            return

        drawn_cards = [self.deck.draw(), self.deck.draw()]
        for c in drawn_cards:
            self.draw_memory(self.active_player, c)
        self.log(f"{self.active_player.name} draws {len(drawn_cards)} card(s): {[card.name for card in drawn_cards]}")

        card_to_keep = self.active_player.keep_card(drawn_cards, self)
        self.log(f"{self.active_player.name} keeps the {card_to_keep.name} card ({card_to_keep.value}).")

        op = self.get_other_player(self.active_player)
        op.player_memory = []

        drawn_cards.append(self.active_player.hand.pop())
        self.return_cards_to_deck(drawn_cards, card_to_keep)



    def effect_king(self):
        """
        Effect of the King card: the current player exchanges his/her card with the target player's card.
        """
        target_player = self.active_player.choose_target_player(self.players, self)
        if not target_player:
            self.log("No player is targetable, the card has no effect!")
            return

        self.exchange_cards(self.active_player, target_player)

    def effect_countess(self):
        """
        Effect of the Countess card: no additional effect.
        """
        pass


    def effect_princess(self):
        """
        Effect of the Princess card: the current player is eliminated from the round if he/she plays or discards the card.
        """
        current_player = self.active_player
        self.eliminate_player(current_player)
        self.log(f"{current_player.name} played the Princess and is eliminated from the round.")


    def log(self, message):
        """
        Print the given message if verbose mode is enabled.
        """
        if self.verbose:
            print(message)


    def log_duel_info(self, card1, card2):
        """
        Print the cards of the two players involved in a duel.
        """
        self.log(f"{self.active_player.name} has the {card1.name} card ({card1.value}).")
        self.log(f"Target player has the {card2.name} card ({card2.value}).")


    def eliminate_player(self, player):
        """
        Eliminate the given player from the round.
        """
        self.log(f"{player.name} loses the round.")
        player.hand = []


    def discard_and_draw(self, player):
        """
        Discard the target player's card and draw a new one.
        """
        discarded_card = player.discard()
        if discarded_card:
            self.handle_discarded_card(discarded_card, player)
            player.forget_player_card(discarded_card)
            if discarded_card.name != "Princess":
                player.draw(self.deck.draw())
            self.update_discarded_cards_count(discarded_card)


    def handle_discarded_card(self, card, player):
        """
        Handle the effect of the discarded card.
        """
        self.log(f"{player.name} discards the {card.name} card")
        if card.name == "Spy":
            player.has_played_or_discarded_spy = True
        elif card.name == "Princess":
            self.log(f"{player.name} discarded the Princess and is eliminated from the round.")
            player.hand = []


    def return_cards_to_deck(self, drawn_cards, card_to_keep):
        """
        Return the cards to the deck, except the one the player chose to keep.
        """
        cards_to_return = [card for card in drawn_cards if card != card_to_keep]
        self.active_player.hand.append(card_to_keep)
        self.active_player.deck_memory.extend(cards_to_return)
        op = self.get_other_player(self.active_player)
        op.deck_memory.extend(['unknown', 'unknown'])
        self.deck.draw_pile.extend(cards_to_return)


    def exchange_cards(self, player1, player2):
        """
        Exchange the cards of the two players.
        """
        card1 = player1.card()
        card2 = player2.card()

        self.log(f"{player1.name} and {player2.name} exchange their cards.")
        player1.hand.remove(card1)
        player2.hand.remove(card2)
        player1.hand.append(card2)
        player2.hand.append(card1)

        player1.remember_player_card(card1)
        player1.forget_player_card(card2)
        player2.remember_player_card(card2)
        player1.forget_player_card(card1)


    def end_of_round(self):
        """
        Handle the end of the round.
        """
        if self.is_round_over():
            winning_players = self.determine_round_winners()
            self.award_points(winning_players)
            self.log_round_results(winning_players)
            self.new_round()

    def determine_round_winners(self):
        """
        Determine the winner(s) of the round.
        """
        players_in_game = [p for p in self.players if p.hand]
        max_card_value = max(max(p.hand, key=lambda c: c.value).value for p in players_in_game)
        return [p for p in players_in_game if max(p.hand, key=lambda c: c.value).value == max_card_value]


    def award_points(self, winners):
        """
        Award points to the winner(s) of the round.
        """
        for player in winners:
            if player not in self.points:
                self.points[player] = 0
            self.points[player] += 1
            self.log(f"{player.name} wins the round and gets 1 point!")

        self.award_spy_bonus()


    def log_round_results(self, winners):
        """
        Print the results of the round.
        """
        self.log(f"Round winners: {', '.join(p.name for p in winners)}")
        self.log(f"Current points: {', '.join(f'{p.name}: {self.points[p]}' for p in self.players)}")


    def award_spy_bonus(self):
        """
        Award a bonus point to the only player to have played or discarded a Spy card, if any.
        """
        spy_players = [p for p in self.players if p.has_played_or_discarded_spy and p.hand]
        if len(spy_players) == 1:
            self.points[spy_players[0]] += 1
            self.log(f"{spy_players[0].name} gets 1 bonus point for being the only player to play or discard a Spy card at the end of the round.")


    def new_round(self):
        """
        Start a new round.
        """
        self.deck = Deck()
        self.deck.fill()
        self.deck.shuffle()
        self.reset_players_for_new_round()
        self.distribute_cards()
        self.active_player = self.players[0]


    def reset_players_for_new_round(self):
        """
        Reset the players for a new round.
        """
        for player in self.players:
            player.hand = []
            player.player_memory = []
            player.deck_memory = []
            player.has_played_or_discarded_spy = False
            player.reachable = True

    def update_discarded_cards_count(self, card):
        """
        Update the count of discarded cards.
        """
        if card.name in self.discarded_cards:
            self.discarded_cards[card.name] += 1
        else:
            self.discarded_cards[card.name] = 1


    def initiate_deck_memory(self):
        for player in self.players:
            player.deck_memory = ['unknown'] * len(self.deck.draw_pile)





