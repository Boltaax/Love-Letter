class Move:
    def __init__(self, card=None, target=None, character=None, keep=None):
        self.card = card
        self.target = target
        self.character = character
        self.keep = keep

    def __str__(self):
        """
        Returns a string representation of the Move object.

        The string includes the card, target, character, and keep attributes.

        Returns:
            str: A string representation of the Move object.
        """
        return f"\n(Carte : {str(self.card)} Target : {str(self.target)} Character : {self.character} Keep : {self.keep})"

