const playerChipsElement = document.getElementById("player-chips");
let initialChips = 100;

playerChipsElement.textContent = initialChips;



document.addEventListener("DOMContentLoaded", function() {
    const startGameModal = document.getElementById("startGameModal");
    const startGameButton = document.getElementById("start-game");
    const selectBetModal = document.getElementById("selectBetModal");

    // Hide the selectBetModal initially
    selectBetModal.style.display = "none";

    // Show the startGameModal when the page loads
    startGameModal.style.display = "block";

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

                // Update the JavaScript variable
                initialChips -= selectedBet;

                // Initialize the game (deal cards, show scores, etc.)
                initializeGame();
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
            console.log(data, 'potato')
            // Process the game data returned by the server
            data.player_cards.forEach(card => {
                // Create an image element for the player's card
                const playerCardImage = document.createElement("img");
                playerCardImage.src = cardToImagePath(card);
                console.log(playerCardImage)
                // Append it to the player's card container in your HTML
                document.getElementById("player-hand").appendChild(playerCardImage);
            });

            data.dealer_cards.forEach(card => {
                // Create an image element for the dealer's card
                const dealerCardImage = document.createElement("img");
                dealerCardImage.src = cardToImagePath(card);
                // Append it to the dealer's card container in your HTML
                document.getElementById("dealer-hand").appendChild(dealerCardImage);
            });
        })
        .catch(error => {
            console.error('Error starting the game:', error);
        });
}




function cardToImagePath(card) {
    const [value, suit] = card.split(' of ');
    return `static/img/${value.toLowerCase()}_of_${suit.toLowerCase()}.png`;
}


// event listener for stand:
const standButton = document.getElementById("stand");
standButton.addEventListener("click", () => {
    // Replace the face-down card with the actual dealer's first card
    revealDealerCard(initialDealerCard);
    // Other logic for the dealer's turn
});