from unittest import TestCase
from app import app
from flask import session

class FlaskTests(TestCase):
    """Tests for Flask Boggle app."""

    def setUp(self):
        """Set up test client and configure app for testing."""
        self.client = app.test_client()
        app.config['TESTING'] = True
        app.config['SECRET_KEY'] = 'test_secret_key'

    def tearDown(self):
        """Clean up after each test."""
        with self.client as client:
            with client.session_transaction() as sess:
                sess.clear()  # Clear session data


    def test_homepage(self):
        """Test if the homepage loads correctly and intializes the game board."""
        with self.client as client:
            response = client.get('/') # Send a GET request to the homepage
            self.assertEqual(response.status_code, 200) # Check the status code
            self.assertIn(b'<table>', response.data) #Ensure the obard is in the HTML response
            self.assertIn('board', session) # Check if the board is in the session

    def test_valid_word(self):
        """Test the /guess route for a valid word."""
        with self.client as client:
            with client.session_transaction() as sess:
                # Set up a test board
                 sess['board'] = [["C", "A", "T", "D", "O"],
                             ["P", "L", "A", "Y", "E"],
                             ["R", "S", "G", "I", "T"],
                             ["H", "U", "N", "K", "F"],
                             ["B", "O", "A", "R", "D"]]
                 
            # Post a valid word
            response = client.post('/guess', json={'guess':'cat'})
            self.assertEqual(response.status_code, 200) #Check the status code
            self.assertEqual(response.json['result'], 'ok') # Check the response

    def test_invalid_word(self):
        """Test the /guess route for an invalid word."""
        with self.client as client:
            with client.session_transaction() as sess:
                # Set up a test board
                sess['board'] = [["B", "Z", "T", "Y", "O"],
                             ["P", "V", "A", "Y", "E"],
                             ["J", "S", "G", "I", "W"],
                             ["H", "U", "U", "X", "F"],
                             ["B", "R", "A", "R", "D"]]
            
            response = client.post('/guess', json={'guess': 'xyz'})
            self.assertEqual(response.status_code, 200)
            self.assertEqual(response.json['result'], 'not-a-word')

    def test_game_over(self):
        """Test the /game-over route for updating the session with score and plays."""
        with self.client as client:
            with client.session_transaction() as sess:
                sess['highest_score'] = 10
                sess['num_plays'] = 2

        response = client.post('/game-over', json={'score': 15})
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.json['highest_score'], 15)
        self.assertEqual(response.json['num_plays'], 3)
                                   