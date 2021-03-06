import unittest

from party import app
from model import db, example_data, connect_to_db, Game


class PartyTests(unittest.TestCase):
    """Tests for my party site."""

    def setUp(self):
        self.client = app.test_client()
        app.config['TESTING'] = True      

    def test_homepage(self):
        result = self.client.get("/")
        self.assertIn("board games, rainbows, and ice cream sundaes", result.data)

    def test_no_rsvp_yet(self):
        # FIXME: Add a test to show we see the RSVP form, but NOT the
        # party details
        result = self.client.get("/")
        self.assertIn("Please RSVP", result.data)
        self.assertNotIn("123 Magic Unicorn Way", result.data)

    def test_rsvp(self):
        result = self.client.post("/rsvp",
                                  data={"name": "Jane",
                                        "email": "jane@jane.com"},
                                  follow_redirects=True)
        # Once we RSVP, we should see the party details, but
        # not the RSVP form
        self.assertNotIn("Please RSVP", result.data)
        self.assertIn("123 Magic Unicorn Way", result.data)

class PartyTestsDatabase(unittest.TestCase):
    """Flask tests that use the database."""

    def setUp(self):
        """Stuff to do before every test."""

        self.client = app.test_client()
        app.config['TESTING'] = True

        # Connect to test database (uncomment when testing database)
        connect_to_db(app, "postgresql:///testdb")

        # Create tables and add sample data (uncomment when testing database)
        db.create_all()
        example_data()

        # setting a session
        with self.client as c:
            with c.session_transaction() as sess:
                sess['RSVP'] = True

    def tearDown(self):
        """Do at end of every test."""

        db.session.close()
        db.drop_all()

    def test_games(self):
        #FIXME: test that the games page displays the game from example_data()
        result = self.client.get("/games")

        self.assertNotIn("Please RSVP", result.data)
        self.assertNotIn("Amazing Labyrinth", result.data)
        self.assertNotIn("123 Magic Unicorn Way", result.data)
        self.assertIn("Anomia", result.data)
        self.assertIn("Pictionary", result.data)
        self.assertIn("Taboo", result.data)

        all_games = db.session.query(Game.name).all()
        print all_games


if __name__ == "__main__":
    unittest.main()
