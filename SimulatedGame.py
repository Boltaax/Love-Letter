from copy import deepcopy
from Game import LoveLetterGame

class LoveLetterSimulatedGame(LoveLetterGame):
    def __init__(self, original_game):
        super().__init__(original_game.players)
        self.deck = deepcopy(original_game.deck)
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
