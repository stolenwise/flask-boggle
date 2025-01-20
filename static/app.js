class BoggleGame {
    constructor(timerDuration = 60) {
        // Initialize state
        this.score = 0;
        this.guessedWords = new Set(); // Track guessed words to prevent duplicates
        this.timeRemaining = timerDuration;
        this.timerInterval = null;

        this.updateScore();
        $("#timer").text(this.timeRemaining);

        // Event listeners for user actions
        $("#guess-form").on("submit", this.handleGuess.bind(this));
        $("#restart-button").on("click", this.restartGame.bind(this));

        // Start the game timer
        this.startTimer();
    }

    // Method: Update the score on the page
    updateScore() {
        $("#score").text(this.score);
    }

    // Method: Start the timer
    startTimer() {
        console.log("Timer started");
        this.timerInterval = setInterval(() => {
            if (this.timeRemaining > 0) {
                this.timeRemaining -= 1;
                $("#timer").text(this.timeRemaining);
            } else {
                clearInterval(this.timerInterval);
                this.endGame();
            }
        }, 1000);
    }

    // Method: Handle a word guess
    handleGuess(event) {
        event.preventDefault(); // Prevent the form from refreshing the page
        const guess = $("#guess").val().trim();

        // Check for duplicate guesses
        if (this.guessedWords.has(guess)) {
            $("#result").text(`❌ "${guess}" has already been guessed.`);
            $("#guess").val("");
            return;
        }

        // Send the guess to the server
        axios.post("/guess", { guess: guess })
            .then((response) => {
                const result = response.data.result;

                if (result === "ok") {
                    this.score += guess.length; // Increase score
                    this.guessedWords.add(guess); // Add the word to the set
                    this.updateScore();
                    $("#result").text(`✅ "${guess}" is valid! +${guess.length} points.`);
                } else if (result === "not-on-board") {
                    $("#result").text("❌ That word is not on the board.");
                } else if (result === "not-a-word") {
                    $("#result").text("❌ That is not a valid word in the dictionary.");
                }
            })
            .catch((error) => {
                console.error("Error submitting guess:", error);
                $("#result").text("❌ An error occurred while submitting your guess.");
            });

        // Clear the input field
        $("#guess").val("");
    }

    // Method: End the game when the timer runs out
    endGame() {
        $("#guess").prop("disabled", true); // Disable the input field
        $("#submit-button").prop("disabled", true); // Disable the submit button
        $("#result").text("⏰ Time is up!");

        // Send the score to the server
        axios.post("/game-over", { score: this.score })
            .then((response) => {
                const data = response.data;
                $("#highest-score").text(data.highest_score);
                $("#num-plays").text(data.num_plays);
            })
            .catch((error) => {
                console.error("Error sending game data:", error);
            });
    }

    // Method: Restart the game
    restartGame() {
        axios.post("/restart") // Add a route to clear the session
            .then(() => {
                location.reload(); // Reload the page
            })
            .catch((error) => {
                console.error("Error restarting game:", error);
            });
    }
}

// Instantiate the game when the page loads
$(document).ready(() => {
    new BoggleGame(60);
});


