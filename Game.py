from Deck import Deck
import random

class LoveLetterGame:
    def __init__(self, joueurs):
        self.joueurs = joueurs
        self.deck = Deck()
        self.deck.remplir_pioche()
        self.deck.shuffle()
        self.objectif_points = len(joueurs) - 1
        self.points = {joueur: 0 for joueur in joueurs}
        self.joueur_actif = 0
        self.espionne_count = 0

    def distribuer_cartes(self):
        for joueur in self.joueurs:
            joueur.piocher(self.deck.piocher())

    def jouer_tour(self):
        global carte_jouee
        joueur_actuel = self.joueurs[self.joueur_actif]
        #   print(f"Tour de {joueur_actuel.nom}")
        if not joueur_actuel.reachable:
            #   print(f"{joueur_actuel.nom} est de nouveau ciblable !")
            joueur_actuel.reachable = True

        if len(joueur_actuel.hand) > 0 and len(self.deck.pioche) > 0:
            joueur_actuel.piocher(self.deck.piocher())
            if joueur_actuel.comtesse():
                for carte in joueur_actuel.hand:
                    if carte.nom == "Comtesse":
                        joueur_actuel.hand.remove(carte)
                        carte_jouee = carte  # Utilisez la carte retirée
                        break
            else:
                carte_jouee = joueur_actuel.play_best_card()  # Le joueur joue une carte de sa main
            #   print(f"{joueur_actuel.nom} joue la carte {carte_jouee.nom}")
            self.resolve_effet(carte_jouee)
        self.fin_de_manche()


    def resolve_effet(self, carte):
        if carte_jouee.nom == "Espionne":
            self.espionne_count += 1
        if carte.nom == "Garde":
            joueur_cible = self.choisir_joueur_cible()
            if joueur_cible is not None:
                nom_personnage = self.choisir_personnage()
                #   print(f"{self.joueurs[self.joueur_actif].nom} choisit {joueur_cible.nom} comme cible et devine {nom_personnage}")
                if nom_personnage in [c.nom for c in joueur_cible.hand]:
                    joueur_cible.hand = [c for c in joueur_cible.hand if c.nom != nom_personnage]
                    #   print(f"La devinette est correcte. {joueur_cible.nom} perd la carte {nom_personnage}")
                else:
                    #   print(f"La devinette est incorrecte. Rien ne se passe.")
                    pass
            else :
                #   print("Aucun joueur n'est ciblable, la carte n'a aucun effet !")
                pass

        elif carte.nom == "Prêtre":
            joueur_cible = self.choisir_joueur_cible()
            if joueur_cible is not None:
                #   print(f"{self.joueurs[self.joueur_actif].nom} choisit {joueur_cible.nom} comme cible et regarde {joueur_cible.show_card().nom}")
                pass
            else :
                #   print("Aucun joueur n'est ciblable, la carte n'a aucun effet !")
                pass
        elif carte.nom == "Baron":
            joueur_cible = self.choisir_joueur_cible()
            if joueur_cible is not None:
                joueur_actuel = self.joueurs[self.joueur_actif]
                carte_joueur_actif = joueur_actuel.show_card()
                carte_joueur_cible = joueur_cible.show_card()
                #   print(f"{joueur_actuel.nom} choisit {joueur_cible.nom} comme cible.")
                #   print(f"{joueur_actuel.nom} a la carte {carte_joueur_actif.nom} ({carte_joueur_actif.valeur}).")
                #   print(f"{joueur_cible.nom} a la carte {carte_joueur_cible.nom} ({carte_joueur_cible.valeur}).")
                if carte_joueur_actif.valeur > carte_joueur_cible.valeur:
                    #   print(f"{joueur_actuel.nom} remporte le duel. {joueur_cible.nom} perd la manche.")
                    joueur_cible.hand.remove(carte_joueur_cible)
                elif carte_joueur_actif.valeur < carte_joueur_cible.valeur:
                    #   print(f"{joueur_cible.nom} remporte le duel. {joueur_actuel.nom} perd la manche.")
                    joueur_actuel.hand.remove(carte_joueur_actif)
                else:
                    #   print("Égalité, personne ne perd la manche.")
                    pass
            else :
                #   print("Aucun joueur n'est ciblable, la carte n'a aucun effet !")
                pass
        elif carte.nom == "Servante":
            self.joueurs[self.joueur_actif].reachable = False
            #   print(f"{self.joueurs[self.joueur_actif].nom} n'est pas ciblable pour un tour !")
        elif carte.nom == "Prince":
            joueur_cible = self.choisir_joueur_cible()
            if joueur_cible is not None and len(self.deck.pioche) > 0:
                #   print(f"{self.joueurs[self.joueur_actif].nom} choisit {joueur_cible.nom}")
                joueur_cible.throw()
                joueur_cible.piocher(self.deck.piocher())
            else :
                #   print("Aucun joueur n'est ciblable, la carte n'a aucun effet !")
                pass
        elif carte.nom == "Chancelier":
            joueur_actuel = self.joueurs[self.joueur_actif]
            # Vérifiez s'il y a suffisamment de cartes dans la pioche.
            cartes_piochees = []
            for _ in range(2):
                if len(self.deck.pioche) > 0:
                    carte_piochee = self.deck.piocher()
                    cartes_piochees.append(carte_piochee)
                else:
                    #   print("La pioche est vide.")
                    break
            # Affiche les cartes piochées.
            #   print(f"{joueur_actuel.nom} pioche {len(cartes_piochees)} cartes : {[carte.nom for carte in cartes_piochees]}")
            # Vérifiez si des cartes ont été piochées avant de continuer.
            if len(cartes_piochees) > 0:
                carte_a_garder = joueur_actuel.choose_card_to_keep(cartes_piochees)
                #   print(f"{joueur_actuel.nom} conserve la carte {carte_a_garder.nom} ({carte_a_garder.valeur}).")
                cartes_a_remettre = [carte for carte in cartes_piochees if carte != carte_a_garder]
                cartes_a_remettre.reverse()  # Remettez les cartes dans l'ordre inverse sous le paquet.
                self.deck.pioche.extend(cartes_a_remettre)
        elif carte.nom == "Roi":
            joueur_cible = self.choisir_joueur_cible()
            if joueur_cible is not None:
                joueur_actuel = self.joueurs[self.joueur_actif]
                #   print(f"{joueur_actuel.nom} choisit {joueur_cible.nom} comme cible.")
                carte_joueur_actif = joueur_actuel.show_card()
                carte_joueur_cible = joueur_cible.show_card()
                #   print(f"{joueur_actuel.nom} a la carte {carte_joueur_actif.nom} ({carte_joueur_actif.valeur}).")
                #   print(f"{joueur_cible.nom} a la carte {carte_joueur_cible.nom} ({carte_joueur_cible.valeur}).")
                joueur_actuel.hand.remove(carte_joueur_actif)
                joueur_cible.hand.remove(carte_joueur_cible)
                joueur_actuel.hand.append(carte_joueur_cible)
                joueur_cible.hand.append(carte_joueur_actif)
                #   print(f"{joueur_actuel.nom} et {joueur_cible.nom} ont échangé leurs cartes.")
            else :
                #   print("Aucun joueur n'est ciblable, la carte n'a aucun effet !")
                pass
        elif carte.nom == "Comtesse":
            pass
        elif carte.nom == "Princesse":
            joueur_actuel = self.joueurs[self.joueur_actif]
            #   print(f"{joueur_actuel.nom} joue la Princesse et est éliminé de la manche.")
            joueur_actuel.hand.remove(joueur_actuel.show_card())


    def choisir_joueur_cible(self):
        joueur_cible = None
        joueur_actuel = self.joueurs[self.joueur_actif]
        joueurs_disponibles = [j for j in self.joueurs if (j != joueur_actuel and j.reachable and len(j.hand) > 0)]
        if len(joueurs_disponibles) > 0:
            joueur_cible = random.choice(joueurs_disponibles)
        return joueur_cible

    def choisir_personnage(self):
        # Liste de tous les personnages possibles
        personnages_possibles = ["Espionne", "Prêtre", "Baron", "Servante", "Prince", "Chancelier", "Roi",
                                 "Comtesse", "Princesse"]
        # Choisissez un personnage au hasard parmi les personnages restants
        personnage_choisi = random.choice(personnages_possibles)
        return personnage_choisi

    def fin_de_manche(self):
        if len(self.deck.pioche) == 0 or (len([j for j in self.joueurs if len(j.hand) > 0]) == 1):
            joueurs_en_jeu = [j for j in self.joueurs if len(j.hand) > 0]
            if joueurs_en_jeu:
                joueur_gagnant = max(joueurs_en_jeu, key=lambda j: max([c.valeur for c in j.hand]))
                #AJOUTER POINTS BONUS ESPIONNE
                if len(self.deck.pioche) == 0:
                    #   print("Il n'y a plus de carte dans la pioche !")
                    pass
                else :
                    #   print(f"{joueur_gagnant.nom} est le dernier joueur en vie.")
                    pass
                self.points[joueur_gagnant] += 1
                #   print(f"{joueur_gagnant.nom} gagne la manche et obtient 1 point.")
            self.nouvelle_manche()
        else:
            if self.joueur_actif == len(self.joueurs) - 1:
                self.joueur_actif = 0
            else:
                self.joueur_actif += 1

    def nouvelle_manche(self):
        self.deck = Deck()
        self.deck.remplir_pioche()
        self.deck.shuffle()
        for joueur in self.joueurs:
            joueur.hand = []
        self.distribuer_cartes()
        self.joueur_actif = 0


