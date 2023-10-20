# class Gambler(Player):
#     def __init__(self, chips):
#         super().__init__()
#         self.chips = chips

    # def bet(self):
    #     stake = input(f"Total chips: {self.chips}. Enter your bet amount: ")
    #     try:
    #         if int(stake) > self.chips:
    #             print("You cannot bet more than you have")
    #             self.bet()
    #         else:
    #             self.chips -= int(stake)
    #             return int(stake)
    #     except ValueError:
    #         print('Please enter a valid integer.')
    #         self.bet()

            # if self.players[0].chips == 0:
            #     print("You've run out of chips")
            #     break

# def get_game_state(self, player_score, dealer_score):
#         player_info = [str(card) for card in self.players[0].hand]
#         dealer_info = [str(card) for card in self.players[1].hand]
#         game_state = {
#             'player_cards': player_info,
#             'dealer_cards': dealer_info,
#             'player_score': player_score,
#             'dealer_score': dealer_score,
#         }
#         return game_state





# Bottom:
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

# def main():
#     game = Blackjack()
#     game.play()



    # NEED TO ADJUST  - BLACKJACK Class
#     def player_choice(self, player):
#         print('delete this!!')
#         answer = input("Hit or Stand? (H/S): ")
#         if answer.lower() == "h":
#             self.hit(player)
#         if answer.lower() == "s":
#             self.players_turn = False
#             Dealer.hand[1] = initialDealerCard
#             dealer_score = Dealer.score_aces  
#             game_state = self.get_game_state(player.score_aces, dealer_score)
#             return game_state



#    PLAYER Class:    
    # def getHand(self):
    #     print("\t\t\tThe player's hand:")
    #     for card in (self.hand):
    #         print(card)
    #         print("")
    #     print("")

    # def get_hand_info(self):
    #     # Create a list of dictionaries with card information
    #     hand_info = [{'suit': card.suit, 'value': card.value} for card in self.hand]
    #     return hand_info