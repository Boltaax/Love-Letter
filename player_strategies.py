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
        simulated_game = LoveLetterSimulatedGame(game)
        pov_player = self.copy_player_view(simulated_game)
        self.best_move = self.expectiminimax(pov_player, self.depth, True)
        return self.best_move.card  # Retourne la carte du meilleur mouvement

    def choose_target_player(self, player, players, game):
        return self.best_move.target  # Retourne la cible du meilleur mouvement

    def choose_character(self, player, characters, game):
        return self.best_move.character  # Retourne le personnage à deviner du meilleur mouvement

    def keep_card(self, player, cards, game):
        return self.best_move.keep  # Retourne la carte à garder du meilleur mouvement

    def copy_player_view(self, simulated_board):
        # Crée une copie de l'état du jeu en tenant compte des informations du joueur
        copied_board = deepcopy(simulated_board)  # Commence par une copie profonde

        # Met à jour les informations avec les données que le joueur actif connaît
        active_player = copied_board.active_player

        for player in copied_board.players:
            if player != active_player:
                player.hand = [0]
                player.deck_memory = ['unknown'] * len(copied_board.deck.draw_pile)

        return copied_board

    def expectiminimax(self, game, depth, maximizing_player):
        #TODO : Initialiser une partie avec les mêmes caractéristiques mais toutes les cartes non connues à l'init deviennent
        # des cartes 'unknown' qui lorsqu'elles sont piochées peuvent devenir n'importe laquelle des cartes possiblement piochables
        # (p > 0) il faut garder la probabilité de chaque carte pour multiplier chaque proba entre elles et le poids de chaque moove
        # est calculé à la fin avec evaluate_board qui donne un score, eval = proba_totale*score et si celle-ci est la plus élevée
        # elle est gardée et le moove qui a provoqué ceci est gardé en tant que best_moove.

        if depth == 0 or game.is_round_over():
            return self.evaluate_board(game)

        if maximizing_player:
            max_eval = float('-inf')
            best_move = None

            for possible_move in game.get_possible_moves(self):


                next_game = game.simulate_player_turn(self, possible_move)
                eval = self.expectiminimax(next_game, depth - 1, False)
                if eval > max_eval:
                    max_eval = eval
                    best_move = possible_move
            return best_move
        else:
            weighted_evals = 0
            total_probability = 0

            for possible_move in game.get_possible_moves(self):

                next_game = game.simulate_player_turn(self, possible_move)

                if self.random_event_at_node(next_game):
                    probability = self.probability_of_random_event(next_game)
                    weighted_evals += probability * self.expectiminimax(next_game, depth - 1, maximizing_player)
                    total_probability += probability
                else:
                    eval = self.expectiminimax(next_game, depth - 1, True)
                    weighted_evals += eval
                    total_probability += 1

            return weighted_evals / total_probability if total_probability != 0 else 0

    def random_event_at_node(self, game):
        # TODO: Implémentez votre fonction pour déterminer s'il y a un événement aléatoire à ce nœud du jeu
        pass

    def probability_of_random_event(self, game):
        # TODO: Implémentez votre fonction pour calculer la probabilité de l'événement aléatoire à ce nœud du jeu
        pass

    def evaluate_board(self, simulated_board):
        # TODO: Implement a heuristic evaluation function to evaluate the current game state
        evaluation_score = 0
        # Check if the current player has been eliminated
        if not self.original_player.hand:
            evaluation_score -= 10000  # Deduct a high score for being eliminated
            for p in simulated_board.players:
                if p != simulated_board.players and p.hand:
                    evaluation_score += (simulated_board.points[self.original_player] - simulated_board.points[p]) * 1000

        # Check if any other player has been eliminated
        for p in simulated_board.players:
            if not p.hand and p != simulated_board.players:
                evaluation_score += 1000  # Add points for each player who has been eliminated

        # Check the number of cards in the player's memory
        if self.original_player.player_memory:
            evaluation_score += 50 * self.original_player.player_memory


        # TODO: Implement a searching algorithm thanks to probability to give a score for each possibility that a player can win or not the game
        #  he will use the probability_draw_card method, and give for each player the probability that he will win thanks to the higher score card

        # Add more evaluation factors based on the specific game rules and strategies

        return evaluation_score

    def probability_draw_card(self, player, card, game):
        return game.probability_draw_cards(player, card)



