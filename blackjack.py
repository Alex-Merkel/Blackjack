import random

class Blackjack():

# When game begins:  shuffle the 4 suits together
    def __init__(self, player=0, player_hand=[], dealer=0, dealer_hand=[]):
        self.player = player
        self.dealer = dealer
        self.player_hand = player_hand
        self.dealer_hand = dealer_hand




# deal to both player and dealer (both cards showing for player, only 1 for dealer) (pop() to take from shuffled deck)
    def deal(self):
        cards = list(range(1, 14))
        clubs = cards
        diamonds = cards
        hearts = cards
        spades = cards
        all_cards = clubs + diamonds + hearts + spades
        random.shuffle(all_cards)
        active_hand = True
        while active_hand:            
            self.player_hand.append(all_cards.pop(0))
            self.dealer_hand.append(all_cards.pop(0))
            self.player_hand.append(all_cards.pop(0))
            print(f"The dealer has {self.dealer_hand[0]}.")
            self.dealer_hand.append(all_cards.pop(0))
            print(f"You have {sum(self.player_hand)}.")
            if sum(self.player_hand) == 21:
                print("Blackjack, you win!")
                active_hand = False
            elif sum(self.player_hand) > 21:
                print("Sorry, you went over 21 and have busted.")
                active_hand = False

            else:
                response = input("hit or stand? ")
                if response.lower() == "stand":
                    print(f"The dealer's score with the second card is {sum(self.dealer_hand)}")
                    if self.player_hand > self.dealer_hand:
                        print("Congrats, you win!")
                    elif self.player_hand == self.dealer_hand:
                        print("The scores are the same, it's a push (tie).")
                    else:
                        print("The dealer wins.")
                elif response.lower() == "hit":
                    self.player_hand.append(all_cards.pop(0))
                    print(f"You now have")

                    


                try:
                    response.lower() == "hit" or response.lower() == "stand"
                    if response.lower() == "hit":
                        self.player_hand.append(all_cards.pop(0))


                    elif response.lower() == "stand":
                        self.player_hand.append(all_cards.pop(0))
                        print


                except:
                    print("Sorry, that is not a valid command. Please enter 'hit' or 'stand'")        
                            

            # print(self.player_hand)




# if player gets 21 with first 2 cards, they win

# present value to player and allow them to stand or hit until busting over 21

# if player stands, show the second of the dealers cards (keep hidden until player selects stand)

# don't allow hit/stand for dealer, just compare with player unless player busts (keep in mind dealer CAN bust, (13 + 13) is over 21)




my_hand = Blackjack()

def run(Blackjack):
    Blackjack.deal()
    


run(my_hand)

