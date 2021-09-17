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
from application.app import setup_db, app
from application.models import db


# JWT_SECRET = os.getenv('JWT_SECRET')


class ExpenseTrackerTestCase(unittest.TestCase):
  """Testing backend apis for expense tracker.
  """
  def setUp(self):
    self.app = app
    self.client = self.app.test_client
    self.user_token = os.getenv('TOKEN')
    # binds the app to the current context
    with self.app.app_context():
      db.create_all()
  
  def tearDown(self):
    pass

  def test_get_transactions(self):
    res = self.client().get(
      '/transactions',
      headers={
        'Authorization': f'Bearer {self.user_token}'
      })
    data = json.loads(res.data)
    self.assertEqual(res.status_code, 200)
    self.assertEqual(data['success'], True)
    self.assertTrue(len(data['transactions']) > 0)

  def test_get_single_transaction(self):
    res = self.client().get(
      '/transactions/1',
      headers={
        'Authorization': f'Bearer {self.user_token}'
      })
    data = json.loads(res.data)
    self.assertEqual(res.status_code, 200)
    self.assertEqual(data['success'], True)
    self.assertTrue(data['transaction']['amount'])

  def test_get_single_transaction_error(self):
    res = self.client().get(
      'transactions/123456',
      headers={
        'Authorization': f'Bearer {self.user_token}'
      })
    data = json.loads(res.data)
    self.assertEqual(res.status_code, 404)
    self.assertEqual(data['success'], False)

  def test_post_transaction(self):
    res = self.client().post(
      '/transactions',
      json={
        "card_id": 1,
        "category_id": 2,
        "amount": 1000,
        "currency_id": 1,
        "time": "1/1/21 12:00:00.0",
        "description": "buy stuff",
        "receipt_no": "12345"
      },
      headers={
        'Authorization': f'Bearer {self.user_token}'
      }
    )
    data = json.loads(res.data)
    self.assertEqual(res.status_code, 200)
    self.assertEqual(data['success'], True)

  def test_post_transaction_error(self):
    res = self.client().post(
      '/transactions',
      json={
        'card_id': 1,
        'category_id': 2
      },
      headers={
        'Authorization': f'Bearer {self.user_token}'
      })
    data = json.loads(res.data)
    self.assertEqual(res.status_code, 422)
    self.assertEqual(data['success'], False)

  def test_patch_transaction(self):
    res = self.client().patch(
      '/transactions/1',
      json={
        "card_id": 1,
        "category_id": 2,
        "amount": 1000,
        "currency_id": 1,
        "time": "01/01/21 12:00:00.0",
        "description": "buy stuff",
        "receipt_no": "12345"
      },
      headers={
        'Authorization': f'Bearer {self.user_token}'
      }
    )
    data = json.loads(res.data)
    self.assertEqual(res.status_code, 200)
    self.assertEqual(data['success'], True)

  def test_delete_transaction(self):
    res = self.client().delete(
      '/transactions/3',
      headers={
        'Authorization': f'Bearer {self.user_token}'
      })
    data = json.loads(res.data)
    self.assertEqual(res.status_code, 200)
    self.assertEqual(data['deleted'], 3)

  def test_get_cards(self):
    res = self.client().get(
      '/cards',
      headers={
        'Authorization': f'Bearer {self.user_token}'
      })
    data = json.loads(res.data)
    self.assertEqual(res.status_code, 200)
    self.assertGreater(len(data['cards']), 0)

  def test_get_card(self):
    res = self.client().get(
      '/cards/1',
      headers={
        'Authorization': f'Bearer {self.user_token}'
      })
    data = json.loads(res.data)
    self.assertEqual(res.status_code, 200)
    self.assertTrue(data['card']['number'])
  
  def test_post_card(self):
    res = self.client().post(
      '/cards',
      json={
        'user_id': 1,
        'number': '1234567901234',
        'code': '000',
        'expire': '12/23',
        'processor': 'mastercard'
      },
      headers={
        'Authorization': f'Bearer {self.user_token}'
      }
    )
    data = json.loads(res.data)
    self.assertEqual(res.status_code, 200)
    self.assertEqual(data['success'], True)

  def test_delete_card(self):
    res = self.client().delete(
      '/cards/4',
      headers={
        'Authorization': f'Bearer {self.user_token}'
      })
    data = json.loads(res.data)
    self.assertEqual(res.status_code, 200)
    self.assertEqual(data['success'], True)

  def test_get_categories(self):
    res = self.client().get(
      '/categories',
      headers={
        'Authorization': f'Bearer {self.user_token}'
      })
    data = json.loads(res.data)
    self.assertEqual(res.status_code, 200)
    self.assertGreater(len(data['categories']), 0)

  def test_get_category(self):
    res = self.client().get(
      '/categories/2',
      headers={
        'Authorization': f'Bearer {self.user_token}'
      })
    data = json.loads(res.data)
    self.assertEqual(res.status_code, 200)
    self.assertTrue(data['category']['name'])

  def test_delete_category(self):
    res = self.client().delete(
      '/categories/1',
      headers={
        'Authorization': f'Bearer {self.user_token}'
      })
    data = json.loads(res.data)
    self.assertEqual(res.status_code, 200)
    self.assertEqual(data['success'], True)

  def test_post_category(self):
    res = self.client().post(
      '/categories',
      json={
        "name": "dummy"
      },
      headers={
        'Authorization': f'Bearer {self.user_token}'
      }
    )
    data = json.loads(res.data)
    self.assertEqual(res.status_code, 200)
    self.assertEqual(data['success'], True)

  def test_get_currencies(self):
    res = self.client().get(
      '/currencies',
      headers={
        'Authorization': f'Bearer {self.user_token}'
      })
    data = json.loads(res.data)
    self.assertEqual(res.status_code, 200)
    self.assertGreater(len(data['currencies']), 0)

  def test_get_currency(self):
    res = self.client().get(
      '/currencies/2',
      headers={
        'Authorization': f'Bearer {self.user_token}'
      })
    data = json.loads(res.data)
    self.assertEqual(res.status_code, 200)
    self.assertTrue(data['currency']['name'])

  def test_delete_currency(self):
    res = self.client().delete(
      '/currencies/3',
      headers={
        'Authorization': f'Bearer {self.user_token}'
      })
    data = json.loads(res.data)
    self.assertEqual(res.status_code, 200)
    self.assertEqual(data['success'], True)

  def test_post_currency(self):
    res = self.client().post(
      '/currencies',
      json={
        "name": "dummy"
      },
      headers={
        'Authorization': f'Bearer {self.user_token}'
      }
    )
    data = json.loads(res.data)
    self.assertEqual(res.status_code, 200)
    self.assertEqual(data['success'], True)


  def test_get_users(self):
    res = self.client().get(
      '/users',
      headers={
        'Authorization': f'Bearer {self.user_token}'
      })
    data = json.loads(res.data)
    self.assertEqual(res.status_code, 200)
    self.assertGreater(len(data['users']), 0)

  def test_get_user(self):
    res = self.client().get(
      '/users/2',
      headers={
        'Authorization': f'Bearer {self.user_token}'
      })
    data = json.loads(res.data)
    self.assertEqual(res.status_code, 200)
    self.assertTrue(data['user']['name'])

  def test_delete_user(self):
    res = self.client().delete(
      '/users/3',
      headers={
        'Authorization': f'Bearer {self.user_token}'
      })
    data = json.loads(res.data)
    self.assertEqual(res.status_code, 200)
    self.assertEqual(data['success'], True)

  def test_delete_user_error(self):
    res = self.client().delete(
      '/users/9999',
      headers={
        'Authorization': f'Bearer {self.user_token}'
      })
    data = json.loads(res.data)
    self.assertEqual(res.status_code, 404)
    self.assertEqual(data['success'], False)

  def test_post_user(self):
    res = self.client().post(
      '/users',
      json={
        "name": "dummy",
        "email": "123@gmail.com"
      },
      headers={
        'Authorization': f'Bearer {self.user_token}'
      }
    )
    data = json.loads(res.data)
    self.assertEqual(res.status_code, 200)
    self.assertEqual(data['success'], True)
