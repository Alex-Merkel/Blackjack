from flask import render_template, request, redirect, url_for, jsonify
from app import app
from app.game_logic import Blackjack

# Initialize the game object
game = Blackjack()

@app.route('/')
def home():
    return render_template('game.html')

@app.route('/start_game')
def start_game():
    game.initiate_game()
    player_score = game.players[0].score_aces
    dealer_score = game.players[1].score_aces
    game_state = game.get_game_state(player_score, dealer_score)
    return jsonify(game_state)

@app.route('/hit', methods=['POST'])
def hit():
    player = game.players[0]
    game.hit(player)
    player_score = game.players[0].score_aces
    dealer_score = game.players[1].score_aces
    game_state = game.get_game_state(player_score, dealer_score)
    return jsonify(game_state)

@app.route('/stand', methods=['POST'])
def stand():
    game.stand()
    player_score = game.players[0].score_aces
    dealer_score = game.players[1].score_aces
    game_state = game.get_game_state(player_score, dealer_score)
    return jsonify(game_state)

@app.route('/play_again')
def play_again():
    game.play_again()
    player_score = game.players[0].score_aces
    dealer_score = game.players[1].score_aces
    game_state = game.get_game_state(player_score, dealer_score)  
    return jsonify(game_state)


# Make function for player_score, dealer_score, game_state since used in all routes above!!!???
# Add below route
# @app.route('/restart / reset')
