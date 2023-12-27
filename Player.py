from Move import Move

class Player:
    def __init__(self, name, strategy):
        """
        Initialize a new player with a given name.

        :param name: The name of the player.
        :param strategy: Whether the player is human or not.
        """
        self.name = name
        self.hand = []
        self.reachable = True
        self.strategy = strategy
        self.has_played_or_discarded_spy = False
        self.player_memory = []
        self.deck_memory = []


    def draw(self, card):
        """
        Add a card to the player's hand.

        :param card: The card to be added to the hand.
        """
        if card is not None:
            self.hand.append(card)


    def choose_card_to_play(self, game):
        """
        Choose a card to play according to the player's strategy.

        :return: The chosen card.
        """
        choosen_card = self.strategy.choose_card_to_play(self, game)
        self.hand.remove(choosen_card)
        return choosen_card


    def card(self):
        """
        Return the first and only card from the player's hand.

        :return: The first and only card from the hand.
        """
        if self.hand:
            return self.hand[0]
        else:
            return None


    def discard(self):
        """
        Remove and return the last card from the player's hand.

        :return: The last card from the hand.
        """
        if self.hand:
            return self.hand.pop()
        else:
            return None


    def keep_card(self, cards, game):
        """
        Choose a card to keep after playing the "Chancellor" card, according to the player's strategy.

        :param cards: The list of cards to choose from.

        :return: The chosen card.
        """
        return self.strategy.keep_card(self, cards, game)


    def countess(self):
        """
        :return: Whether the player has the "Countess" card and a "King" or "Prince" card in hand.
        """
        has_comtesse = any(card.name == "Comtesse" for card in self.hand)
        has_king_or_prince = any(card.name in ["King", "Prince"] for card in self.hand)
        return has_comtesse and has_king_or_prince


    def choose_target_player(self, players, game):
        """
        Choose a target player to use a card on, according to the player's strategy.

        :param players: The list of players to choose from.

        :return: The chosen player.
        """
        available_players = [p for p in players if p != self and p.reachable and p.hand]
        return self.strategy.choose_target_player(self, available_players, game)


    def choose_character(self, game):
        """
        Choose a character to guess because of the "Guard" card, according to the player's strategy.

        :return: The chosen character.
        """
        # List of all possible characters
        possible_characters = ["Spy", "Priest", "Baron", "Handmaid", "Prince", "Chancellor", "King",
                                 "Countess", "Princess"]
        return self.strategy.choose_character(self, possible_characters, game)

    def get_possible_moves(self, all_players):
        """
        Get a list of possible moves for the player in the current game state.

        :param all_players: A list of all players in the game.

        :return: A list of possible moves. Each move is represented as a tuple (action, card, target),
                 where 'action' is either 'play' or 'discard', 'card' is the card to be played or discarded,
                 and 'target' is the target player or -1 (no specific target).
        """
        possible_moves = []

        if self.hand:
            for card in self.hand:
                # Check if the card has a specific target
                if card.name == "Guard":
                    targetable_players = [p for p in all_players if p != self and p.reachable and p.hand]
                    for target_player in targetable_players:
                        for character in ['Spy', 'Priest', 'Baron', 'Handmaid', 'Prince', 'Chancellor', 'King', 'Countess', 'Princess']:
                            possible_moves.append(Move(card, target_player, character, None))
                elif card.name == "Priest" or card.name == "Baron" or card.name == "King":
                    targetable_players = [p for p in all_players if p != self and p.reachable and p.hand]
                    for target_player in targetable_players:
                        possible_moves.append(Move(card, target_player, None, None))
                elif card.name == "Prince":
                    targetable_players = [p for p in all_players if p.reachable and p.hand]
                    for target_player in targetable_players:
                        possible_moves.append(Move(card, target_player, None, None))
                elif card.name == "Chancellor":
                    for character in ['Spy', 'Guard', 'Priest', 'Baron', 'Handmaid', 'Prince', 'Chancellor', 'King', 'Countess', 'Princess']:
                        possible_moves.append(Move(card, None, None, character))
                else:
                    possible_moves.append(Move(card, None, None, None))

        return possible_moves

    def remember_player_card(self, card):
        """
        Remember a card that the player saw in another player's hand.

        :param card: The card that the player saw.

        """
        self.player_memory.append(card)

    def forget_player_card(self, card):
        """
        Erase the card from the memory of all players

        :param card: The card to be erased from the memory.
        """
        for c in self.player_memory:
            if card.name == c.name:
                self.player_memory.remove(card)



    def __str__(self):
        """
        Return a string representation of the player.
        """
        return f"{self.name} has the hand: {', '.join(str(card) for card in self.hand)}"