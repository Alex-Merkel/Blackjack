from flask import render_template, request, redirect, url_for
from app import app
# from . import Deck, Card, Player, Gambler, Dealer, Blackjack


@app.route('/start_game')
def start_game():
    # Start a new game (initialize the Blackjack game object)
    # Redirect back to the home route
    return redirect(url_for('home'))

@app.route('/hit', methods=['POST'])
def hit():
    # Handle player's "Hit" action
    # Add a card to the player's hand and update the game state
    # Redirect back to the home route
    return redirect(url_for('home'))

@app.route('/stand', methods=['POST'])
def stand():
    # Handle player's "Stand" action
    # Let the dealer play and determine the winner
    # Redirect back to the home route
    return redirect(url_for('home'))

@app.route('/restart_game')
def restart_game():
    # Reset the game and start a new round
    # Redirect back to the home route
    return redirect(url_for('home'))
