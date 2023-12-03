from abc import ABC, abstractmethod
import random


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
    def choose_card_to_play(player):
        pass

    @abstractmethod
    def keep_card(self, player, cards):
        pass

    @abstractmethod
    def choose_target_player(self, player, players):
        pass

    @abstractmethod
    def choose_character(self, player, characters):
        pass


class HumanStrategy(PlayerStrategy):
    def choose_card_to_play(self, player):
        return self._choose_from_list(player.name, player.hand, "Choose a card to play: ")
    
    def choose_target_player(self, player, players):
        return self._choose_from_list(player.name, players, "Choose a player to target: ")
    
    def choose_character(self, player, characters):
        return self._choose_from_list(player.name, characters, "Choose a character to guess: ")
    
    def keep_card(self, player, cards):
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
    def choose_card_to_play(self, player):
        return self._choose_from_list(player.hand)
    
    def choose_target_player(self, player, players):
        return self._choose_from_list(players)
    
    def choose_character(self, player, characters):
        return self._choose_from_list(characters)
    
    def keep_card(self, player, cards):
        return self._choose_from_list(player.hand + cards)

    def _choose_from_list(self, items):
        if items:
            return random.choice(items)
        else:
            return None


class MinMaxStrategy(PlayerStrategy):
    def __init__(self, depth=10):
        self.depth = depth

    def choose_card_to_play(self, player):

        possible_moves = player.get_possible_moves()  # Define a method in your Player class to get all possible moves

        best_move = None
        best_eval = float('-inf')

        for move in possible_moves:
            # Assume play_card is a method in your LoveLetter game that simulates playing a card
            simulated_board = simulate_play_card(player, move)

            # Assume evaluate_board is a method in your MinMaxStrategy that evaluates the current game state
            eval = self.evaluate_board(player, simulated_board.players, simulated_board.cards, simulated_board.characters)

            if eval > best_eval:
                best_eval = eval
                best_move = move

        return best_move

    def choose_target_player(self, player, players):
        # Implement MinMax algorithm to choose the best target player
        pass

    def choose_character(self, player, characters):
        # Implement MinMax algorithm to choose the best character to guess
        pass

    def keep_card(self, player, cards):
        # Implement MinMax algorithm to choose the best card to keep
        pass

    def evaluate_board(self, player, players, cards, characters):
        # Implement a heuristic evaluation function to evaluate the current game state
        pass

    def min_max(self, player, simulated_board, depth, maximizing_player):
        if depth == 0 or simulated_board.is_game_over():
            return self.evaluate_board(player, simulated_board)

        if maximizing_player:
            max_eval = float('-inf')
            for possible_move in simulated_board.get_possible_moves():
                next_board = simulated_board.simulate_play_card(player, possible_move)
                eval = self.min_max(player, next_board, depth - 1, False)
                max_eval = max(max_eval, eval)
            return max_eval
        else:
            min_eval = float('inf')
            for possible_move in simulated_board.get_possible_moves():
                next_board = simulated_board.simulate_play_card(player, possible_move)
                eval = self.min_max(player, next_board, depth - 1, True)
                min_eval = min(min_eval, eval)
            return min_eval

    def choose_best_move(self, player, simulated_board, maximizing_player):
        best_eval = float('-inf') if maximizing_player else float('inf')
        best_move = None

        for possible_move in simulated_board.get_possible_moves():
            next_board = simulated_board.simulate_play_card(player, possible_move)
            eval = self.min_max(player, next_board, self.depth, maximizing_player)

            if (maximizing_player and eval > best_eval) or (not maximizing_player and eval < best_eval):
                best_eval = eval
                best_move = possible_move

        return best_move

def simulate_play_card(self, player, played_card):
    """
    Simulate the effects of a player playing a card.

    :param player: The player who is playing the card.
    :param played_card: The card the player is playing.

    :return: The simulated game state after playing the card.
    """
    # Create a deep copy of the current game state
    simulated_game = deepcopy(self)

    # Find the player in the simulated game
    simulated_player = next(p for p in simulated_game.players if p.name == player.name)

    # Remove the played card from the player's hand
    simulated_player.hand.remove(played_card)

    # Simulate the effect of the played card
    simulated_game.resolve_effect(played_card)

    # Check if the round should end
    if simulated_game.is_round_end():
        simulated_game.end_of_round()

    return simulated_game

def simulate_move(self, player):
    """
    Simulate the player making a move (playing a card).

    :param player: The player making the move.

    :return: The simulated game state after the player's move.
    """
    # Choose a card to play using the MinMax strategy
    chosen_card = player.strategy.choose_card_to_play(player)

    # Simulate the effects of playing the chosen card
    simulated_game = self.simulate_play_card(player, chosen_card)

    return simulated_game