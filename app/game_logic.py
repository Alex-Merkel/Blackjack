import itertools
import random
import time


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

    def get_hand_info(self):
        # Create a list of dictionaries with card information
        hand_info = [{'suit': card.suit, 'value': card.value} for card in self.hand]
        return hand_info

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

    def get_game_state(self):
        player_info = [str(card) for card in self.players[0].hand]
        dealer_info = [str(card) for card in self.players[1].hand]
        game_state = {
            'player_cards': player_info,
            'dealer_cards': dealer_info,
        }
        return game_state


    def hit(self, player):
        new_card = self.deck.cards.pop()
        player.hand.append(new_card)
        if isinstance(player, Dealer):
            player.show(True)
            self.checkBust(player, is_dealer=True)
        else:
            player.getHand()
        self.checkBust(player)
        print(str(new_card))
        return str(new_card)

    # NEED TO ADJUST
    def player_choice(self, player):
        answer = input("Hit or Stand? (H/S): ")
        if answer.lower() == "h":
            self.hit(player)
        if answer.lower() == "s":
            self.players_turn = False
            Dealer.hand[1] = initialDealerCard
            dealer_score = Dealer.score_aces  
            game_state = self.get_game_state(player.score_aces, dealer_score)
            return game_state

    def checkBust(self, player, is_dealer=False):
        if player.isBusted:
            if is_dealer:
                print("Dealer busts")
            else:
                print("You bust")
            self.players_turn = False
            self.player_lost()


    def player_lost(self):
        print("You've lost")

    def draw(self):
        print("It is a draw. You receive your bet back.")

    def player_won(self):
        print("You won! Here are your chips.")

    def compare(self, player, dealer):
        if player.score_aces > dealer.score_aces:
            self.player_won()
        elif player.score_aces == dealer.score_aces:
            self.draw()
        else:
            self.player_lost()

    def reset(self):
        for player in self.players:
            player.resetHand()

    def replay(self):
        again = None
        while again != "y" or again != "n":
            again = input("Play again? (Y/N):")
            if again.lower() == "y":
                return True
            elif again.lower() == "n":
                print("Thanks for playing!")
                return False
            else:
                print("Invalid input, please try again.")

    def play(self):
        self.deck = Deck()
        player = Player()
        dealer = Dealer()
        self.players = [player, dealer]
        self.deck.fill(4)
        self.deck.shuffle()
        self.deal()
        # Save initial dealer card to use later
        initialDealerCard = dealer.hand[0]
        print(initialDealerCard)

        # while self.players_turn:
        #     player.getHand()
        #     self.player_choice(player)

        # if not player.isBusted:
        #     dealer.show()
        #     while not self.players_turn:
        #         if dealer.score_aces < 17:
        #             print("Dealer hits")
        #             self.hit(dealer)
        #             time.sleep(1)
        #         elif dealer.score_aces >= 17 and not dealer.isBusted:
        #             print(f"Dealer stands with {dealer.score_aces}.")
        #             break
        #         elif dealer.isBusted:
        #             self.player_won()
        #             break

        # if not dealer.isBusted:
        #     self.compare(player, dealer)

        # again = self.replay()
        # if not again:
        #     self.reset()


def main():
    game = Blackjack()
    game.play()