from abc import ABC, abstractmethod
from copy import deepcopy
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
        self.best_move = Move()

    def choose_card_to_play(self, player, game):
        self.original_player = player  # Stocker le joueur d'origine
        simulated_game = LoveLetterSimulatedGame(game, player)
        self.best_move = self.minimax(simulated_game, self.depth, True)
        return self.best_move.card  # Retourne la carte du meilleur mouvement

    def choose_target_player(self, player, players, game):
        return self.best_move.target  # Retourne la cible du meilleur mouvement

    def choose_character(self, player, characters, game):
        return self.best_move.character  # Retourne le personnage à deviner du meilleur mouvement

    def keep_card(self, player, cards, game):
        return self.best_move.keep  # Retourne la carte à garder du meilleur mouvement

    def copy_player_view(self, original_player, simulated_board):
        # Crée une copie de l'état du jeu en tenant compte des informations du joueur
        copied_board = deepcopy(simulated_board)  # Commence par une copie profonde

        # Met à jour les informations du joueur actif avec les données que le joueur connaît
        active_player = copied_board.active_player
        active_player_memory = copied_board.players[active_player]['memory']

        for player in copied_board.players:
            if player == active_player:
                # Copie uniquement les informations pertinentes pour le joueur actif
                active_player_memory[player] = {'card': simulated_board.players[player]['memory']['card']}
            else:
                # Les autres joueurs voient la carte comme "inconnue"
                active_player_memory[player] = {'card': 'unknown', 'position': 'unknown'}

        return copied_board

    def minimax(self, simulated_board, depth, maximizing_player):
        player = simulated_board.active_player
        print("Depth:", depth)

        if depth == 0 or simulated_board.is_round_over():
            return self.evaluate_board(self.original_player, simulated_board.players, simulated_board)
        if maximizing_player:
            max_eval = float('-inf')
            best_move = None
            for possible_move in simulated_board.get_possible_moves(simulated_board.players, player):
                copy_board = deepcopy(simulated_board)  # Utilise deepcopy ici
                next_board = copy_board.simulate_player_turn(player, possible_move)
                eval = self.minimax(next_board, depth - 1, False)
                if eval > max_eval:
                    max_eval = eval
                    best_move = possible_move
            self.best_move = best_move
            return best_move
        else:
            min_eval = float('inf')
            for possible_move in simulated_board.get_possible_moves(simulated_board.players, player):
                copy_board = deepcopy(simulated_board)  # Utilise deepcopy ici
                next_board = copy_board.simulate_player_turn(player, possible_move)
                eval = self.minimax(next_board, depth - 1, True)
                min_eval = min(min_eval, eval)
            return min_eval

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



