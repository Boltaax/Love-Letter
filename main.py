from Player import Player
from Game import LoveLetterGame
from tqdm import tqdm
from player_strategies import get_strategies
import pandas as pd
import matplotlib.pyplot as plt
from GameStats import GameStats

def create_players(number_of_players):
    """
    Create and return a list of players for the game.
    
    :param number_of_players: The number of players in the game.
    :return: A list of Player objects.
    """
    players = []
    strategies = get_strategies()
    strategy_names = list(strategies.keys())

    # Display available strategies
    print("Available strategies:")
    for i, name in enumerate(strategy_names, 1):
        print(f"{i}. {name}")

    for i in range(1, number_of_players + 1):
        while True:
            try:
                choice = int(input(f"Choose the strategy for Player {i} (enter a number): "))
                if 1 <= choice <= len(strategy_names):
                    strategy_name = strategy_names[choice - 1]
                    strategy_class = strategies[strategy_name]
                    if strategy_name == "MiniMax":
                        depth = int(input(f"Enter the depth for MiniMax strategy (default is 1): ") or 1)
                        strategy_instance = strategy_class(depth)
                    else:
                        strategy_instance = strategy_class()
                    break
                else:
                    print("Invalid number. Please choose a valid strategy number.")
            except ValueError:
                print("Invalid input. Please enter a number.")

        player_name = f"Player {i}"
        players.append(Player(player_name, strategy=strategy_instance))

    return players


def play_game(players, game_number, verbose=False):
    """
    Play a single game of LoveLetter with the given players.

    :param players: A list of Player objects participating in the game.
    """
    game = LoveLetterGame(players, game_number, verbose=verbose)
    game.new_round()

    while max(game.points.values()) < game.target_points:
        game.play_turn()

    return game.points


# Main script
if __name__ == "__main__":
    number_of_players = 2
    print("The number of players in the game is fixed to 2.")
    number_of_games = int(input("Enter the number of games to play: "))

    # Determine verbosity based on the number of games
    verbose = False
    if number_of_games == 1:
        verbose_input = input("Enable verbose mode? (y/n): ").strip().lower()
        verbose = verbose_input == 'y'

    players = create_players(number_of_players)
    win_counts = {player.name: 0 for player in players}
    total_game_stats = []
    excel_file_path = "game_results.xlsx"

    with pd.ExcelWriter(excel_file_path, engine='openpyxl') as writer:
        writer.book.create_sheet("GameResults")
        game_stats = GameStats(game_number=0)
        game_stats.header(writer, "GameResults")
        with tqdm(total=number_of_games) as pbar:
            for i in range(1, number_of_games+1):
                game_stats = GameStats(game_number=i)
                points = play_game(players, game_number=i, verbose=verbose)
                winner = max(points, key=points.get)
                win_counts[winner.name] += 1
                game_stats.add_round({'game_number': i,'points': points, 'winner': winner, 'loser': min(points, key=points.get)})
                game_stats.save_to_excel(writer, sheet_name="GameResults")
                total_game_stats.append(game_stats)
                pbar.update(1)

    total_games = sum(win_counts.values())
    print("\nOverall Results:")
    for player_name, wins in win_counts.items():
        win_rate = wins / total_games if total_games > 0 else 0
        print(f"{player_name} wins: {wins} ({win_rate:.2%} win rate)")

    print(f"\nResults saved to {excel_file_path}")

    # Create a dataframe with the results
    results_df = pd.DataFrame(columns=['GameNumber', 'Player', 'Points'])
    for game_stats in total_game_stats:
        for round_info in game_stats.rounds:
            game_number = round_info['game_number']
            for player, points in round_info['points'].items():
                results_df = pd.concat([results_df, pd.DataFrame({'GameNumber': [game_number], 'Player': [player], 'Points': [points]})], ignore_index=True)

    # Create the points progression graph
    plt.figure(figsize=(12, 8))
    plt.subplot(2, 1, 1)  # Create the first subplot
    for player in results_df['Player'].unique():
        player_data = results_df[results_df['Player'] == player]
        total_points = player_data['Points'].sum()
        average_points_per_game = total_points / total_games if total_games > 0 else 0
        label = f"{player.name} (Total Points: {total_points}, Avg Points/Game: {average_points_per_game:.2f})"
        plt.plot(player_data['GameNumber'], player_data['Points'], label=label)
    plt.xlabel('Game Number')
    plt.ylabel('Points')
    plt.title('Points Progression by Player')
    plt.legend()

    # Create the wins by player graph (bar chart)
    plt.subplot(2, 1, 2)  # Create the second subplot
    players_names = list(win_counts.keys())
    wins = list(win_counts.values())
    win_percentages = {player: wins / total_games for player, wins in win_counts.items()}

    colors = [plt.cm.RdYlGn(win_percentages[player]) for player in players_names]

    bars = plt.bar(players_names, wins, color=colors)
    plt.xlabel('Players')
    plt.ylabel('Number of Wins')
    plt.title('Wins by Player')
    for bar, player in zip(bars, players_names):
        win_rate = win_percentages[player]
        plt.text(bar.get_x() + bar.get_width() / 2, bar.get_height(), f'{win_rate:.2%}', ha='center', va='bottom')

    # Display the graphs
    plt.tight_layout()  # Avoid overlapping of the subplots
    plt.show()