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
        player_type = input(f"Is Player {i} human? (y/n): ").strip().lower()
        is_human = player_type == 'y'
        player_name = f"Player {i}"
        players.append(Player(player_name, is_human=is_human))
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

    return max(game.points, key=game.points.get)


# Main script
if __name__ == "__main__":
    number_of_players = int(input("Enter the number of players (2-6): "))
    number_of_games = int(input("Enter the number of games to play: "))

    # Determine verbosity based on the number of games
    verbose = False
    if number_of_games == 1:
        verbose_input = input("Enable verbose mode? (y/n): ").strip().lower()
        verbose = verbose_input == 'y'

    players = create_players(number_of_players)
    win_counts = {player.name: 0 for player in players}

    with tqdm(total=number_of_games) as pbar:
        for _ in range(number_of_games):
            winner = play_game(players, verbose=verbose)
            win_counts[winner.name] += 1
            pbar.update(1)

    total_games = sum(win_counts.values())
    for player_name, wins in win_counts.items():
        win_rate = wins / total_games if total_games > 0 else 0
        print(f"{player_name} wins: {wins} ({win_rate:.2%} win rate)")
