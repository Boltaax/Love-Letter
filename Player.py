from player_strategies import RandomStrategy, HumanStrategy


class Player:
    def __init__(self, name, strategy):
        """
        Initialize a new player with a given name.

        :param name: The name of the player.
        :param is_human: Whether the player is human or not.
        """
        self.name = name
        self.hand = []
        self.reachable = True
        self.strategy = strategy
        self.has_played_or_discarded_spy = False


    def draw(self, card):
        """
        Add a card to the player's hand.

        :param card: The card to be added to the hand.
        """
        if card is not None:
            self.hand.append(card)


    def choose_card_to_play(self):
        """
        Choose a card to play according to the player's strategy.

        :return: The chosen card.
        """
        choosen_card = self.strategy.choose_card_to_play(self)
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


    def keep_card(self, cards):
        """
        Choose a card to keep after playing the "Chancellor" card, according to the player's strategy.

        :param cards: The list of cards to choose from.

        :return: The chosen card.
        """
        return self.strategy.keep_card(self, cards)


    def countess(self):
        """
        :return: Whether the player has the "Countess" card and a "King" or "Prince" card in hand.
        """
        has_comtesse = any(card.name == "Comtesse" for card in self.hand)
        has_king_or_prince = any(card.name in ["King", "Prince"] for card in self.hand)
        return has_comtesse and has_king_or_prince


    def choose_target_player(self, players):
        """
        Choose a target player to use a card on, according to the player's strategy.

        :param players: The list of players to choose from.

        :return: The chosen player.
        """
        available_players = [p for p in players if p != self and p.reachable and p.hand]
        return self.strategy.choose_target_player(self, available_players)


    def choose_character(self):
        """
        Choose a character to guess because of the "Guard" card, according to the player's strategy.

        :return: The chosen character.
        """
        # List of all possible characters
        possible_characters = ["Spy", "Priest", "Baron", "Handmaid", "Prince", "Chancellor", "King",
                                 "Countess", "Princess"]
        return self.strategy.choose_character(self, possible_characters)


    def __str__(self):
        """
        Return a string representation of the player.
        """
        return f"{self.name}"