from copy import deepcopy
from Game import LoveLetterGame
from Move import Move

class LoveLetterSimulatedGame(LoveLetterGame):
    def __init__(self, original_game):
        super().__init__(original_game.players)
        self.players = deepcopy(original_game.players)
        self.deck = deepcopy(original_game.deck)
        self.discarded_cards = deepcopy(original_game.discarded_cards)
        self.points = deepcopy(original_game.points)
        self.active_player = deepcopy(original_game.active_player)
        self.spy_count = deepcopy(original_game.spy_count)
        self.verbose = False  # Set to True for debugging if needed

    def simulate_player_turn(self, player, move):
        """
        Simulate a player's turn.

        :param player: The player whose turn is being simulated.
        :param move: The move the player is making.

        :return: The simulated game state after the player's turn.
        """
        # Create a deep copy of the current game state
        # Find the player in the simulated game
        simulated_player = next(p for p in self.players if p.name == player.name)
        simulated_player.hand = player.hand.copy()
        self.active_player = simulated_player

        # Simulate the effect of the player's turn
        self.resolve_player_turn(simulated_player, move)
        op = self.get_other_player(simulated_player)

        # Check if the round has ended
        if self.is_round_end():
            return self
        # Else, we are doing all the things necessary for the next player simulated turn
        else:
            self.active_player = op
            self.active_player.reachable = True
            drawn_card = self.deck.draw()
            self.active_player.draw(drawn_card)
            self.draw_memory(self.active_player, drawn_card)
            return self


    def resolve_player_turn(self, player, move):
        """
        Resolve the effects of a player's turn.

        :param player: The player whose turn is being resolved.
        :param move: The move the player is making.
        """
        if move.card:
            played_card = next(card for card in player.hand if card.name == move.card.name)
            player.hand.remove(played_card)
            op = self.get_other_player(player)
            op.forget_player_card(played_card)
            self.resolve_effect(move)


    def resolve_effect(self, move):
        """
        Resolve the effect of the played card.
        """
        effect_method = self.get_effect_method(move)

        if effect_method:
            if move.card.name == "Spy" or move.card.name == "Handmaid" or move.card.name == "Countess" or move.card.name == "Princess":
                effect_method()
            else:
                effect_method(move)

    def get_effect_method(self, move):
        """
        Return the method corresponding to the card's effect.
        """
        return {
            "Spy": self.effect_spy,
            "Guard": self.effect_guard_s,
            "Priest": self.effect_priest_s,
            "Baron": self.effect_baron_s,
            "Handmaid": self.effect_handmaid,
            "Prince": self.effect_prince_s,
            "Chancellor": self.effect_chancellor_s,
            "King": self.effect_king_s,
            "Countess": self.effect_countess,
            "Princess": self.effect_princess
        }.get(move.card.name, None)

    def effect_guard_s(self, move):
        """
        Effect of the Guard card: guess a character, if correct, the target player is eliminated from the round.
        """

        target_player = None
        for player in self.players:
            if move.target:
                if player.name == move.target.name:
                    target_player = player
        if not target_player:
            self.log("No player is targetable, the card has no effect!")
            return

        guessed_character = move.character
        self.log(f"{self.active_player.name} chooses {target_player.name} as target and guesses {guessed_character}")

        if guessed_character in [c.name for c in target_player.hand]:
            self.log("The guess is correct. The target player is eliminated from the round.")
            target_player.hand = []
        else:
            self.log("The guess is incorrect. Nothing happens.")

    def effect_priest_s(self, move):
        """
        Effect of the Priest card: look at the target player's card.
        """

        target_player = None
        for player in self.players:
            if move.target:
                if player.name == move.target.name:
                    target_player = player
        if target_player:
            self.log(f"{self.active_player.name} chooses {target_player.name} as target and looks at {target_player.card().name}")
            self.active_player.remember_player_card(target_player.card())
        else:
            self.log("No player is targetable, the card has no effect!")

    def effect_baron_s(self, move):
        """
        Effect of the Baron card: compare the target player's card with the current player's card.
        The player with the lower value card is eliminated from the round.
        """
        target_player = None
        for player in self.players:
            if move.target:
                if player.name == move.target.name:
                    target_player = player
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

    def effect_prince_s(self, move):
        """
        Effect of the Prince card: the target player discards his/her card and draws a new one.
        """
        target_player = None
        for player in self.players:
            if move.target:
                if player.name == move.target.name:
                    target_player = player
        if not target_player or not self.deck.draw_pile:
            self.log("No player is targetable, or deck is empty. The card has no effect!")
            return

        self.log(f"{self.active_player.name} chooses {target_player.name}")
        self.discard_and_draw(target_player)

    def effect_chancellor_s(self, move):
        """
        Effect of the Chancellor card: the current player draws 2 cards from the deck.
        One of the cards is kept, the others are returned to the deck.
        """

        if len(self.deck.draw_pile) < 2:
            self.log("Not enough cards in the deck to draw.")
            return
        if move.keep:
            drawn_cards = [self.deck.draw(), self.deck.draw()]
            for c in drawn_cards:
                self.active_player.draw(c)
                self.draw_memory(self.active_player, c)

            self.log(f"{self.active_player.name} draws {len(drawn_cards)} card(s): {[card.name for card in drawn_cards]}")

            card_to_keep = self.active_player.hand[move.keep]
            self.log(f"{self.active_player.name} keeps the {card_to_keep.name} card ({card_to_keep.value}).")
            self.return_cards_to_deck(drawn_cards, card_to_keep)

    def effect_king_s(self, move):
        """
        Effect of the King card: the current player exchanges his/her card with the target player's card.
        """

        target_player = None
        for player in self.players:
            if move.target:
                if player.name == move.target.name:
                    target_player = player
        if not target_player:
            self.log("No player is targetable, the card has no effect!")
            return

        self.exchange_cards(self.active_player, target_player)

    def get_possible_moves(self, player):
        """
        Get a list of possible moves for the player in the current game state.

        :param player: the player whose it the turn to play.

        :return: A list of possible moves. Each move is represented as a tuple (action, card, target),
                 where 'action' is either 'play' or 'discard', 'card' is the card to be played or discarded,
                 and 'target' is the target player or None (no specific target).
        """
        op = self.get_other_player(player)
        possible_moves = []
        for card in player.hand:
            # Check if the card has a specific target
            if card.name == "Guard":
                targetable_players = [op] if op.reachable and op.hand else []
                if targetable_players:
                    for target_player in targetable_players:
                        for character in ['Spy', 'Priest', 'Baron', 'Handmaid', 'Prince', 'Chancellor', 'King', 'Countess', 'Princess']:
                            possible_moves.append(Move(card, target_player, character, None))
                else:
                    possible_moves.append(Move(card, None, None, None))
            elif card.name == "Priest" or card.name == "Baron" or card.name == "King":
                targetable_players = [op] if op.reachable and op.hand else []
                if targetable_players:
                    for target_player in targetable_players:
                        possible_moves.append(Move(card, target_player, None, None))
                else:
                    possible_moves.append(Move(card, None, None, None))
            elif card.name == "Prince":
                targetable_players = [p for p in self.players if p.reachable and p.hand]
                for target_player in targetable_players:
                    possible_moves.append(Move(card, target_player, None, None))
            elif card.name == "Chancellor":
                for i in range(3):
                    possible_moves.append(Move(card, None, None, i))
            else:
                possible_moves.append(Move(card, None, None, None))
        return possible_moves



