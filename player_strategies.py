from abc import ABC, abstractmethod
import random

def get_strategies():
    '''
    Returns a dictionary of all available strategies
    '''
    return {
        "Human": HumanStrategy,
        "Random": RandomStrategy
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


# TODO: Implement MinMaxStrategy