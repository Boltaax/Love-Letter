class Card:
    def __init__(self, name, value=None):
        """
        Initialize a new card with a given name and value.

        :param name: The name of the card (e.g., 'Guard', 'Priest').
        :param value: The value or strength of the card.
        """
        self.name = name
        if value is not None:
            self.value = value
        else:
            self.set_value(name)

    def set_value(self, name):
        """
        Set the value of the card based on its name.

        Args:
            name (str): The name of the card.

        Returns:
            None
        """
        match name:
            case "unknown":
                self.value = -1
            case "Spy":
                self.value = 0
            case "Guard":
                self.value = 1
            case "Priest":
                self.value = 2
            case "Baron":
                self.value = 3
            case "Handmaid":
                self.value = 4
            case "Prince":
                self.value = 5
            case "Chancellor":
                self.value = 6
            case "King":
                self.value = 7
            case "Countess":
                self.value = 8
            case "Princess":
                self.value = 9

    def __str__(self):
        """
        Return a string representation of the card.
        """
        return f"Card {self.name} ({self.value})"