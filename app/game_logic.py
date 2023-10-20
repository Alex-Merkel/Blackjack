import itertools
import random
# Get rid of import time???
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

    # def show(self, all = False):
    #     print("\t\t\tThe dealer has:")
    #     if all:
    #         for card in self.hand:
    #             print(card)
    #     else:
    #         print(self.hand[0])
    #         print('PUT SOMETHING HERE')


class Blackjack:
    def __init__(self):
        self.players = []
        self.deck = []
        self.players_turn = True
        self.inital_dealer_card = None

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

    def get_game_state(self, player_score, dealer_score):
        player_info = [str(card) for card in self.players[0].hand]
        dealer_info = [str(card) for card in self.players[1].hand]

        game_state = {
            'player_cards': player_info,
            'dealer_cards': dealer_info,
            'player_score': player_score,
            'dealer_score': dealer_score,
        }
        return game_state



    def hit(self, player):
        new_card = self.deck.cards.pop()
        player.hand.append(new_card)
        if isinstance(player, Dealer):
            # Should be good to delete line below!!!???
            # player.show(True)
            self.checkBust(player, is_dealer=True)
        else:
            print('watermelons_def hit')
            # player.getHand()
        self.checkBust(player)
        print(str(new_card))
        return str(new_card)
    
    def dealer_turn(self):
        dealer = self.players[1]
        while dealer.score_aces < 17:
            self.hit(dealer)

        # Check if the dealer has busted after finishing their turn
        self.checkBust(dealer, is_dealer=True)

    def stand(self):
        self.dealer_turn()

        # Get player and dealer scores
        player_score = self.players[0].score_aces
        dealer_score = self.players[1].score_aces


        # Compare the scores
        if dealer_score > player_score:
            print("Dealer wins!")
        elif dealer_score < player_score:
            print("Player wins!")
        else:
            print("It's a draw!")


    def checkBust(self, player, is_dealer=False):
        if player.isBusted:
            if is_dealer:
                # Check if the dealer has any Aces and reduce their score by 10 if it's over 21
                while player.score_aces > 21 and player.aces > 0:
                    player.hand[player.hand.index(next(card for card in player.hand if card.value == 'Ace'))].value = '1'
                if player.score_aces > 21:
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


    def initiate_game(self):
        self.deck = Deck()
        player = Player()
        dealer = Dealer()
        self.players = [player, dealer]
        self.deck.fill(4)
        self.deck.shuffle()
        self.deal()
        # Save initial (hidden / face-down) dealer card to use later
        self.initial_dealer_card = dealer.hand[0]
        print(self.initial_dealer_card)

    def play_again(self):
        # maybe try self.reset() and get rid of 2 lines below???
        self.players[0].resetHand()
        self.players[1].resetHand()
        self.players_turn = True 
        self.inital_dealer_card = None

        # Return the game state
        player_score = self.players[0].score_aces
        dealer_score = self.players[1].score_aces
        game_state = self.get_game_state(player_score, dealer_score)
        
        return game_state