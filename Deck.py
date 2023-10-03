from Cards import Carte
import random

class Deck:
    def __init__(self):
        self.pioche = []

    def remplir_pioche(self):
        self.pioche = (
            [Carte("Espionne", 0)] * 2 +
            [Carte("Garde", 1)] * 6 +
            [Carte("Prêtre", 2)] * 2 +
            [Carte("Baron", 3)] * 2 +
            [Carte("Servante", 4)] * 2 +
            [Carte("Prince", 5)] * 2 +
            [Carte("Chancelier", 6)] * 2 +
            [Carte("Roi", 7)] +
            [Carte("Comtesse", 8)] +
            [Carte("Princesse", 9)]
        )

    def shuffle(self):
        random.shuffle(self.pioche)

    def piocher(self):
        return self.pioche.pop(0);
