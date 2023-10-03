import random

class Joueur:
    def __init__(self,nom):
        self.nom = nom
        self.hand = []
        self.reachable = True

    def piocher(self, carte):
        self.hand.append(carte)

    def play_best_card(self):
        return self.hand.pop(random.randint(0, 1))

    def show_card(self):
        return self.hand[0]

    def throw(self):
        carte = self.hand.pop()
        #   print(self.nom, " avait ",carte.nom, " dans sa main !" )
        return carte

    def choose_card_to_keep(self, cartes):
        return cartes[random.randint(0, len(cartes)-1)]

    def comtesse(self):
        # Vérifiez si le joueur a la carte "Comtesse" et une carte "Roi" ou "Prince" dans sa main
        has_comtesse = any(carte.nom == "Comtesse" for carte in self.hand)
        has_king_or_prince = any(carte.nom in ["Roi", "Prince"] for carte in self.hand)
        return has_comtesse and has_king_or_prince
