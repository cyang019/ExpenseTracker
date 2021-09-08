import os
import sys
import datetime
from flask import Flask, request, abort, jsonify
from flask_sqlalchemy import SQLAlchemy
from flask_cors import CORS
sys.path.insert(0, os.path.dirname(os.path.dirname(__file__)))
from application.models import (
  setup_db, db, migrate,
  User, Card, Category, Transaction
)


TIME_FORMAT = "%m/%d/%y %H:%M:%S.%f"

def create_app(config_name):
  app = Flask(__name__)
  config_module = f"application.config.{config_name.capitalize()}Config"
  app.config.from_object(config_module)
  db.init_app(app)
  migrate.init_app(app, db)


  CORS(app, resources={r"/api/*": {"origins": "*"}})

  @app.route("/")
  def hello_world():
    return "Hello, World!"

  @app.after_request
  def after_request(response):
    response.headers.add(
      'Access-Control-Allow-Headers', 'Content-Type,Authorization,true')
    response.headers.add(
      'Access-Control-Allow-Methods', 'GET,PUT,POST,DELETE,OPTIONS')
    return response

  @app.route('/transactions', methods=['GET'])
  def get_transactions():
    selection = Transaction.query.all()
    transactions = [s.format() for s in selection]
    return jsonify({
      'success': True,
      'transactions': transactions
    })

  @app.route('/transactions/<int:transaction_id>', methods=['GET'])
  def get_transaction(transaction_id:int):
    selection = Transaction.query.filter(Transaction.id == transaction_id).one_or_none()
    if selection is None:
      abort(404)

    return jsonify({
      'success': True,
      'transaction': selection.format()
    })


  @app.route('/transactions', methods=['POST'])
  def post_transaction():
    body = request.get_json()
    card_id = body.get('card_id', None)
    category_id = body.get('category_id', None)
    amount = body.get('amount', None)
    currency_id = body.get('currency_id', None)
    time_str = body.get('time', None)
    time_obj = None
    if time_str is not None:
      time_obj = datetime.datetime.strptime(time_str, TIME_FORMAT)
    description = body.get('description')
    receipt_no = body.get('receipt_no')
    try:
      if amount is None:
        raise ValueError(f'Need transaction amount in cents.')
      transaction = Transaction(
        card_id=card_id,
        category_id=category_id,
        amount=amount,
        currency_id=currency_id,
        time=time_obj,
        description=description,
        receipt_no=receipt_no
      )
      transaction.insert()
    except Exception as e:
      error = True
      print(f'error creating new transaction: {e}')
      db.session.rollback()
    finally:
      db.session.close()
    if error:
      abort(422)

    return jsonify({
      'success': True
    })


  @app.route('/transactions/<int:transaction_id>', methods=['PATCH'])
  def patch_transaction(transaction_id:int):
    body = request.get_json()
    card_id = body.get('card_id', None)
    category_id = body.get('category_id', None)
    amount = body.get('amount', None)
    currency_id = body.get('currency_id', None)
    time_str = body.get('time', None)
    time_obj = None
    if time_str is not None:
      time_obj = datetime.datetime.strptime(time_str, TIME_FORMAT)
    description = body.get('description')
    receipt_no = body.get('receipt_no')
    try:
      transaction = Transaction.query().get(transaction_id)
      if card_id is not None:
        transaction.card_id = card_id
      if category_id is not None:
        transaction.category_id = category_id
      if amount is not None:
        transaction.amount = amount
      if currency_id is not None:
        transaction.currency_id = currency_id
      if time_obj is not None:
        transaction.time = time_obj
      if description is not None:
        transaction.description = description
      if receipt_no is not None:
        transaction.receipt_no = receipt_no
      transaction.update()
    except Exception as e:
      error = True
      print(f'error creating new transaction: {e}')
      db.session.rollback()
    finally:
      db.session.close()
    if error:
      abort(422)
    return jsonify({
      'success': True
    })

  @app.route('/transactions/<int:transaction_id>', methods=['DELETE'])
  def delete_transaction(transaction_id:int):
    transaction = Transaction.query.filter(Transaction.id == transaction_id).one_or_none()
    if transaction is None:
      abort(404)

    transaction.delete()
    return jsonify({
      'success': True,
      'deleted': transaction_id
    })

  @app.route('/cards', methods=['GET'])
  def get_cards():
    pass

  @app.route('/cards/<int:card_id>', methods=['GET'])
  def get_card(card_id:int):
    pass

  @app.route('/cards', methods=['POST'])
  def post_card(card_id:int):
    pass

  @app.route('/cards/<int:card_id>', methods=['DELETE'])
  def delete_card(card_id:int):
    pass

  @app.route('/categories', methods=['GET'])
  def get_categories():
    pass

  @app.route('/categories/<int:category_id>', methods=['GET'])
  def get_category(category_id:int):
    pass

  @app.route('/categories', methods=['POST'])
  def post_category(category_id:int):
    pass

  @app.route('/categories/<int:category_id>', methods=['DELETE'])
  def delete_category(category_id:int):
    pass

  @app.route('/currencies', methods=['GET'])
  def get_currencies():
    pass

  @app.route('/currencies/<int:currency_id>', methods=['GET'])
  def get_currency(currency_id:int):
    pass

  @app.route('/currencies', methods=['POST'])
  def post_currency(currency_id:int):
    pass

  @app.route('/currencies/<int:currency_id>', methods=['DELETE'])
  def delete_currency(currency_id:int):
    pass

  @app.route('/users', methods=['GET'])
  def get_users():
    pass

  @app.route('/users/<int:user_id>', methods=['GET'])
  def get_user(user_id:int):
    pass

  @app.route('/users', methods=['POST'])
  def post_user(user_id:int):
    pass

  @app.route('/users/<int:user_id>', methods=['DELETE'])
  def delete_user(user_id:int):
    pass

  @app.errorhandler(404)
  def not_found(error):
    return jsonify({
      "success": False,
      "error": 404,
      "message": "resource not found"
      }), 404

  @app.errorhandler(422)
  def unprocessable(error):
    return jsonify({
      "success": False,
      "error": 422,
      "message": "unprocessable"
      }), 422

  @app.errorhandler(400)
  def bad_request(error):
    return jsonify({
      "success": False,
      "error": 400,
      "message": "bad request"
      }), 400

  return app


if __name__ == '__main__':
  # database_name = "postgres"
  # database_path = "postgresql://{}:{}@{}/{}".format(
  #   'postgres', 'postgres',
  #   'localhost:6432', database_name)
  app = create_app('development')
  # setup_db(app, database_path)

  # binds the app to the current context
  # with app.app_context():
  #   db = SQLAlchemy()
  #   db.init_app(app)
  #   # create all tables
  #   db.create_all()
  
  app.run(host='127.0.0.1')
