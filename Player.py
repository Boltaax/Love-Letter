import random

class Player:
    def __init__(self, name):
        self.name = name
        self.hand = []
        self.reachable = True

    def draw(self, card):
        self.hand.append(card)

    def play_best_card(self):
        return self.hand.pop(random.randint(0, 1))

    def show_card(self):
        return self.hand[0]

    def throw(self):
        card = self.hand.pop()
        #   print(self.name, " had ", card.name, " in their hand!")
        return card

    def choose_card_to_keep(self, cards):
        return cards[random.randint(0, len(cards)-1)]

    def comtesse(self):
        # Check if the player has the "Comtesse" card and a "King" or "Prince" card in their hand
        has_comtesse = any(card.name == "Comtesse" for card in self.hand)
        has_king_or_prince = any(card.name in ["King", "Prince"] for card in self.hand)
        return has_comtesse and has_king_or_prince
