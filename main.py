from Player import Player
from Game import LoveLetterGame

def create_players(number_of_players):
    """
    Create and return a list of players for the game.

    :param number_of_players: The number of players in the game.
    :return: A list of Player objects.
    """
    players = []
    for i in range(1, number_of_players + 1):
        player_name = f"Player {i}"
        players.append(Player(player_name))
    return players

def play_game(players):
    """
    Play a single game of LoveLetter with the given players.

    :param players: A list of Player objects participating in the game.
    """
    game = LoveLetterGame(players)
    game.distribute_cards()

    while max(game.points.values()) < game.target_points:
        game.play_turn()

    winner = max(game.points, key=game.points.get)
    print(f"{winner.name} wins the game with {game.points[winner]} points!")

# Main script
if __name__ == "__main__":
    number_of_players = 2
    players = create_players(number_of_players)
    play_game(players)
