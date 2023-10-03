from Joueur import Joueur
from Game import LoveLetterGame

import random

for nb_partie in range(10000):
    print("Partie n°",nb_partie)
    # Exemple de partie
    nb_joueur = random.randint(2, 6)
    joueurs = []

    for i in range(1, nb_joueur + 1):
        nom_joueur = f"Joueur {i}"
        joueur_i = Joueur(nom_joueur)
        joueurs.append(joueur_i)

    jeu = LoveLetterGame(joueurs)
    jeu.distribuer_cartes()

    while max(jeu.points.values()) <= jeu.objectif_points:
        jeu.jouer_tour()

    gagnant = max(jeu.points, key=jeu.points.get)
    #   print(f"{gagnant.nom} gagne la partie avec {jeu.points[gagnant]} points !")

    """for joueur in joueurs:
        if joueur != gagnant:
            print(f"{joueur.nom} finit la partie avec {jeu.points[joueur]} points !")"""