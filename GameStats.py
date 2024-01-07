from collections import defaultdict
import pandas as pd

class GameStats:
    def __init__(self, game_number):
        self.game_number = game_number
        self.rounds = []
        self.points = defaultdict(int)
        self.winner = None

    def add_round(self, round_info):
        self.rounds.append(round_info)
        for player, points in round_info['points'].items():
            self.points[player.name] += points
        self.winner = max(self.points, key=self.points.get)

    def to_dataframe(self):
        df_data = []
        for round_info in self.rounds:
            game_number = round_info['game_number']
            winner = round_info['winner']
            loser = round_info['loser'] if 'loser' in round_info else None
            winner_points = round_info['points'][winner]
            loser_points = round_info['points'].get(loser, None) if loser else None

            df_data.append({
                'GameNumber': game_number,
                'Winner': winner.name,
                'WinnerStrategy': f"{winner.strategy.name} {winner.strategy.depth}" if hasattr(winner.strategy, 'depth') and winner.strategy.depth else winner.strategy.name,
                'WinnerPoints': winner_points,
                'LoserPoints': loser_points,
                'Loser': loser.name,
                'LoserStrategy': f"{loser.strategy.name} {loser.strategy.depth}" if hasattr(loser.strategy, 'depth') and loser.strategy.depth else loser.strategy.name
            })

        df = pd.DataFrame(df_data)
        return df

    def save_to_excel(self, excel_writer, sheet_name):
        """
        Save the data from the object to an Excel file.

        Args:
            excel_writer (pandas.ExcelWriter): The Excel writer object to write the data to.
            sheet_name (str): The name of the sheet to write the data to.

        Returns:
            None
        """
        df = self.to_dataframe()
        if sheet_name not in excel_writer.sheets:
            excel_writer.book.create_sheet(sheet_name)

        df.to_excel(excel_writer, sheet_name=sheet_name, index=False, startrow=excel_writer.sheets[sheet_name].max_row,
                    header=False)

    def header(self, excel_writer, sheet_name):
        df = pd.DataFrame([{
            'GameNumber': 'Game Number',
            'Winner': 'Winner',
            'WinnerStrategy': 'Winner Strategy',
            'WinnerPoints': 'Winner points',
            'LoserPoints': 'Loser points',
            'Loser': 'Loser',
            'LoserStrategy': 'Loser Strategy'
        }])
        if sheet_name not in excel_writer.sheets:
            excel_writer.book.create_sheet(sheet_name)

        df.to_excel(excel_writer, sheet_name=sheet_name, index=False, startrow=excel_writer.sheets[sheet_name].max_row,
                    header=False)
