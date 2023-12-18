from abc import ABC, abstractmethod
import random
from SimulatedGame import LoveLetterSimulatedGame
from Move import Move



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
    def __init__(self, depth=3):
        self.depth = depth
        self.original_player = None  # Ajout de la variable pour stocker le joueur d'origine

    def choose_card_to_play(self, player, game):
        self.original_player = player  # Stocker le joueur d'origine
        simulated_game = LoveLetterSimulatedGame(original_game=game)
        best_move = self.expectiminimax(simulated_game, self.depth, True)
        return best_move.card  # Retourne la carte du meilleur mouvement

    def choose_target_player(self, player, players, game):
        simulated_game = LoveLetterSimulatedGame(original_game=game)
        best_move = self.expectiminimax(simulated_game, self.depth, True)
        return best_move.target  # Retourne la cible du meilleur mouvement

    def choose_character(self, player, characters, game):
        simulated_game = LoveLetterSimulatedGame(original_game=game)
        best_move = self.expectiminimax(simulated_game, self.depth, True)
        return best_move.character  # Retourne le personnage à deviner du meilleur mouvement

    def keep_card(self, player, cards, game):
        simulated_game = LoveLetterSimulatedGame(original_game=game)
        best_move = self.expectiminimax(simulated_game, self.depth, True)
        return best_move.keep  # Retourne la carte à garder du meilleur mouvement

    def expectiminimax(self, simulated_board, depth, maximizing_player):
        player = simulated_board.active_player

        if depth == 0 or simulated_board.is_round_over():
            return self.evaluate_board(self.original_player, simulated_board.players, simulated_board)

        if maximizing_player:
            max_eval = float('-inf')
            best_move = None

            for possible_move in simulated_board.get_possible_moves(simulated_board.players, player):
                next_board = simulated_board.simulate_player_turn(player, possible_move)
                eval = self.expectiminimax(next_board, depth - 1, False)
                if eval > max_eval:
                    max_eval = eval
                    best_move = possible_move
            return best_move
        else:
            weighted_evals = 0
            total_probability = 0

            for possible_move in simulated_board.get_possible_moves(simulated_board.players, player):
                next_board = simulated_board.simulate_player_turn(player, possible_move)

                if self.random_event_at_node(next_board):
                    # Return weighted average of all child nodes' values
                    probability = self.probability_of_random_event(next_board)
                    weighted_evals += probability * self.expectiminimax(next_board, depth - 1, maximizing_player)
                    total_probability += probability
                else:
                    eval = self.expectiminimax(next_board, depth - 1, True)
                    weighted_evals += eval
                    total_probability += 1

            return weighted_evals / total_probability if total_probability != 0 else 0

    def evaluate_board(self, player, players, simulated_board):
        # TODO: Implement a heuristic evaluation function to evaluate the current game state

        evaluation_score = 0

        # Check if the current player has been eliminated
        if not player.hand:
            evaluation_score -= 10000  # Deduct a high score for being eliminated
            for p in players:
                if p != player and p.hand:
                    evaluation_score += (simulated_board.points[player] - simulated_board.points[p]) * 1000

        # Check if any other player has been eliminated
        for p in players:
            if not p.hand and p != player:
                evaluation_score += 500  # Add points for each player who has been eliminated

        # Check the number of cards in the player's memory
        if 'memory' in player.__dict__:
            for other_player in players:
                if other_player != player and other_player.name != "deck":
                    evaluation_score += 10 * other_player.card().value

        # TODO: Implement a searching algorithm thanks to probability to give a score for each possibility that a player can win or not the game
        #  he will use the probability_draw_card method, and give for each player the probability that he will win thanks to the higher score card

        # Add more evaluation factors based on the specific game rules and strategies

        return evaluation_score

    def probability_draw_card(self, player, card, game):
        return game.probability_draw_cards(player, card)

    def probability_of_random_event(self, simulated_board):
        total_probability = 0

        for possible_move in simulated_board.get_possible_moves(simulated_board.players, simulated_board.active_player):
            move_probability = self.calculate_move_probability(simulated_board, possible_move)
            total_probability += move_probability * self.calculate_move_weight(simulated_board, possible_move)

        return total_probability

    def calculate_move_probability(self, simulated_board, possible_move):
        # Calculate the probability of success for a specific move

        # Example: Probability of drawing a specific card
        card_to_draw = self.get_card_to_draw(simulated_board, possible_move)
        probability_draw = self.probability_draw_card(simulated_board.active_player, card_to_draw, simulated_board)

        # Example: Probability of guessing correctly
        if possible_move.card.name == "Guard":
            probability_guess = self.probability_of_correct_guess(simulated_board, possible_move)
        else:
            probability_guess = 1  # Assume non-Guard cards always guess correctly

        # You can add more factors based on your game rules

        return probability_draw * probability_guess

    def get_card_to_draw(self, simulated_board, possible_move):
        # Determine the card that needs to be drawn for the move
        # Example: For Prince card, the card to draw is the target player's card
        if possible_move.card.name == "Prince":
            return possible_move.target.card().name
        # Add more cases for other cards as needed
        else:
            return None  # No specific card needed

    def probability_of_correct_guess(self, simulated_board, possible_move):
        # Calculate the probability of guessing correctly for Guard card

        # Example: If the target player has a known card, calculate the probability of guessing it
        target_player = possible_move.target
        if target_player and target_player.name in simulated_board.active_player.memory:
            guessed_card = possible_move.character
            actual_card = target_player.memory[target_player.name].name
            if guessed_card == actual_card:
                return 1  # Correct guess
            else:
                return 0  # Incorrect guess
        else:
            # If the target player's card is unknown, you might use a default probability
            return 1 / len(simulated_board.deck)  # Adjust as needed

    def calculate_move_weight(self, simulated_board, possible_move):
        # Calculate a weight for the move based on its likelihood of occurring
        # This can be based on the importance of the move, number of possible moves, etc.
        # You might need to fine-tune this based on your game dynamics
        return 1  # Placeholder value; adjust as needed


