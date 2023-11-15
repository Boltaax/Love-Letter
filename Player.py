import random

class Player:
    def __init__(self, name):
        """
        Initialize a new player with a given name.

        :param name: The name of the player.
        """
        self.name = name
        self.hand = []
        self.reachable = True
        self.has_played_or_discarded_spy = False

    def draw(self, card):
        """
        Add a card to the player's hand.

        :param card: The card to be added to the hand.
        """
        if card is not None:
            self.hand.append(card)

    def play_random_card(self):
        """
        Remove and return a random card from the player's hand.
        Renamed from play_best_card to better reflect its functionality.

        :return: A randomly selected card from the hand.
        """
        if self.hand:
            return self.hand.pop(random.randint(0, len(self.hand) - 1))
        else:
            return None

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

    def choose_card_to_keep(self, cards):
        return cards[random.randint(0, len(cards)-1)]

    def countess(self):
        # Check if the player has the "Countess" card and a "King" or "Prince" card in their hand
        has_comtesse = any(card.name == "Comtesse" for card in self.hand)
        has_king_or_prince = any(card.name in ["King", "Prince"] for card in self.hand)
        return has_comtesse and has_king_or_prince
