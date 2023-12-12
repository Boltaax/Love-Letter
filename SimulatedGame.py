from copy import deepcopy
from Game import LoveLetterGame
from Move import Move

class LoveLetterSimulatedGame(LoveLetterGame):
    def __init__(self, original_game):
        super().__init__(original_game.players)
        self.deck = deepcopy(original_game.deck)
        self.discarded_cards = original_game.discarded_cards
        self.points = deepcopy(original_game.points)
        self.active_player = original_game.active_player
        self.spy_count = original_game.spy_count
        self.verbose = False  # Set to True for debugging if needed

    def simulate_play_card(self, player, move):
        """
        Simulate the effects of a player playing a card.

        :param player: The player who is playing the card.
        :param move: The move the player is playing.

        :return: The simulated game state after playing the card.
        """
        # Create a deep copy of the current game state
        simulated_game = deepcopy(self)

        print(f"Simulated played moove : card: {move.card} target: ({move.target}) character: {move.character} keep: {move.keep}")

        # Find the player in the simulated game
        simulated_player = next(p for p in simulated_game.players if p.name == player.name)

        played_card = next(card for card in simulated_player.hand if card.name == move.card.name)

        # Remove the played card from the player's hand
        simulated_player.hand.remove(played_card)

        # Simulate the effect of the played card
        simulated_game.resolve_effect(move)

        # Check if the round should end
        if simulated_game.is_round_end():
            simulated_game.end_of_round()

        return simulated_game

    def resolve_effect(self, move):
        """
        Resolve the effect of the played card.
        """
        effect_method = self.get_effect_method(move)

        if effect_method:
            effect_method()

    def get_effect_method(self, move):
        """
        Return the method corresponding to the card's effect.
        """
        return {
            "Spy": self.effect_spy,
            "Guard": self.effect_guard_s(move),
            "Priest": self.effect_priest_s(move),
            "Baron": self.effect_baron_s(move),
            "Handmaid": self.effect_handmaid,
            "Prince": self.effect_prince_s(move),
            "Chancellor": self.effect_chancellor_s(move),
            "King": self.effect_king_s(move),
            "Countess": self.effect_countess,
            "Princess": self.effect_princess
        }.get(move.card.name, None)

    def effect_guard_s(self, move):
        """
        Effect of the Guard card: guess a character, if correct, the target player is eliminated from the round.
        """
        target_player = move.target
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
        target_player = move.target
        if target_player:
            self.log(f"{self.active_player.name} chooses {target_player.name} as target and looks at {target_player.card().name}")
            self.active_player.remember_card(target_player.name, target_player.card())
        else:
            self.log("No player is targetable, the card has no effect!")

    def effect_baron_s(self, move):
        """
        Effect of the Baron card: compare the target player's card with the current player's card.
        The player with the lower value card is eliminated from the round.
        """
        target_player = move.target
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
        target_player = move.target
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
            self.log(f"{self.active_player.name} draws {len(drawn_cards)} card(s): {[card.name for card in drawn_cards]}")

            card_to_keep = self.active_player.hand[move.keep]
            self.log(f"{self.active_player.name} keeps the {card_to_keep.name} card ({card_to_keep.value}).")
            self.return_cards_to_deck(drawn_cards, card_to_keep)

    def effect_king_s(self, move):
        """
        Effect of the King card: the current player exchanges his/her card with the target player's card.
        """
        target_player = move.target
        if not target_player:
            self.log("No player is targetable, the card has no effect!")
            return

        self.exchange_cards(self.active_player, target_player)

    def get_possible_moves(self, card, all_players, player):
        """
        Get a list of possible moves for the player in the current game state.

        :param card: the card that have all these possible moves

        :param player: the player whose it the turn to play.

        :param all_players: A list of all players in the game.

        :return: A list of possible moves. Each move is represented as a tuple (action, card, target),
                 where 'action' is either 'play' or 'discard', 'card' is the card to be played or discarded,
                 and 'target' is the target player or -1 (no specific target).
        """
        possible_moves = []

        # Check if the card has a specific target
        if card.name == "Guard":
            targetable_players = [p for p in all_players if p != player and p.reachable and p.hand]
            if targetable_players:
                for target_player in targetable_players:
                    for character in ['Spy', 'Priest', 'Baron', 'Handmaid', 'Prince', 'Chancellor', 'King', 'Countess', 'Princess']:
                        possible_moves.append(Move(card, target_player, character, None))
            else:
                possible_moves.append(Move(card, None, None, None))
        elif card.name == "Priest" or card.name == "Baron" or card.name == "King":
            targetable_players = [p for p in all_players if p != player and p.reachable and p.hand]
            if targetable_players:
                for target_player in targetable_players:
                    possible_moves.append(Move(card, target_player, None, None))
            else:
                possible_moves.append(Move(card, None, None, None))
        elif card.name == "Prince":
            targetable_players = [p for p in all_players if p.reachable and p.hand]
            for target_player in targetable_players:
                possible_moves.append(Move(card, target_player, None, None))
        elif card.name == "Chancellor":
            for i in range(3):
                possible_moves.append(Move(card, None, None, i))
        else:
            possible_moves.append(Move(card, None, None, None))

        return possible_moves

