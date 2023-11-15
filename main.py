from Player import Player
from Game import LoveLetterGame

import random

for game_number in range(10000):
    print("Game number", game_number)
    # Example of a game
    number_of_players = 2
    players = []

    for i in range(1, number_of_players + 1):
        player_name = f"Player {i}"
        player_i = Player(player_name)
        players.append(player_i)

    game = LoveLetterGame(players)
    game.distribute_cards()

    while max(game.points.values()) <= game.target_points:
        game.play_turn()

    winner = max(game.points, key=game.points.get)
    #   print(f"{winner.name} wins the game with {game.points[winner]} points!")

    """for player in players:
        if player != winner:
            print(f"{player.name} finishes the game with {game.points[player]} points!")"""
