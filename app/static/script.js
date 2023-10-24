let playerChips = 100;
let initial_dealer_card = ''
let initial_dealer_score = 0
let selectedBet = 0


document.addEventListener("DOMContentLoaded", function() {
    const startGameModal = document.getElementById("startGameModal");
    const startGameButton = document.getElementById("start-game");
    const selectBetModal = document.getElementById("selectBetModal");
    const playerChipsElement = document.getElementById("player-chips");
    const playerChipsModalElement = document.getElementById("player-chips-modal");

    // Hide the selectBetModal initially
    selectBetModal.style.display = "none";

    // Show the startGameModal when the page loads
    startGameModal.style.display = "block";

    // Set the initial number of chips when the page loads
    playerChipsElement.textContent = playerChips;
    playerChipsModalElement.textContent = playerChips;

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
            selectedBet = parseInt(selectedBetString, 10);
            
            if (selectedBet > 0 && selectedBet <= playerChips) {
                // Close the selectBetModal
                selectBetModal.style.display = "none";

                // Update playerChips and display value in the HTML
                playerChips = playerChips - selectedBet;
                playerChipsElement.textContent = playerChips;
                playerChipsModalElement.textContent = playerChips;


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
});




// Initialize Game function
function initializeGame() {
    fetch('/start_game')
        .then(response => response.json())
        .then(data => {
            // Save face down card and initial total dealer score
            initial_dealer_card = data.dealer_cards[0]
            initial_dealer_score = data.initial_dealer_score

            // Create an image element for the face-down card
            const faceDownCardImage = document.createElement("img");
            faceDownCardImage.src = 'static/img/card_back.png';
            faceDownCardImage.setAttribute('id', 'faceDownImage');

            document.getElementById("dealer-hand").appendChild(faceDownCardImage);

            // Process the game data returned by the server
            data.player_cards.forEach(card => {
                // Create an image element for the player's card
                const playerCardImage = document.createElement("img");
                playerCardImage.src = cardToImagePath(card);

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

                document.getElementById("dealer-hand").appendChild(dealerCardImage);
            });

            document.getElementById("player-score").textContent = `Player Score: ${data.player_score}`;
            document.getElementById("dealer-score").textContent = `Dealer Score: ${data.dealer_score}`;
        })
        .catch(error => {
            console.error('Error starting the game:', error);
        });
}




// Take data from backend and convert to image path for frontend to get card images
function cardToImagePath(card) {
    let [value, suit] = card.split(' of ');
    
    // Check if the value is '1' and replace it with 'ace'
    if (value === '1') {
        value = 'ace';
    }

    return `static/img/${value.toLowerCase()}_of_${suit.toLowerCase()}.png`;
}


// Hit button, event listener
const hitButton = document.getElementById("hit");
hitButton.addEventListener("click", () => {
    fetch('/hit', { method: 'POST' })
        .then(response => response.json())
        .then(data => {
            // Process the new card data
            const newCardImage = document.createElement("img");
            newCardImage.src = cardToImagePath(data.player_cards[data.player_cards.length - 1]);

            document.getElementById("player-hand").appendChild(newCardImage);

            // Update the player's score
            document.getElementById("player-score").textContent = `Player Score: ${data.player_score}`;
            
            if (data.player_score > 21) {
                // Player has busted - show the "End Game Modal" with the "You've busted" message
                const endGameModal = document.getElementById("endGameModal");
                endGameModal.style.display = "block";
                
                // Set the text in the endGameHeader to "You've busted"
                const endGameHeader = document.getElementById("endGameHeader");
                endGameHeader.textContent = "You've busted with " + data.player_score;
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
    dealerScore.textContent = `Dealer Score: ${initial_dealer_score}`;

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
                dealerScore.textContent = `Dealer Score: ${data.dealer_score}`;

                // Continue with the next hit
                dealerHit(data, index + 1);
            }, 1000);

            // Update the dealer's score with a delay
            setTimeout(() => {
                dealerScore.textContent = `Dealer Score: ${data.dealer_score}`;
            }, (index - 1) * 1000);
        } else {
            // Once all hitting is done, handle the game logic for the dealer
            setTimeout(() => {
                handleCompare(data);
            }, 2000); 
        }
    }

    fetch('/stand', { method: 'POST' })
        .then(response => response.json())
        .then(data => {
            // Start the dealerHit function
            dealerHit(data, 2);
        })
        .catch(error => {
            console.error('Error handling stand:', error);
        });

    // Function to handle dealer actions and display the modal
    function handleCompare(data) {
        // Check the outcome and display the appropriate modal and message
        const outcome = data.outcome;
        const endGameModal = document.getElementById("endGameModal");
        const endGameHeader = document.getElementById("endGameHeader");
        const endGameScore = document.getElementById("endGameScore");
        const playerChipsModalElement = document.getElementById("player-chips-modal");

        if (outcome === "Dealer busts, you win!!") {
            endGameHeader.textContent = `Dealer busts, you win!! Here are your ${2 * selectedBet} chips!`;
            endGameScore.textContent = `Dealer Score: ${data.dealer_score} Player Score: ${data.player_score}`;
            // Update the player's chips when they win
            playerChips = playerChips + (2 * selectedBet)
            playerChipsModalElement.textContent = playerChips;
        } else if (outcome === "You win!!") {
            endGameHeader.textContent = `You win!! Here are your ${2 * selectedBet} chips!`;
            endGameScore.textContent = `Dealer Score: ${data.dealer_score} Player Score: ${data.player_score}`;
            // Update the player's chips when they win
            playerChips = playerChips + (2 * selectedBet)
            playerChipsModalElement.textContent = playerChips;
        } else if (outcome === "Dealer wins") {
            endGameHeader.textContent = "Dealer wins";
            endGameScore.textContent = `Dealer Score: ${data.dealer_score} Player Score: ${data.player_score}`;
        } else {
            endGameHeader.textContent = `It's a tie, here are your ${selectedBet} chips back.`;
            endGameScore.textContent = `Dealer Score: ${data.dealer_score} Player Score: ${data.player_score}`;
            // Return the bet to the player in case of a draw (push)
            playerChips = playerChips + selectedBet
            playerChipsModalElement.textContent = playerChips;
        }

        // Show the end game modal
        endGameModal.style.display = "block";
    }
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
});


