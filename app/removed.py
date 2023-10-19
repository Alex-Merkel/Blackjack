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