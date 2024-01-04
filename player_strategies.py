from abc import ABC, abstractmethod
from copy import deepcopy
import random
from SimulatedGame import LoveLetterSimulatedGame
from Cards import Card
from itertools import product



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
    def __init__(self, depth=2):
        self.depth = depth
        self.original_player = None  # Ajout de la variable pour stocker le joueur d'origine
        self.best_move = None # Ajout de ma variable pour stocker la meilleure action à réaliser

    def choose_card_to_play(self, player, game):
        self.original_player = player  # Stocker le joueur d'origine
        simulated_game = LoveLetterSimulatedGame(game)
        pov_player = self.copy_player_view(simulated_game)

        print(pov_player)
        self.best_move = self.depth_algo(pov_player, 1, True)
        print(f"Best move : {self.best_move}")
        best_card = next(c for c in player.hand if c.name == self.best_move.card.name)
        return best_card  # Retourne la carte du meilleur mouvement

    def choose_target_player(self, player, players, game):
        print(f"players : {', '.join(str(player) for player in players)} --- best move target : {str(self.best_move.target)}")
        best_target = None
        if players:
            for p in players:
                if p.name == self.best_move.target.name:
                    best_target = p
        return best_target  # Retourne la cible du meilleur mouvement

    def choose_character(self, player, characters, game):
        return self.best_move.character  # Retourne le personnage à deviner du meilleur mouvement

    def keep_card(self, player, cards, game):
        all_cards = player.hand + cards
        return all_cards[self.best_move.keep]   # Retourne la carte à garder du meilleur mouvement

    def copy_player_view(self, simulated_board):
        # Crée une copie de l'état du jeu en tenant compte des informations du joueur
        copied_board = deepcopy(simulated_board)  # Commence par une copie profonde

        # Met à jour les informations avec les données que le joueur actif connaît
        active_player = copied_board.active_player

        copied_board.deck.draw_pile = active_player.deck_memory

        for player in copied_board.players:
            if not copied_board.is_active_player(player):
                if not active_player.player_memory:
                    player.hand.pop()
                    player.hand.append(Card('unknown', -1))
                player.deck_memory = [Card('unknown', -1)] * len(copied_board.deck.draw_pile)

        return copied_board

    def depth_algo(self, _game, depth, maximizing):
        game = deepcopy(_game)
        weighted_evals = 0
        total_probability = 0

        if depth == 0 or game.is_round_end():
            print("\n\nEnvoyé\n\n")
            return self.evaluate_board(game)

        elif maximizing:
            max_eval = float('-inf')
            best_move = None
            for possible_hand, proba1 in zip(*self.get_possible_hands(game, game.active_player)):
                game.active_player.hand = possible_hand
                for possible_move in game.get_possible_moves(game.active_player):
                    print(str(possible_move))
                    op = game.get_other_player(game.active_player)
                    for possible_card, proba2 in zip(*self.get_possible_cards(game, op)):
                        test_game = deepcopy(game)
                        op.hand = [Card(possible_card)]
                        next_game = test_game.simulate_player_turn(game.active_player, possible_move)
                        eval = self.depth_algo(next_game, depth - 1, False)
                        print(f"Eval finale : {eval}")
                        if eval * proba1 * proba2 > max_eval:
                            max_eval = eval
                            best_move = possible_move
                        print(f"Best eval : {max_eval}")

            return best_move
        else:
            for possible_hand, proba1 in zip(*self.get_possible_hands(game, game.active_player)):
                game.active_player.hand = possible_hand
                for possible_move in game.get_possible_moves(game.active_player):
                    op = game.get_other_player(game.active_player)
                    for possible_card, proba2 in zip(*self.get_possible_cards(game, op)):
                        test_game = deepcopy(game)
                        op.hand = [Card(possible_card)]
                        next_game = test_game.simulate_player_turn(game.active_player, possible_move)
                        eval = self.depth_algo(next_game, depth - 1, False)
                        print(f"Eval inter : {eval}")
                        weighted_evals += eval * proba1 * proba2
                        total_probability += 1
            return weighted_evals / total_probability if total_probability != 0 else 0


    def get_possible_cards(self, game, player):
        possible_cards = []
        probabilities = []
        named_cards = ["Spy", "Guard", "Priest", "Baron", "Handmaid", "Prince", "Chancellor", "King", "Countess", "Princess"]
        nbr_unknown_card = (
                sum(1 for card in player.deck_memory if card.name == "unknown") +
                sum(1 for card in player.player_memory if card.name == "unknown") +
                sum(1 for card in player.hand if card.name == "unknown")
        )

        if player.card() and player.card().name != "unknown":
            possible_cards.append(player.card().name)
        else:
            for card_name in named_cards:
                count_card = (
                        game.discarded_cards.get(card_name, 0) +
                        sum(1 for card in player.deck_memory if card.name == card_name) +
                        sum(1 for card in player.player_memory if card.name == card_name) +
                        sum(1 for card in player.hand if card.name == card_name)
                    )

                # Calculate the total count of the card in the game
                num_card = {"Spy": 2, "Guard": 6, "Priest": 2, "Baron": 2, "Handmaid": 2, "Prince": 2, "Chancellor": 2,
                            "King": 1, "Countess": 1, "Princess": 1}
                # Check if the card is still possible
                probability = (num_card.get(card_name, 0) - count_card) / nbr_unknown_card if nbr_unknown_card != 0 else 0
                if probability > 0:
                    possible_cards.append(card_name)
                    probabilities.append(probability)

        return possible_cards, probabilities

    def get_possible_hands(self, game, player):
        possible_hands = []
        probabilities = []
        named_cards = ["Spy", "Guard", "Priest", "Baron", "Handmaid", "Prince", "Chancellor", "King", "Countess",
                       "Princess"]
        unknown_cards = sum(1 for card in player.hand if card.name == "unknown")
        nbr_unknown_card = (
                sum(1 for card in player.deck_memory if card.name == "unknown") +
                sum(1 for card in player.player_memory if card.name == "unknown") +
                sum(1 for card in player.hand if card.name == "unknown")
        )

        if unknown_cards == 0:
            possible_hands.append(player.hand)
            probabilities.append(1)
        elif unknown_cards == 1:
            known_card = next((card for card in player.hand if card.name != "unknown"))
            print(f"carte connue : {known_card.name}")
            for card_name in named_cards:
                possible_hand = [known_card, Card(card_name)]
                count_card = (
                        game.discarded_cards.get(card_name, 0) +
                        sum(1 for card in player.deck_memory if card.name == card_name) +
                        sum(1 for card in player.player_memory if card.name == card_name) +
                        sum(1 for card in player.hand if card.name == card_name)
                )
                num_card = {"Spy": 2, "Guard": 6, "Priest": 2, "Baron": 2, "Handmaid": 2, "Prince": 2, "Chancellor": 2,
                            "King": 1, "Countess": 1, "Princess": 1}
                probability = (num_card.get(card_name, 0) - count_card) / nbr_unknown_card if nbr_unknown_card != 0 else 0
                # Check if the card is still possible
                if probability > 0:
                    possible_hands.append(possible_hand)
                    probabilities.append(probability)
        elif unknown_cards == 2:
            for card_name_1, card_name_2 in product(named_cards, repeat=2):
                possible_hand = [Card(card_name_1), Card(card_name_2)]
                count_card_1 = (
                        game.discarded_cards.get(card_name_1, 0) +
                        sum(1 for card in player.deck_memory if card.name == card_name_1) +
                        sum(1 for card in player.player_memory if card.name == card_name_1) +
                        sum(1 for card in player.hand if card.name == card_name_1)
                )
                count_card_2 = (
                        game.discarded_cards.get(card_name_2, 0) +
                        sum(1 for card in player.deck_memory if card.name == card_name_2) +
                        sum(1 for card in player.player_memory if card.name == card_name_2) +
                        sum(1 for card in player.hand if card.name == card_name_2)
                )
                if card_name_1 == card_name_2:
                    count_card_2 += 1
                num_card = {"Spy": 2, "Guard": 6, "Priest": 2, "Baron": 2, "Handmaid": 2, "Prince": 2, "Chancellor": 2,
                            "King": 1, "Countess": 1, "Princess": 1}
                probability_1 = (num_card.get(card_name_1, 0) - count_card_1) / nbr_unknown_card if nbr_unknown_card != 0 else 0
                probability_2 = (num_card.get(card_name_2, 0) - count_card_2) / nbr_unknown_card-1 if nbr_unknown_card-1 != 0 else 0
                probability = probability_1 * probability_2
                if probability > 0:
                    possible_hands.append(possible_hand)
                    probabilities.append(probability)

        for i, hand in enumerate(possible_hands):
            print(f" main{i + 1} : {', '.join(str(card) for card in hand)}, probability: {probabilities[i]}")

        return possible_hands, probabilities


    def evaluate_board(self, simulated_board):
        evaluation_score = 0
        # Check if the current player has been eliminated
        for p in simulated_board.players:
            if p.name == self.original_player.name:
                op = simulated_board.get_other_player(p)
                if not p.hand:
                    evaluation_score -= 100 # Deduct a high score for being eliminated
                if p.has_played_or_discarded_spy and op.has_played_or_discarded_spy:
                    evaluation_score -= 5
                elif p.has_played_or_discarded_spy and not op.has_played_or_discarded_spy:
                    evaluation_score += 10
                elif not p.has_played_or_discarded_spy and op.has_played_or_discarded_spy:
                    evaluation_score -= 15
                if p.player_memory:
                    evaluation_score += 2 * (1 + p.player_memory[0].value)

                #TODO : ajouter des scores en fonctions du score de la carte et de la présence ou non du Roi, de gardes, de princes, etc.. dans les cartes possibles
                # pour chaque carte dans la carte du joueur en fonction de sa value ou nom on compare, en faire environ 10 par cartes

            else:
                if not p.hand:
                    evaluation_score += 100 # Add a high score for eliminating the other player



        # Add more evaluation factors based on the specific game rules and strategies
        return evaluation_score




