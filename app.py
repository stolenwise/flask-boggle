from boggle import Boggle
from flask import Flask, request, render_template, jsonify, session
import pdb

with open("words.txt") as f:  # Load a dictionary of words
    words = set(word.strip().lower() for word in f)

boggle_game = Boggle()

app = Flask(__name__)   # Create an instance of the Flask class
app.config['SECRET_KEY'] = 'secret key'

if __name__ == "__main__":
    app.run(debug=True)

@app.before_request
def initialize_session():
    if "num_plays" not in session:
        session["num_plays"] = 0
    if "highest_score" not in session:
        session["highest_score"] = 0

@app.route("/")
def homepage():
    """Render the homepage and initialize a new game."""
    if "board" not in session:  # Only create a new board if it doesn't exist
        board = boggle_game.make_board()
        session["board"] = board
    return render_template("index.html", board=session["board"])

    return render_template('index.html', board=board, highscore=highscore, nplays=nplays)

@app.route("/guess", methods=["POST"])
def guess():
    """
    Check if the guessed word is valid.
    Validates the guess against the board and the dictionary.
    Returns a JSON response with the result.
    """
    try:
        # Get the guessed word from the request
        word = request.json.get("guess").lower()  # Normalize the guess to lowercase

        # Retrieve the board from the session
        board = session.get("board")
        if not board:
            return jsonify({"result": "error"}), 400  # Error if board is missing from the session

        # Debugging output
        print("Board:", board)
        print("Guess:", word)

        # Check if the word is valid in the dictionary
        if word not in boggle_game.words:
            print("Word is not in dictionary.")
            return jsonify({"result": "not-a-word"})

        # Check if the word is valid on the board
        board_result = boggle_game.check_valid_word(board, word)
        print("Board result:", board_result)

        if board_result == "ok":
            return jsonify({"result": "ok"})
        elif board_result == "not-on-board":
            return jsonify({"result": "not-on-board"})
        else:
            return jsonify({"result": "error"})
    except Exception as e:
        # Log any exceptions
        print("Error:", str(e))
        return jsonify({"result": "error"}), 500


@app.route('/game-over', methods=['POST'])
def game_over():
    try:
        # Debug: Log incoming data
        print("Incoming data:", request.json)

        # Get the score from the request JSON
        data = request.json
        current_score = data.get("score", 0)

        # Debug: Log session variables before updating
        print("Session before:", session)

        # Update the number of games played
        session["num_plays"] += 1

        # Update the highest score if the current score is higher
        if current_score > session["highest_score"]:
            session["highest_score"] = current_score

        # Debug: Log session variables after updating
        print("Session after:", session)

        # Return updated stats to the front-end
        return jsonify(
            highest_score=session["highest_score"],
            num_plays=session["num_plays"]
        )

    except Exception as e:
        # Debug: Log any errors
        print("Error in /game-over route:", e)
        return jsonify({"error": str(e)}), 500
    
@app.route("/restart", methods=["POST"])
def restart():
    """Clear the session to start a new game."""
    session.clear()
    return "Session cleared", 200