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

from app import app

# Create our tables (we do this here, so we only create the tables
# once for all tests --- in each test, we'll delete the data
# and create fresh new clean test data

db.create_all()

class UserModelTestCase(TestCase):
    """Test views for messages."""

    def setUp(self):
        """Create test client, add sample data."""

        db.drop_all()
        db.create_all()

        self.uid = 12345
        user = User.signup(username="testuser", email='testuser@test.com', password="testuser", image_url=None)
        user.id = self.uid
        db.session.commit()

        self.user = User.query.get(self.uid)

        self.client = app.test_client()

    def tearDown(self):
        """Clean up fouled transactions"""
        db.session.rollback()
        return super().tearDown()

    def test_message_model(self):
      '''Test messages model'''
      message = Message(text="Hello", user_id=self.uid)
      db.session.add(message)
      db.session.commit()

      self.assertEqual(message.text, "Hello")
      self.assertEqual(message.user_id, self.uid)

    def test_message_likes(self):
      '''Test messages likes'''
      message = Message(text="Hello", user_id=self.uid)
      db.session.add(message)
      db.session.commit()

      message_id = message.id

      like = Likes(message_id=message_id, user_id=self.uid)
      db.session.add(like)
      db.session.commit()

      self.assertEqual(like.message_id, message_id)
      self.assertEqual(like.user_id, self.uid)

