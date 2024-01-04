class Move:
    def __init__(self, card=None, target=None, character=None, keep=None):
        self.card = card
        self.target = target
        self.character = character
        self.keep = keep

    def __str__(self):
        return f"\n(Carte : {str(self.card)} Target : {str(self.target)} Character : {self.character} Keep : {self.keep})"

