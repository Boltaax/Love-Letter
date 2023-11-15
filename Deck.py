from Cards import Card
import random

class Deck:
    def __init__(self):
        self.draw_pile = []

    def fill(self):
        self.deck = (
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
        random.shuffle(self.deck)

    def draw(self):
        return self.deck.pop(0)
