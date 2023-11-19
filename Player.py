import random


class Player:
    def __init__(self, name, is_human=False):
        """
        Initialize a new player with a given name.

        :param name: The name of the player.
        :param is_human: Whether the player is human or not.
        """
        self.name = name
        self.hand = []
        self.reachable = True
        self.is_human = is_human
        self.has_played_or_discarded_spy = False


    def draw(self, card):
        """
        Add a card to the player's hand.

        :param card: The card to be added to the hand.
        """
        if card is not None:
            self.hand.append(card)


    def choose_card_to_play(self):
        """
        Choose a card to play. Human players choose a card, while AI players choose randomly.

        :return: The chosen card.
        """
        choosen_card = self._choose_from_list(self.hand, "choose a card to play: ")
        self.hand.remove(choosen_card)
        return choosen_card


    def card(self):
        """
        Return the first and only card from the player's hand.

        :return: The first and only card from the hand.
        """
        if self.hand:
            return self.hand[0]
        else:
            return None


    def discard(self):
        """
        Remove and return the last card from the player's hand.

        :return: The last card from the hand.
        """
        if self.hand:
            return self.hand.pop()
        else:
            return None


    def keep_card(self, cards):
        """
        Choose a card to keep after playing the "Chancellor" card. Human players choose a card, while AI players choose randomly.

        :param cards: The list of cards to choose from.

        :return: The chosen card.
        """
        if self.is_human:
            # Display cards and prompt for choice
            i = 0
            for i, card in enumerate(cards):
                print(f"{i}: {card}")
            print(f"{i+1}: {self.hand[0]}")
            
            # Validate user input
            while True:
                choice = input(f"{self.name}, choose a card to keep: ")
                if not choice.isdigit():
                    print("Invalid input. Please enter a number.")
                    continue
                choice = int(choice)
                if choice < 0 or choice >= len(cards) + 1:
                    print("Invalid input. Please enter a valid card number.")
                    continue
                break
            
            if choice == len(cards):
                return self.hand[0]
            else:
                return cards[choice]
        else:
            return cards[random.randint(0, len(cards)-1)]


    def countess(self):
        """
        :return: Whether the player has the "Countess" card and a "King" or "Prince" card in hand.
        """
        has_comtesse = any(card.name == "Comtesse" for card in self.hand)
        has_king_or_prince = any(card.name in ["King", "Prince"] for card in self.hand)
        return has_comtesse and has_king_or_prince


    def choose_target_player(self, players):
        """
        Choose a target player to use a card on. Human players choose a player, while AI players choose randomly.

        :param players: The list of players to choose from.

        :return: The chosen player.
        """
        available_players = [p for p in players if p != self and p.reachable and p.hand]
        return self._choose_from_list(available_players, "Choose a player to target: ")


    def choose_character(self):
        """
        Choose a character to guess because of the "Guard" card. Human players choose a character, while AI players choose randomly.

        :return: The chosen character.
        """
        # List of all possible characters
        possible_characters = ["Spy", "Priest", "Baron", "Handmaid", "Prince", "Chancellor", "King",
                                 "Countess", "Princess"]
        return self._choose_from_list(possible_characters, "Choose a character to guess: ")

    
    def _choose_from_list(self, items, prompt):
        """
        Utility method for choosing an item from a list, handling both human and AI players.

        :param items: The list of items to choose from.
        :param prompt: The prompt to display for human players.

        :return: The chosen item.
        """
        if not items:
            return None

        if self.is_human:
            for i, item in enumerate(items):
                print(f"{i}: {item}")
            while True:
                choice = input(f"{self.name}, {prompt}")
                if choice.isdigit() and 0 <= int(choice) < len(items):
                    return items[int(choice)]
                print("Invalid input. Please enter a valid number.")
        else:
            return random.choice(items)


    def __str__(self):
        """
        Return a string representation of the player.
        """
        return f"Player {self.name} with hand {self.hand}"