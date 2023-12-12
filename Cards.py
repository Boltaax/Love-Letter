class Card:
    def __init__(self, name, value):
        """
        Initialize a new card with a given name and value.

        :param name: The name of the card (e.g., 'Guard', 'Priest').
        :param value: The value or strength of the card.
        """
        self.name = name
        self.value = value


    def __str__(self):
        """
        Return a string representation of the card.
        """
        return f"Card {self.name} ({self.value})"