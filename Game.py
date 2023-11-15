from Deck import Deck
import random

class LoveLetterGame:
    def __init__(self, players):
        self.players = players
        self.deck = Deck()
        self.deck.fill()
        self.deck.shuffle()
        self.target_points = 6 # 6 points to win the game in a 2-player game
        self.points = {player: 0 for player in players}
        self.active_player = 0
        self.spy_count = 0

    def distribute_cards(self):
        for player in self.players:
            player.draw(self.deck.draw())

    def play_turn(self):
        global played_card
        current_player = self.players[self.active_player]
        #   print(f"Turn of {current_player.name}")
        if not current_player.reachable:
            #   print(f"{current_player.name} is reachable again!")
            current_player.reachable = True

        if len(current_player.hand) > 0 and len(self.deck.draw_pile) > 0:
            current_player.draw(self.deck.draw())
            if current_player.countess():
                for card in current_player.hand:
                    if card.name == "Countess":
                        current_player.hand.remove(card)
                        played_card = card  # Use the removed card
                        break
            else:
                played_card = current_player.play_best_card()  # Player plays a card from their hand
            #   print(f"{current_player.name} plays the {played_card.name} card")
            self.resolve_effect(played_card)
        self.end_of_round()


    def resolve_effect(self, card):
        if played_card.name == "Spy":
            self.spy_count += 1
        if card.name == "Guard":
            target_player = self.choose_target_player()
            if target_player is not None:
                guessed_character = self.choose_character()
                #   print(f"{self.players[self.active_player].name} chooses {target_player.name} as target and guesses {guessed_character}")
                if guessed_character in [c.name for c in target_player.hand]:
                    target_player.hand = [c for c in target_player.hand if c.name != guessed_character]
                    #   print(f"The guess is correct. {target_player.name} loses the {guessed_character} card")
                else:
                    #   print("The guess is incorrect. Nothing happens.")
                    pass
            else :
                #   print("No player is targetable, the card has no effect!")
                pass

        elif card.name == "Priest":
            target_player = self.choose_target_player()
            if target_player is not None:
                #   print(f"{self.players[self.active_player].name} chooses {target_player.name} as target and looks at {target_player.show_card().name}")
                pass
            else :
                #   print("No player is targetable, the card has no effect!")
                pass
        elif card.name == "Baron":
            target_player = self.choose_target_player()
            if target_player is not None:
                current_player = self.players[self.active_player]
                current_player_card = current_player.show_card()
                target_player_card = target_player.show_card()
                #   print(f"{current_player.name} chooses {target_player.name} as target.")
                #   print(f"{current_player.name} has the {current_player_card.name} card ({current_player_card.value}).")
                #   print(f"{target_player.name} has the {target_player_card.name} card ({target_player_card.value}).")
                if current_player_card.value > target_player_card.value:
                    #   print(f"{current_player.name} wins the duel. {target_player.name} loses the round.")
                    target_player.hand.remove(target_player_card)
                elif current_player_card.value < target_player_card.value:
                    #   print(f"{target_player.name} wins the duel. {current_player.name} loses the round.")
                    current_player.hand.remove(current_player_card)
                else:
                    #   print("Tie, no one loses the round.")
                    pass
            else :
                #   print("No player is targetable, the card has no effect!")
                pass
        elif card.name == "Handmaid":
            self.players[self.active_player].reachable = False
            #   print(f"{self.players[self.active_player].name} is not targetable for a turn!")
        elif card.name == "Prince":
            target_player = self.choose_target_player()
            if target_player is not None and len(self.deck.draw_pile) > 0:
                #   print(f"{self.players[self.active_player].name} chooses {target_player.name}")
                target_player.discard()
                target_player.draw(self.deck.draw())
            else :
                #   print("No player is targetable, the card has no effect!")
                pass
        elif card.name == "Chancellor":
            current_player = self.players[self.active_player]
            # Check if there are enough cards in the draw pile.
            drawn_cards = []
            for _ in range(2):
                if len(self.deck.draw_pile) > 0:
                    drawn_card = self.deck.draw()
                    drawn_cards.append(drawn_card)
                else:
                    #   print("The draw pile is empty.")
                    break
            # Display the drawn cards.
            #   print(f"{current_player.name} draws {len(drawn_cards)} cards: {[card.name for card in drawn_cards]}")
            # Check if any cards were drawn before continuing.
            if len(drawn_cards) > 0:
                card_to_keep = current_player.choose_card_to_keep(drawn_cards)
                #   print(f"{current_player.name} keeps the {card_to_keep.name} card ({card_to_keep.value}).")
                cards_to_return = [card for card in drawn_cards if card != card_to_keep]
                cards_to_return.reverse()  # Put the cards back in reverse order under the draw pile.
                self.deck.draw_pile.extend(cards_to_return)
        elif card.name == "King":
            target_player = self.choose_target_player()
            if target_player is not None:
                current_player = self.players[self.active_player]
                #   print(f"{current_player.name} chooses {target_player.name} as target.")
                current_player_card = current_player.show_card()
                target_player_card = target_player.show_card()
                #   print(f"{current_player.name} has the {current_player_card.name} card ({current_player_card.value}).")
                #   print(f"{target_player.name} has the {target_player_card.name} card ({target_player_card.value}).")
                current_player.hand.remove(current_player_card)
                target_player.hand.remove(target_player_card)
                current_player.hand.append(target_player_card)
                target_player.hand.append(current_player_card)
                #   print(f"{current_player.name} and {target_player.name} have exchanged their cards.")
            else :
                #   print("No player is targetable, the card has no effect!")
                pass
        elif card.name == "Countess":
            pass
        elif card.name == "Princess":
            current_player = self.players[self.active_player]
            #   print(f"{current_player.name} plays the Princess and is eliminated from the round.")
            current_player.hand.remove(current_player.show_card())


    def choose_target_player(self):
        target_player = None
        current_player = self.players[self.active_player]
        available_players = [j for j in self.players if (j != current_player and j.reachable and len(j.hand) > 0)]
        if len(available_players) > 0:
            target_player = random.choice(available_players)
        return target_player

    def choose_character(self):
        # List of all possible characters
        possible_characters = ["Spy", "Priest", "Baron", "Handmaid", "Prince", "Chancellor", "King",
                                 "Countess", "Princess"]
        # Choose a character at random from the remaining characters
        chosen_character = random.choice(possible_characters)
        return chosen_character

    def end_of_round(self):
        if len(self.deck.draw_pile) == 0 or (len([j for j in self.players if len(j.hand) > 0]) == 1):
            players_in_game = [j for j in self.players if len(j.hand) > 0]
            if players_in_game:
                winning_player = max(players_in_game, key=lambda j: max([c.value for c in j.hand]))
                # ADD SPY BONUS POINTS
                if len(self.deck.draw_pile) == 0:
                    #   print("There are no more cards in the draw pile!")
                    pass
                else :
                    #   print(f"{winning_player.name} is the last player standing.")
                    pass
                self.points[winning_player] += 1
                #   print(f"{winning_player.name} wins the round and gets 1 point.")
            self.new_round()
        else:
            if self.active_player == len(self.players) - 1:
                self.active_player = 0
            else:
                self.active_player += 1

    def new_round(self):
        self.deck = Deck()
        self.deck.fill()
        self.deck.shuffle()
        for player in self.players:
            player.hand = []
        self.distribute_cards()
        self.active_player = 0
