from Deck import Deck
import random


class LoveLetterGame:
    def __init__(self, players, verbose=False):
        # TODO: Add GUI support
        """
        Initialize a new LoveLetter game with the given players.

        :param players: A list of Player objects participating in the game.
        :param verbose: If True, the game will print detailed information about each turn.
        """
        self.players = players
        self.deck = Deck()
        self.deck.fill()
        self.deck.shuffle()
        # Points to win the game (6 for 2 players, 5 for 3 players, 4 for 4 players, 3 for 5-6 players)
        self.target_points = 6 - max(0, len(players) - 2) if len(players) <= 5 else 3
        self.points = {player: 0 for player in players}
        self.active_player = players[0] # The player whose turn it is
        self.spy_count = 0      # Tracks the number of Spy cards played
        self.verbose = verbose

        if len(players) > 6 or len(players) < 2:
            raise ValueError("The number of players should be between 2 and 6.")


    def distribute_cards(self):
        """
        Distribute one card to each player from the deck at the start of the game.
        """
        for player in self.players:
            player.draw(self.deck.draw())


    def play_turn(self):
        """
        Conduct a single turn in the game.
        """
        for current_player in self.players:
            # set active player to current player
            self.active_player = current_player
            # if only one player left, they win the round
            if len([j for j in self.players if len(j.hand) > 0]) == 1:
                self.end_of_round()
                break

            if not current_player.reachable:
                current_player.reachable = True  # Make the player reachable again

            if current_player.hand and self.deck.draw_pile:
                current_player.draw(self.deck.draw())
                if current_player.countess():
                    for card in current_player.hand:
                        if card.name == "Countess":
                            current_player.hand.remove(card)
                            played_card = card  # Use the removed card
                            break
                else:
                    played_card = current_player.choose_card_to_play()  # Player plays a card from their hand
                    if self.verbose:
                        print(f"{current_player.name} plays the {played_card.name} card")
                self.resolve_effect(played_card)
            elif not self.deck.draw_pile:
                self.end_of_round()
                break


    def resolve_effect(self, card):
        """
        Resolve the effect of the played card.
        """
        effect_method = self.get_effect_method(card.name)
        if effect_method:
            effect_method()


    def get_effect_method(self, card_name):
        """
        Return the method corresponding to the card's effect.
        """
        return {
            "Spy": self.effect_spy,
            "Guard": self.effect_guard,
            "Priest": self.effect_priest,
            "Baron": self.effect_baron,
            "Handmaid": self.effect_handmaid,
            "Prince": self.effect_prince,
            "Chancellor": self.effect_chancellor,
            "King": self.effect_king,
            "Countess": self.effect_countess,
            "Princess": self.effect_princess
        }.get(card_name, None)
    

    def effect_spy(self):
        current_player = self.active_player
        current_player.has_played_or_discarded_spy = True


    def effect_guard(self):
        target_player = self.active_player.choose_target_player(self.players)
        if target_player is not None:
            guessed_character = self.active_player.choose_character()
            if self.verbose:
                print(f"{self.active_player.name} chooses {target_player.name} as target and guesses {guessed_character}")
            if guessed_character in [c.name for c in target_player.hand]:
                if self.verbose:
                    print("The guess is correct. The target player is eliminated from the round.")
                target_player.hand = []
            else:
                if self.verbose:
                    print("The guess is incorrect. Nothing happens.")
                pass
        else :
            if self.verbose:
                print("No player is targetable, the card has no effect!")
            pass


    def effect_priest(self):
        target_player = self.active_player.choose_target_player(self.players)
        if target_player is not None:
            if self.verbose:
                print(f"{self.active_player.name} chooses {target_player.name} as target and looks at {target_player.card().name}")
            pass
        else :
            if self.verbose:
                print("No player is targetable, the card has no effect!")
            pass


    def effect_baron(self):
        target_player = self.active_player.choose_target_player(self.players)
        if target_player is not None:
            current_player = self.active_player
            current_player_card = current_player.card()
            target_player_card = target_player.card()
            if self.verbose:
                print(f"{current_player.name} chooses {target_player.name} as target.")
                print(f"{current_player.name} has the {current_player_card.name} card ({current_player_card.value}).")
                print(f"{target_player.name} has the {target_player_card.name} card ({target_player_card.value}).")
            if current_player_card.value > target_player_card.value:
                if self.verbose:
                    print(f"{current_player.name} wins the duel. {target_player.name} loses the round.")
                target_player.hand = []
            elif current_player_card.value < target_player_card.value:
                if self.verbose:
                    print(f"{target_player.name} wins the duel. {current_player.name} loses the round.")
                current_player.hand = []
            else:
                if self.verbose:
                    print("Tie, no one loses the round.")
                pass
        else :
            if self.verbose:
                print("No player is targetable, the card has no effect!")
            pass


    def effect_handmaid(self):
        self.active_player.reachable = False
        if self.verbose:
            print(f"{self.active_player.name} is not targetable for a turn!")


    def effect_prince(self):
        target_player = self.active_player.choose_target_player(self.players)
        if target_player is not None and len(self.deck.draw_pile) > 0:
            if self.verbose:
                print(f"{self.active_player.name} chooses {target_player.name}")
            discarded_card = target_player.discard()
            # if the discarded card is a spy, set has_played_or_discarded_spy to True
            if discarded_card.name == "Spy":
                if self.verbose:
                    print(f"{target_player.name} discarded the Spy")
                target_player.has_played_or_discarded_spy = True
            elif discarded_card.name == "Princess": # if the discarded card is a princess, the player is eliminated
                if self.verbose:
                    print(f"{target_player.name} discarded the Princess and is eliminated from the round.")
                target_player.hand = []
            target_player.draw(self.deck.draw())
        else :
            if self.verbose:
                print("No player is targetable, the card has no effect!")
            pass


    def effect_chancellor(self):
        current_player = self.active_player
        # Check if there are enough cards in the draw pile.
        drawn_cards = []
        if len(self.deck.draw_pile) >= 2:
            drawn_cards = [self.deck.draw(), self.deck.draw()]

        # Display the drawn cards.
        if self.verbose:
            print(f"{current_player.name} draws {len(drawn_cards)} card(s): {[card.name for card in drawn_cards]}")
        # Check if any cards were drawn before continuing.
        if len(drawn_cards) > 0:
            card_to_keep = current_player.keep_card(drawn_cards)
            if self.verbose:
                print(f"{current_player.name} keeps the {card_to_keep.name} card ({card_to_keep.value}).")
            # Return the other card(s) to the draw pile.
            if card_to_keep in current_player.hand:
                cards_to_return = drawn_cards
            else:
                cards_to_return = [card for card in drawn_cards if card != card_to_keep] + [current_player.hand.pop()] 
            # Check if the player discarded a spy or princess.
            if "Spy" in [card.name for card in cards_to_return]:
                current_player.has_played_or_discarded_spy = True
                if self.verbose:
                    print(f"{current_player.name} discarded the Spy")
            if "Princess" in [card.name for card in cards_to_return]:
                if self.verbose:
                    print(f"{current_player.name} discarded the Princess and is eliminated from the round.")
                current_player.hand = []
            # Return the cards to the draw pile.
            self.deck.draw_pile.extend(cards_to_return)


    def effect_king(self):
        target_player = self.active_player.choose_target_player(self.players)
        if target_player is not None:
            current_player = self.active_player
            if self.verbose:
                print(f"{current_player.name} chooses {target_player.name} as target.")
            current_player_card = current_player.card()
            target_player_card = target_player.card()
            if self.verbose:
                print(f"{current_player.name} has the {current_player_card.name} card ({current_player_card.value}).")
                print(f"{target_player.name} has the {target_player_card.name} card ({target_player_card.value}).")
            current_player.hand.remove(current_player_card)
            target_player.hand.remove(target_player_card)
            current_player.hand.append(target_player_card)
            target_player.hand.append(current_player_card)
            if self.verbose:
                print(f"{current_player.name} and {target_player.name} have exchanged their cards.")
        else :
            if self.verbose:
                print("No player is targetable, the card has no effect!")
            pass


    def effect_countess(self):
        pass


    def effect_princess(self):
        current_player = self.active_player
        if self.verbose:
            print(f"{current_player.name} plays the Princess and is eliminated from the round.")
        current_player.hand = []


    def end_of_round(self):
        if len(self.deck.draw_pile) == 0 or (len([j for j in self.players if len(j.hand) > 0]) == 1):
            players_in_game = [j for j in self.players if len(j.hand) > 0]
            if players_in_game:
                max_card_value = max([max([c.value for c in j.hand]) for j in players_in_game])
                winning_players = [j for j in players_in_game if max([c.value for c in j.hand]) == max_card_value]
                if len(winning_players) == 1:
                    if self.verbose:
                        print(f"{winning_players[0].name} wins the round and gets 1 point!")
                else:
                    if self.verbose:
                        print(f"{', '.join([j.name for j in winning_players])} win the round and get 1 point each!")
                for winning_player in winning_players:
                    self.points[winning_player] += 1
                    # add spy bonus if the spy was play or discarded by only one player
                    spy_count = sum([1 for j in self.players if j.has_played_or_discarded_spy])
                    if spy_count == 1:
                        benefit_player = [j for j in self.players if j.has_played_or_discarded_spy][0]
                        self.points[benefit_player] += 1
                        if self.verbose:
                            print(f"{benefit_player.name} gets 1 bonus point for being the only player to play or discard a Spy card.")
                if self.verbose:
                    print(f"Current points: {[f'{j.name}: {self.points[j]}' for j in self.points]}")
                self.new_round()


    def new_round(self):
        self.deck = Deck()
        self.deck.fill()
        self.deck.shuffle()
        for player in self.players:
            player.hand = []
        self.distribute_cards()
        self.active_player = self.players[0]
        # for each player, reset has_played_or_discarded_spy to False
        for player in self.players:
            player.has_played_or_discarded_spy = False
