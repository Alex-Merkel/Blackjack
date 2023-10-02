import random
class Blackjack():
    def __init__(self):
        self.cards = list(range(1, 14)) * 4
        random.shuffle(self.cards)

    
class Player(Blackjack):
    def __init__(self):
        super().__init__()
        self.player_hand = [self.cards.pop(0), self.cards.pop(0)]



class Dealer(Blackjack):
    def __init__(self):
        super().__init__()
        self.dealer_hand = [self.cards.pop(0), self.cards.pop(0)]
        