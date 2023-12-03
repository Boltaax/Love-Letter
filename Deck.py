from Cards import Card
import random


class Deck:
    def __init__(self):
        """
        Initialize a new deck of cards.
        """
        self.draw_pile = []
        self.fill()


    def fill(self):
        """
        Fill the deck with the standard set of LoveLetter cards.
        """
        self.draw_pile = (
            [Card("Spy", 0)] * 2 +
            [Card("Guard", 1)] * 6 +
            [Card("Priest", 2)] * 2 +
            [Card("Baron", 3)] * 2 +
            [Card("Handmaid", 4)] * 2 +
            [Card("Prince", 5)] * 2 +
            [Card("Chancellor", 6)] * 2 +
            [Card("King", 7)] +
            [Card("Countess", 8)] +
            [Card("Princess", 9)]
        )


    def shuffle(self):
        """
        Shuffle the deck.
        """
        random.shuffle(self.draw_pile)


    def draw(self):
        """
        Draw a card from the top of the deck.
        
        :return: The drawn card, or None if the deck is empty.
        """
        if self.draw_pile:
            return self.draw_pile.pop()
        else:
            return None
