"""Message model tests."""

# run these tests like:
#
#    python -m unittest test_message_model.py


import os
from unittest import TestCase
from sqlalchemy import exc

from models import db, User, Message, Follows, Likes

# BEFORE we import our app, let's set an environmental variable
# to use a different database for tests (we need to do this
# before we import our app, since that will have already
# connected to the database

os.environ['DATABASE_URL'] = "postgresql:///warbler_test"


# Now we can import app

from app import app, CURR_USER_KEY

# Create our tables (we do this here, so we only create the tables
# once for all tests --- in each test, we'll delete the data
# and create fresh new clean test data

db.create_all()

app.config['WTF_CSRF_ENABLED'] = False

class MessageViewsTestCase(TestCase):
    """Test views for messages."""

    def setUp(self):
        """Create test client, add sample data."""

        db.drop_all()
        db.create_all()

        self.client = app.test_client()


        self.testuser = User.signup(username="testuser", email='testuser@test.com', password="testuser", image_url=None)

        self.testuser.id = 12345
        self.testuser.id = self.testuser.id

        self.u1 = User.signup('u1', 'test1@test.com', 'password', None)
        self.u1_id = 123
        self.u1.id = self.u1_id
        self.u2 = User.signup('u2', 'test2@test.com', 'password', None)
        self.u2_id = 456
        self.u2.id = self.u2_id
        self.u3 = User.signup('u3', 'test3@test.com', 'password', None)
        self.u3.id = 789
        self.u3.id = self.u3.id
        self.u4 = User.signup('u4', 'test4@test.com', 'password', None)

        db.session.commit()

    def tearDown(self):
        """Clean up fouled transactions."""

        db.session.rollback()
        return super().tearDown()

    def test_user_index(self):
        """Can we get user index page?"""

        with self.client as c:
            resp = c.get('/users')
            self.assertEqual(resp.status_code, 200)
            self.assertIn(b'<h1>All Users</h1>', resp.data)

    def test_users_search(self):
        """Can we search for users?"""

        with self.client as c:
            resp = c.get('/users?q=u1')
            self.assertEqual(resp.status_code, 200)
            self.assertIn(b'<h1>Search Results</h1>', resp.data)
            self.assertIn(b'<p>u1</p>', resp.data)
            self.assertNotIn(b'<p>u2</p>', resp.data)
            self.assertNotIn(b'<p>u3</p>', resp.data)
            self.assertNotIn(b'<p>u4</p>', resp.data)

    def setup_likes(self):
        """Setup likes for testing."""

        self.message = Message(text="Hello", user_id=self.testuser.id)
        db.session.add(self.message)
        db.session.commit()

        self.message_id = self.message.id

        self.like = Likes(message_id=self.message_id, user_id=self.testuser.id)
        db.session.add(self.like)
        db.session.commit()

        self.like_id = self.like.id
