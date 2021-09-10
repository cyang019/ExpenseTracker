import sys
import os
import unittest
import json
from flask_sqlalchemy import SQLAlchemy
sys.path.insert(
  0,
  os.path.dirname(os.path.dirname(__file__))
  )
from application.app import create_app, setup_db
from models import db


class ExpenseTrackerTestCase(unittest.TestCase):
  """Testing backend apis for expense tracker.
  """
  def setUp(self):
    self.app = create_app("testing")
    self.client = self.app.test_client
    # binds the app to the current context
    with self.app.app_context():
      db.create_all()
  
  def tearDown(self):
    pass

  def test_get_transactions(self):
    res = self.client().get('/transactions')
    data = json.loads(res.data)
    self.assertEqual(res.status_code, 200)
    self.assertEqual(data['success'], True)

  def test_post_transaction(self):
    res = self.client().post(
      'transactions',
      json={
        "amount": 100
      }
    )
    data = json.loads(res.data)
    self.assertEqual(res.status_code, 422)
    self.assertEqual(data['success'], False)
  