import sys
import os
import unittest
import json
import datetime
from flask_sqlalchemy import SQLAlchemy
sys.path.insert(
  0,
  os.path.dirname(os.path.dirname(__file__))
  )
from application.app import create_app, setup_db
from application.models import db


class ExpenseTrackerTestCase(unittest.TestCase):
  """Testing backend apis for expense tracker.
  """
  def setUp(self):
    self.app = create_app()
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
    self.assertTrue(len(data['transactions']) > 0)

  def test_post_transaction(self):
    res = self.client().post(
      'transactions',
      json={
        "card_id": 1,
        "category_id": 2,
        "amount": 1000,
        "currency_id": 1,
        "time": "1/1/21 12:00:00.0",
        "description": "buy stuff",
        "receipt_no": "12345"
      }
    )
    data = json.loads(res.data)
    self.assertEqual(res.status_code, 200)
    self.assertEqual(data['success'], True)
  