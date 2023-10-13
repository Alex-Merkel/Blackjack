from flask import Flask, render_template
import itertools
import random
import time
# import routes from .routes


app = Flask(__name__)

@app.route('/')
def home():
    # Initialize the game and display the game interface
    game = Blackjack()
    return render_template('blackjack.html', game=game)


class Deck:
    suits = ['Diamonds', 'Spades', 'Clubs', 'Hearts']
    values = ['2', '3', '4', '5', '6', '7', '8', '9', '10', 'Jack', 'Queen', 'King', 'Ace']

    def __init__(self):
        self.cards = []
    
    def __len__(self):
        return len(self.cards)
    
    def fill(self, decks):
        for i in range(decks):
            for suit, value in itertools.product(self.suits, self.values):
                self.cards.append(Card(suit, value))
    
    def clear(self):
        self.cards = []

    def shuffle(self):
        random.shuffle(self.cards)


class Card:
    def __init__(self, suit, value):
        self.suit = suit
        self.value = value

    def __str__(self):
        return f"{self.value} of {self.suit}"
    
    @property
    def score(self):
        if self.value in ['Jack', 'Queen', 'King']:
            return 10
        if self.value == 'Ace':
            return 11
        else:
            return int(self.value)


class Player:
    def __init__(self):
        self.hand = []

    def getHand(self):
        print("\t\t\tThe player's hand:")
        for card in (self.hand):
            print(card)
            print("")
        print("")

    def resetHand(self):
        self.hand = []

    @property
    def aces(self):
        return len([card for card in self.hand if card.value == 'Ace'])
    
    @property
    def score(self):
        return sum([card.score for card in self.hand])

    @property
    def score_aces(self):
        score = self.score
        for ace in range(self.aces):
            if score > 21:
                score -= 10
        return score
    
    @property
    def isBusted(self):
        if self.score_aces > 21:
            return True
        return False
    

class Gambler(Player):
    def __init__(self, chips):
        super().__init__()
        self.chips = chips

    def bet(self):
        stake = input(f"Total chips: {self.chips}. Enter your bet amount: ")
        try:
            if int(stake) > self.chips:
                print("You cannot bet more than you have")
                self.bet()
            else:
                self.chips -= int(stake)
                return int(stake)
        except ValueError:
            print('Please enter a valid integer.')
            self.bet()

    
class Dealer(Player):
    def __init__(self):
        super().__init__()
        self.hand = []

    def show(self, all = False):
        print("\t\t\tThe dealer has:")
        if all:
            for card in self.hand:
                print(card)
        else:
            print(self.hand[0])
            print('PUT SOMETHING HERE')


class Blackjack:
    def __init__(self):
        self.players = []
        self.deck = []
        self.player_bet = 0
        self.players_turn = True

    def deal(self):
        print(f"There are {len(self.deck)} cards left in the deck.")
        if len(self.deck) < 104:
            print('Reshuffling...')
            self.deck.clear()
            self.deck.fill(4)
            self.deck.shuffle()
        for i in range(2):
            for player in self.players:
                player.hand.append(self.deck.cards.pop())

    def hit(self, player):
        player.hand.append(self.deck.cards.pop())
        if isinstance(player, Dealer):
            player.show(True)
        else:
            player.getHand()
        self.checkBust(player)
        print(f"Player score: {player.score_aces}")

    def player_choice(self, player):
        answer = input("Hit or Stand? (H/S): ")
        if answer.lower() == "h":
            self.hit(player)
        if answer.lower() == "s":
            print(f"Standing at: {player.score_aces}")
            self.players_turn = False

    def checkBust(self, player):
        if player.isBusted:
            if(isinstance(player, Gambler)):
                print("You bust")
                self.players_turn = False
                self.player_lost()
            elif(isinstance(player, Dealer)):
                print("Dealer busts")

    def player_lost(self):
        print("You've lost")

    def draw(self, player):
        print(f"It is a draw. You receive your {self.player_bet} back.")
        player.chips += self.player_bet

    def player_won(self, player):
        print(f"You won! Here are {self.player_bet * 2} chips.")
        player.chips += self.player_bet * 2

    def compare(self, player, dealer):
        if player.score_aces > dealer.score_aces:
            self.player_won(player)
        elif player.score_aces == dealer.score_aces:
            self.draw(player)
        else:
            self.player_lost()

    def reset(self):
        for player in self.players:
            player.resetHand()
        self.player_bet = 0

    def replay(self, player):
        again = None
        while again != "y" or again != "n":
            again = input("Play again? (Y/N):")
            if again.lower() == "y":
                return True
            elif again.lower() == "n":
                print(f"You leave with {player.chips} chips, thanks for playing!")
                return False
            else:
                print("Invalid input, please try again.")

    def play(self):
        print("This is Blackjack")
        self.deck = Deck()
        player = Gambler(100)
        dealer = Dealer()
        self.players = [player, dealer]
        self.deck.fill(4)
        self.deck.shuffle()
        running = True

        while running:
            if self.players[0].chips == 0:
                print("You've run out of chips")
                break
            self.player_bet = player.bet()
            self.deal()
            dealer.show()
            player.getHand()
            while self.players_turn:
                self.player_choice(player)
            if not player.isBusted:
                dealer.show()
                while not self.players_turn:
                    if dealer.score_aces < 17:
                        print("Dealer hits")
                        self.hit(dealer)
                        time.sleep(1)
                    elif dealer.score_aces >= 17 and not dealer.isBusted:
                        print(f"Dealer stands with {dealer.score_aces}.")
                        break
                    elif dealer.isBusted:
                        self.player_won(player)
                        break
                if not dealer.isBusted:
                    self.compare(player, dealer)
            again = self.replay(player)
            if not again:
                running = False
            self.players_turn = True
            self.reset()

def main():
    game = Blackjack()
    game.play()


# if __name__ == "__main__":
#     main()

# Possibly this one?
if __name__ == "__main__":   
    app.run()