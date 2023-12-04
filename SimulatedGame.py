from copy import deepcopy
from Game import LoveLetterGame

class LoveLetterSimulatedGame(LoveLetterGame):
    def __init__(self, original_game):
        super().__init__(original_game.players)
        self.deck = deepcopy(original_game.deck)
        self.discarded_cards = original_game.discarded_cards
        self.points = deepcopy(original_game.points)
        self.active_player = original_game.active_player
        self.spy_count = original_game.spy_count
        self.verbose = False  # Set to True for debugging if needed

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

    def get_possible_moves(self, all_players, player):
        """
        Get a list of possible moves for the player in the current game state.

        :param player: the player whose it the turn to play.

        :param all_players: A list of all players in the game.

        :return: A list of possible moves. Each move is represented as a tuple (action, card, target),
                 where 'action' is either 'play' or 'discard', 'card' is the card to be played or discarded,
                 and 'target' is the target player or -1 (no specific target).
        """
        possible_moves = []

        if player.hand:
            for card in player.hand:
                # Check if the card has a specific target
                if card.name == "Guard" or card.name == "Baron" or card.name == "Priest" or card.name == "King":
                    # Get a list of targetable players
                    targetable_players = [p for p in all_players if p != player and p.reachable and p.hand]
                    for target_player in targetable_players:
                        possible_moves.append((card, target_player))
                elif card.name == "Prince":
                    # Get a list of targetable players
                    targetable_players = [p for p in all_players and p.reachable and p.hand]
                    for target_player in targetable_players:
                        possible_moves.append((card, target_player))
                else:
                    possible_moves.append((card, -1))

        return possible_moves

    def get_possible_moves(self, player):
        """
        Get a list of possible moves for the given player in the current simulated game state.

        :param player: The player for whom to generate possible moves.

        :return: A list of possible moves. Each move is represented as a tuple (action, card),
                 where 'action' is either 'play' or 'discard', and 'card' is the card to be played or discarded.
        """
        possible_moves = []

        if player.hand:
            # Add all playable cards
            for card in player.hand:
                possible_moves.append(('play', card))

        return possible_moves
