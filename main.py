from Player import Player
from Game import LoveLetterGame
from tqdm import tqdm

def create_players(number_of_players):
    """
    Create and return a list of players for the game.

    :param number_of_players: The number of players in the game.
    :return: A list of Player objects.
    """
    players = []
    for i in range(1, number_of_players + 1):
        player_name = f"Player {i}"
        players.append(Player(player_name, is_human=False))
    return players


def play_game(players, verbose=False):
    """
    Play a single game of LoveLetter with the given players.

    :param players: A list of Player objects participating in the game.
    """
    game = LoveLetterGame(players, verbose=verbose)
    game.distribute_cards()

    while max(game.points.values()) < game.target_points:
        game.play_turn()

    winner = max(game.points, key=game.points.get)
    return winner


# Main script
if __name__ == "__main__":
    number_of_players = 2
    number_of_games = 10
    players = create_players(number_of_players)
    player1_wins = 0
    player2_wins = 0

    with tqdm(total=number_of_games) as pbar:
        for _ in range(number_of_games):
            winner = play_game(players, verbose=True)
            if winner.name == "Player 1":
                player1_wins += 1
            elif winner.name == "Player 2":
                player2_wins += 1
            pbar.update(1)

    print(f"Player 1 wins: {player1_wins}")
    print(f"Player 2 wins: {player2_wins}")
    print(f"Player 1 win rate: {player1_wins / (player1_wins + player2_wins)}")
    print(f"Player 2 win rate: {player2_wins / (player1_wins + player2_wins)}")
