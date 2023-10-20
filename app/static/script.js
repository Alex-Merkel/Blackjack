// const playerChipsElement = document.getElementById("player-chips");
let initialChips = 100;
// playerChipsElement.textContent = initialChips;
let initial_dealer_card = ''
// let dealerScore;
// let initial_dealer_hand_value = 0
// let player_score = 0





document.addEventListener("DOMContentLoaded", function() {
    const startGameModal = document.getElementById("startGameModal");
    const startGameButton = document.getElementById("start-game");
    const selectBetModal = document.getElementById("selectBetModal");
    const dealerScore = document.getElementById("dealer-score");
    const playerChipsElement = document.getElementById("player-chips");
    const playerChipsModalElement = document.getElementById("player-chips-modal");

    // Hide the selectBetModal initially
    selectBetModal.style.display = "none";

    // Hide the dealer-score initially
    dealerScore.style.display = "none";

    // Show the startGameModal when the page loads
    startGameModal.style.display = "block";

    // Set the initial number of chips when the page loads
    playerChipsElement.textContent = initialChips;
    playerChipsModalElement.textContent = initialChips; // Set initial chips in the modal

    // Handle the "Start Game" button click
    startGameButton.addEventListener("click", function() {
        // Close the startGameModal
        startGameModal.style.display = "none";

        // Show the betModal
        selectBetModal.style.display = "block";
    });

    // Handle the "Select Bet Amount" button click
    const selectBetButton = document.getElementById("select-bet");
    selectBetButton.addEventListener("click", function() {
        // Get the input value as a string
        const selectedBetString = document.getElementById("bet-amount").value;
        
        // Check if the input is a positive whole number
        if (/^\d+$/.test(selectedBetString)) {
            const selectedBet = parseInt(selectedBetString, 10);
            const playerChips = parseInt(playerChipsElement.textContent);
            
            if (selectedBet > 0 && selectedBet <= playerChips) {
                // Close the selectBetModal
                selectBetModal.style.display = "none";

                // Update the displayed chips value in the HTML
                playerChipsElement.textContent = playerChips - selectedBet;
                playerChipsModalElement.textContent = playerChips - selectedBet; // Update chips in the modal

                // Update the JavaScript variable
                initialChips -= selectedBet;

                // Initialize the game (deal cards, show scores, etc.)
                initializeGame();
            } else if (selectedBet > playerChips) {
                alert('You cannot bet more chips than you have.');
            } else {
                alert('Must enter a positive whole number.');
            }
        } else {
            alert('Please enter a valid whole number.');
        }
    });

    // Add more game initialization and logic functions
});




// Initialize Game function
function initializeGame() {
    fetch('/start_game')
        .then(response => response.json())
        .then(data => {
            initial_dealer_card = data.dealer_cards[0]
            player_score = data.player_score
            dealer_score = data.dealer_score
            console.log(dealer_score)
            console.log(initial_dealer_card)
            // Create an image element for the face-down card
            const faceDownCardImage = document.createElement("img");
            faceDownCardImage.src = 'static/img/card_back.png';
            faceDownCardImage.setAttribute('id', 'faceDownImage');
            // Append it to the dealer's card container in your HTML
            document.getElementById("dealer-hand").appendChild(faceDownCardImage);

            // Process the game data returned by the server
            data.player_cards.forEach(card => {
                // Create an image element for the player's card
                const playerCardImage = document.createElement("img");
                playerCardImage.src = cardToImagePath(card);
                // Append it to the player's card container in your HTML
                document.getElementById("player-hand").appendChild(playerCardImage);
            });

            data.dealer_cards.forEach((card, index) => {
                // Skip the first card when appending dealer cards
                if (index === 0) {
                    return;
                }

                // Create an image element for the dealer's card
                const dealerCardImage = document.createElement("img");
                dealerCardImage.src = cardToImagePath(card);
                // Append it to the dealer's card container in your HTML
                document.getElementById("dealer-hand").appendChild(dealerCardImage);
            });

            document.getElementById("player-score").textContent = `Player Score: ${data.player_score}`;
            document.getElementById("dealer-score").textContent = `Dealer Score: ${data.dealer_score}`;
        })
        .catch(error => {
            console.error('Error starting the game:', error);
        });
}





function cardToImagePath(card) {
    const [value, suit] = card.split(' of ');
    return `static/img/${value.toLowerCase()}_of_${suit.toLowerCase()}.png`;
}

// Hit button, event listener:
const hitButton = document.getElementById("hit");
hitButton.addEventListener("click", () => {
    fetch('/hit', { method: 'POST' })
        .then(response => response.json())
        .then(data => {
            // Process the new card data
            const newCardImage = document.createElement("img");
            console.log(data.player_cards[data.player_cards.length - 1])
            newCardImage.src = cardToImagePath(data.player_cards[data.player_cards.length - 1]);

            // Append it to the player's card container in your HTML
            document.getElementById("player-hand").appendChild(newCardImage);

            // Update the player's score
            document.getElementById("player-score").textContent = `Player Score: ${data.player_score}`;
            
            if (data.player_score > 21) {
                // Player has busted - show the "End Game Modal" with the "You've busted, you lose" message
                const endGameModal = document.getElementById("endGameModal");
                endGameModal.style.display = "block";
                
                // Set the text in the endGameHeader to "You've busted, you lose"
                const endGameHeader = document.getElementById("endGameHeader");
                endGameHeader.textContent = "You've busted with " + data.player_score;
            } else {
                // player_score = data.player_score
            }
        })
        .catch(error => {
            console.error('Error handling hit:', error);
        });
});






function revealDealerCard(initial_dealer_card) {
    // Get the face-down card image
    const faceDownCardImage = document.getElementById("faceDownImage")

    // Set the src attribute to the actual card's image
    faceDownCardImage.src = cardToImagePath(initial_dealer_card);
}




const standButton = document.getElementById("stand");
standButton.addEventListener("click", () => {
    // Disable hit / stand buttons
    hitButton.disabled = true;
    standButton.disabled = true;

    // Reveal the dealer's face-down card
    revealDealerCard(initial_dealer_card);

    const dealerScore = document.getElementById("dealer-score");

    // Show the dealer score
    dealerScore.style.display = "block";

    // Update the player and dealer scores

    // Recursive function for dealer hits
    function dealerHit(data, index) {
        if (index >= 2 && index < data.dealer_cards.length) {
            // Add a delay between hits
            setTimeout(() => {
                const card = data.dealer_cards[index];
                const newCardImage = document.createElement("img");
                newCardImage.src = cardToImagePath(card);
                document.getElementById("dealer-hand").appendChild(newCardImage);

                // Update the dealer's score in the DOM
                document.getElementById("dealer-score").textContent = `Dealer Score: ${data.dealer_score}`;
                
                // Continue with the next hit
                dealerHit(data, index + 1);
            }, 1000); // 1000 milliseconds (1 second) delay
        } else {
            // All hits are done
            // Handle the game logic for the dealer, e.g., checking for a winner
            // handleDealerActions();
        }
    }

    fetch('/stand', { method: 'POST' })
        .then(response => response.json())
        .then(data => {
            // Start the recursive dealerHit function
            dealerHit(data, 2);
        })
        .catch(error => {
            console.error('Error handling stand:', error);
        });
});





const playAgainButton = document.getElementById("play-again");
playAgainButton.addEventListener("click", () => {
    // Re-enable the hit and stand buttons
    hitButton.disabled = false;
    standButton.disabled = false;
    
    // Remove all images from the dealer and player hands
    document.getElementById("dealer-hand").innerHTML = "";
    document.getElementById("player-hand").innerHTML = "";

    // Update the player and dealer scores
    document.getElementById("player-score").textContent = "Player Score: 0";
    document.getElementById("dealer-score").textContent = "Dealer Score: 0";

    // Close end Game Modal
    endGameModal.style.display = "none"
    // Open up select Bet Modal
    selectBetModal.style.display = "block"

    // Reset the game on the server side
    fetch('/play_again')
        .then(response => response.text())
        .then(data => {
            console.log(data, 'water')
        })
        .catch(error => {
            console.error('Error restarting the game:', error);
        });
});
