import sys
import os
import unittest
import json
from flask_sqlalchemy import SQLAlchemy
sys.path.insert(
  0,
  os.path.join(
    os.path.dirname(
      os.path.dirname(__file__)),
    'src'))
from api import create_app


class ExpenseTrackerTestCase(unittest.TestCase):
  """Testing backend apis for expense tracker.
  """
  def setUp(self):
    self.app = create_app()
    self.client = self.app.test_client
    self.database_name = "expense_tracker_test"
    self.database_path = "postgresql://{}/{}".format(
      'localhost:5432', self.database_name)
    setup_db(self.app, self.database_path)

    # binds the app to the current context
    with self.app.app_context():
      self.db = SQLAlchemy()
      self.db.init_app(self.app)
      # create all tables
      self.db.create_all()
  
  def tearDown(self):
    pass
  