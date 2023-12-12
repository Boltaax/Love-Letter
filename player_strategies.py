from abc import ABC, abstractmethod
import random
from SimulatedGame import LoveLetterSimulatedGame



def get_strategies():
    '''
    Returns a dictionary of all available strategies
    '''
    return {
        "Human": HumanStrategy,
        "Random": RandomStrategy,
        "MinMax": MinMaxStrategy
    }


class PlayerStrategy(ABC):
    @abstractmethod
    def choose_card_to_play(self, player, game):
        pass

    @abstractmethod
    def keep_card(self, player, cards, game):
        pass

    @abstractmethod
    def choose_target_player(self, player, players, game):
        pass

    @abstractmethod
    def choose_character(self, player, characters, game):
        pass


class HumanStrategy(PlayerStrategy):
    def choose_card_to_play(self, player, game):
        return self._choose_from_list(player.name, player.hand, "Choose a card to play: ")
    
    def choose_target_player(self, player, players, game):
        return self._choose_from_list(player.name, players, "Choose a player to target: ")
    
    def choose_character(self, player, characters, game):
        return self._choose_from_list(player.name, characters, "Choose a character to guess: ")
    
    def keep_card(self, player, cards, game):
        return self._choose_from_list(player.name, player.hand + cards, "Choose a card to keep: ")

    def _choose_from_list(self, player_name, items, prompt):
        '''
        Prompts the player to choose an item from a list of items

        :param player_name: The name of the player
        :param items: The list of items to choose from

        :return: The chosen item
        '''
        if items:
            for i, item in enumerate(items):
                print(f"{i}: {item}")
            while True:
                choice = input(f"{player_name}, {prompt}")
                if choice.isdigit() and 0 <= int(choice) < len(items):
                    return items[int(choice)]
                print("Invalid input. Please enter a valid number.")


class RandomStrategy(PlayerStrategy):
    def choose_card_to_play(self, player, game):
        return self._choose_from_list(player.hand)
    
    def choose_target_player(self, player, players, game):
        return self._choose_from_list(players)
    
    def choose_character(self, player, characters, game):
        return self._choose_from_list(characters)
    
    def keep_card(self, player, cards, game):
        return self._choose_from_list(player.hand + cards)

    def _choose_from_list(self, items):
        if items:
            return random.choice(items)
        else:
            return None


class MinMaxStrategy(PlayerStrategy):
    def __init__(self, depth=10):
        self.depth = depth

    def choose_card_to_play(self, player, game):
        simulated_game = LoveLetterSimulatedGame(original_game=game)  # Instantiate with an initial game state
        best_move = self.expectiminimax_card_to_play(player, simulated_game, self.depth, True)
        return best_move

    def expectiminimax_card_to_play(self, player, simulated_board, depth, maximizing_player):
        if depth == 0 or simulated_board.is_round_over():
            return self.evaluate_board(player, simulated_board)

        if maximizing_player:
            max_eval = float('-inf')
            best_move = None

            for possible_move in simulated_board.get_possible_moves(simulated_board.players, player):
                card, target = possible_move
                next_board = simulated_board.simulate_play_card(player, card)
                eval = self.expectiminimax_card_to_play(player, next_board, depth - 1, False)
                if eval > max_eval:
                    max_eval = eval
                    best_move = possible_move

            return best_move
        else:
            min_eval = float('inf')

            for possible_move in simulated_board.get_possible_moves(simulated_board.players, player):
                card, target = possible_move
                next_board = simulated_board.simulate_play_card(player, card)
                eval = self.expectiminimax_card_to_play(player, next_board, depth - 1, True)
                min_eval = min(min_eval, eval)

            return min_eval

    def choose_target_player(self, player, players, game):
        # MinMax algorithm to choose the best target player
        simulated_game = LoveLetterSimulatedGame(original_game=game)
        best_eval = float('-inf')
        best_target = None

        for target_player in players:
            if target_player.reachable and target_player.hand:
                eval = self.expectiminimax_target_player(player, target_player, self.depth, True)
                if eval > best_eval:
                    best_eval = eval
                    best_target = target_player

        return best_target

    def expectiminimax_target_player(self, player, target_player, depth, maximizing_player):
        if depth == 0:
            # Evaluate the board (a simple heuristic)
            return len(player.hand) - len(target_player.hand)

        if maximizing_player:
            max_eval = float('-inf')
            for possible_move in target_player.get_possible_moves():
                next_board = target_player.simulate_play_card(target_player, possible_move)
                eval = self.expectiminimax_target_player(player, next_board, depth - 1, False)
                max_eval = max(max_eval, eval)
            return max_eval
        else:
            min_eval = float('inf')
            for possible_move in target_player.get_possible_moves():
                next_board = target_player.simulate_play_card(target_player, possible_move)
                eval = self.expectiminimax_target_player(player, next_board, depth - 1, True)
                min_eval = min(min_eval, eval)
            return min_eval

    def choose_character(self, player, characters, game):
        # MinMax algorithm to choose the best character to guess
        best_eval = float('-inf')
        best_character = None

        for character in characters:
            eval = self.expectiminimax_character(player, character, self.depth, True)
            if eval > best_eval:
                best_eval = eval
                best_character = character

        return best_character

    def expectiminimax_character(self, player, character, depth, maximizing_player):
        if depth == 0:
            # Evaluate the board (a simple heuristic)
            return 1 if character == player.card().name else 0

        if maximizing_player:
            max_eval = float('-inf')
            for possible_move in player.get_possible_moves():
                next_board = player.simulate_play_card(player, possible_move)
                eval = self.expectiminimax_character(player, character, depth - 1, False)
                max_eval = max(max_eval, eval)
            return max_eval
        else:
            min_eval = float('inf')
            for possible_move in player.get_possible_moves():
                next_board = player.simulate_play_card(player, possible_move)
                eval = self.expectiminimax_character(player, character, depth - 1, True)
                min_eval = min(min_eval, eval)
            return min_eval

    def keep_card(self, player, cards, game):
        # MinMax algorithm to choose the best card to keep
        best_eval = float('-inf')
        best_card = None

        for card in cards:
            eval = self.expectiminimax_keep_card(player, card, self.depth, True)
            if eval > best_eval:
                best_eval = eval
                best_card = card

        return best_card

    def expectiminimax_keep_card(self, player, card, depth, maximizing_player):
        if depth == 0:
            # Evaluate the board (a simple heuristic)
            return 1 if card.name == player.card().name else 0

        if maximizing_player:
            max_eval = float('-inf')
            for possible_move in player.get_possible_moves():
                next_board = player.simulate_play_card(player, possible_move)
                eval = self.expectiminimax_keep_card(player, card, depth - 1, False)
                max_eval = max(max_eval, eval)
            return max_eval
        else:
            min_eval = float('inf')
            for possible_move in player.get_possible_moves():
                next_board = player.simulate_play_card(player, possible_move)
                eval = self.expectiminimax_keep_card(player, card, depth - 1, True)
                min_eval = min(min_eval, eval)
            return min_eval

    def evaluate_board(self, player, simulated_board):
        # TODO: Implement a heuristic evaluation function to evaluate the current game state
        # This function should return a heuristic value for the given board state
        return 0  # Placeholder value, replace with your implementation

    def probability_draw_card(self, player, card, game):
        return game.probability_draw_cards(player, card)


