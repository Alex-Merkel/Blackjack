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
    game.play()
    game_state = game.get_game_state()
    print(game_state)
    return jsonify(game_state)

@app.route('/hit', methods=['POST'])
def hit():
    game.hit_player()  # Call a method in the game logic to handle player hitting
    return redirect(url_for('home'))

@app.route('/stand', methods=['POST'])
def stand():
    game.stand_player()  # Call a method in the game logic to handle player standing
    return redirect(url_for('home'))

@app.route('/restart_game')
def restart_game():
    game.reset()  # Reset the game using the game object
    return redirect(url_for('home'))
