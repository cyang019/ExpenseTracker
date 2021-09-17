import os
import sys
import datetime
from flask import Flask, request, abort, jsonify
from flask_sqlalchemy import SQLAlchemy
from flask_cors import CORS, cross_origin
from werkzeug.exceptions import HTTPException

from application.models import (
  setup_db, db, migrate,
  CardUser, Card, Category, Transaction, Currency
)
from application.auth import AuthError, requires_auth, requires_scope


TIME_FORMAT = "%m/%d/%y %H:%M:%S.%f"


def setup_app(app):
  config_name = os.environ.get("FLASK_CONFIG", "development")
  config_module = f"application.config.{config_name.capitalize()}Config"
  app.config.from_object(config_module)


app = Flask(__name__)
setup_app(app)
setup_db(app)

CORS(app, resources={r"/api/*": {"origins": "*"}})

# @app.route("/")
# def hello_world():
#   return "Hello, World!"

@app.after_request
def after_request(response):
  response.headers.add(
    'Access-Control-Allow-Headers', 'Content-Type,Authorization,true')
  response.headers.add(
    'Access-Control-Allow-Methods', 'GET,PUT,POST,PATCH,DELETE,OPTIONS')
  return response

@app.route('/transactions', methods=['GET'])
@requires_auth
def get_transactions():
  if not requires_scope('view:transactions'):
    abort(403)
  selection = Transaction.query.all()
  transactions = [s.format() for s in selection]
  return jsonify({
    'success': True,
    'transactions': transactions
  })

@app.route('/transactions/<int:transaction_id>', methods=['GET'])
@requires_auth
def get_transaction(transaction_id: int):
  if not requires_scope('view:transactions'):
    abort(403)
  selection = Transaction.query.filter(
    Transaction.id == transaction_id).one_or_none()
  if selection is None:
    abort(404)

  return jsonify({
    'success': True,
    'transaction': selection.format()
  })

@app.route('/transactions', methods=['POST'])
@requires_auth
def post_transaction():
  if not requires_scope('create:transactions'):
    abort(403)
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
  error = False
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
@requires_auth
def patch_transaction(transaction_id: int):
  if not requires_scope('update:transactions'):
    abort(403)
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
  error = False
  try:
    transaction = Transaction.query.get(transaction_id)
    if transaction is None:
      abort(404)
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
@requires_auth
def delete_transaction(transaction_id: int):
  if not requires_scope('delete:transactions'):
    abort(403)
  transaction = Transaction.query.filter(
    Transaction.id == transaction_id).one_or_none()
  if transaction is None:
    abort(404)

  transaction.delete()
  return jsonify({
    'success': True,
    'deleted': transaction_id
  })

@app.route('/cards', methods=['GET'])
@requires_auth
def get_cards():
  if not requires_scope('view:cards'):
    abort(403)
  selection = Card.query.all()
  cards = [s.format() for s in selection]
  return jsonify({
    'success': True,
    'cards': cards
  })

@app.route('/cards/<int:card_id>', methods=['GET'])
@requires_auth
def get_card(card_id: int):
  if not requires_scope('view:cards'):
    abort(403)
  selection = Card.query.filter(Card.id == card_id).one_or_none()
  if selection is None:
    abort(404)

  return jsonify({
    'success': True,
    'card': selection.format()
  })

@app.route('/cards', methods=['POST'])
@requires_auth
def post_card():
  if not requires_scope('create:cards'):
    abort(403)
  body = request.get_json()
  user_id = body.get('user_id', None)
  card_number = body.get('number', None)
  card_code = body.get('code', None)
  card_expire = body.get('expire', None)
  card_processor = body.get('processor', None)
  error = False
  try:
    if card_number is None:
      raise ValueError(f'Need card number.')
    card = Card(
      user_id=user_id,
      number=card_number,
      code=card_code,
      expire=card_expire,
      processor=card_processor
    )
    card.insert()
  except Exception as e:
    error = True
    print(f'error creating new card: {e}')
    db.session.rollback()
  finally:
    db.session.close()
  if error:
    abort(422)

  return jsonify({
    'success': True
  })

@app.route('/cards/<int:card_id>', methods=['DELETE'])
@requires_auth
def delete_card(card_id: int):
  if not requires_scope('delete:cards'):
    abort(403)
  card = Card.query.filter(Card.id == card_id).one_or_none()
  if card is None:
    abort(404)

  card.delete()
  return jsonify({
    'success': True,
    'deleted': card_id
  })

@app.route('/categories', methods=['GET'])
@requires_auth
def get_categories():
  if not requires_scope('view:categories'):
    abort(403)
  selection = Category.query.all()
  categories = [s.format() for s in selection]
  return jsonify({
    'success': True,
    'categories': categories
  })

@app.route('/categories/<int:category_id>', methods=['GET'])
@requires_auth
def get_category(category_id: int):
  if not requires_scope('view:categories'):
    abort(403)
  selection = Category.query.filter(Category.id == category_id).one_or_none()
  if selection is None:
    abort(404)

  return jsonify({
    'success': True,
    'category': selection.format()
  })

@app.route('/categories', methods=['POST'])
@requires_auth
def post_category():
  if not requires_scope('create:categories'):
    abort(403)
  body = request.get_json()
  cat_name = body.get('name', None)
  error = False
  try:
    if cat_name is None:
      raise ValueError(f'Need category name.')
    category = Category(name=cat_name)
    category.insert()
  except Exception as e:
    error = True
    print(f'error creating new category: {e}')
    db.session.rollback()
  finally:
    db.session.close()
  if error:
    abort(422)

  return jsonify({
    'success': True
  })

@app.route('/categories/<int:category_id>', methods=['DELETE'])
@requires_auth
def delete_category(category_id: int):
  if not requires_scope('delete:categories'):
    abort(403)
  error = False
  status_code = 200
  try:
    selection = Transaction.query.filter(
      Transaction.category_id == category_id).all()
    if selection is not None:
      for item in selection:
        item.delete()

    cat = Category.query.filter(Category.id == category_id).one_or_none()
    if cat is None:
      abort(404)
    cat.delete()
  except Exception as e:
    db.session.rollback()
    error = True
    if isinstance(e, HTTPException):
      status_code = e.code
    else:
      status_code = 422
    print(f'error deleting category {category_id}: {e}')
  finally:
    db.session.close()
  if error:
    abort(status_code)

  return jsonify({
    'success': True,
    'deleted': category_id
  })

@app.route('/currencies', methods=['GET'])
@requires_auth
def get_currencies():
  if not requires_scope('view:currencies'):
    abort(403)
  selection = Currency.query.all()
  res = [s.format() for s in selection]
  return jsonify({
    'success': True,
    'currencies': res
  })

@app.route('/currencies/<int:currency_id>', methods=['GET'])
@requires_auth
def get_currency(currency_id: int):
  if not requires_scope('view:currencies'):
    abort(403)
  selection = Currency.query.filter(Currency.id == currency_id).one_or_none()
  if selection is None:
    abort(404)

  res = selection.format()
  return jsonify({
    'success': True,
    'currency': res
  })

@app.route('/currencies', methods=['POST'])
@requires_auth
def post_currency():
  if not requires_scope('create:currencies'):
    abort(403)
  body = request.get_json()
  name = body.get('name', None)
  error = False
  try:
    if name is None:
      raise ValueError(f'Need currency name.')
    currency = Currency(name=name)
    currency.insert()
  except Exception as e:
    error = True
    print(f'error creating new currency: {e}')
    db.session.rollback()
  finally:
    db.session.close()
  if error:
    abort(422)

  return jsonify({
    'success': True
  })

@app.route('/currencies/<int:currency_id>', methods=['DELETE'])
@requires_auth
def delete_currency(currency_id: int):
  if not requires_scope('delete:currencies'):
    abort(403)
  error = False
  status_code = 200
  try:
    selection = Transaction.query.filter(
      Transaction.currency_id == currency_id).all()
    if selection is not None:
      for item in selection:
        item.delete()

    ans = Currency.query.filter(Currency.id == currency_id).one_or_none()
    if ans is None:
      abort(404)

    ans.delete()
  except Exception as e:
    error = True
    db.session.rollback()
    if isinstance(e, HTTPException):
      status_code = e.code
    else:
      status_code = 422
    print(f'error deleting currency {currency_id}: {e}')
  finally:
    db.session.close()
  if error:
    abort(status_code)
  return jsonify({
    'success': True,
    'deleted': currency_id
  })

@app.route('/users', methods=['GET'])
@requires_auth
def get_users():
  if not requires_scope('view:users'):
    abort(403)
  selection = CardUser.query.all()
  res = [s.format() for s in selection]
  return jsonify({
    'success': True,
    'users': res
  })

@app.route('/users/<int:user_id>', methods=['GET'])
@requires_auth
def get_user(user_id: int):
  if not requires_scope('view:users'):
    abort(403)
  selection = CardUser.query.filter(
    CardUser.id == user_id).one_or_none()
  if selection is None:
    abort(404)

  res = selection.format()
  return jsonify({
    'success': True,
    'user': res
  })

@app.route('/users', methods=['POST'])
@requires_auth
def post_user():
  if not requires_scope('create:users'):
    abort(403)
  body = request.get_json()
  name = body.get('name', None)
  email = body.get('email', "")
  error = False
  try:
    if name is None:
      raise ValueError(f'Need user name.')
    user = CardUser(name=name, email=email)
    user.insert()
  except Exception as e:
    error = True
    print(f'error creating new user: {e}')
    db.session.rollback()
  finally:
    db.session.close()
  if error:
    abort(422)

  return jsonify({
    'success': True
  })

@app.route('/users/<int:user_id>', methods=['DELETE'])
@requires_auth
def delete_user(user_id: int):
  if not requires_scope('delete:users'):
    abort(403)
  error = False
  status_code = 200
  try:
    cards = Card.query.filter(Card.user_id == user_id).all()
    if cards is not None:
      for card in cards:
        selection = Transaction.query.filter(
          Transaction.card_id == card.id).all()
        if selection is not None:
          for item in selection:
            item.delete()
        card.delete()

    ans = CardUser.query.filter(CardUser.id == user_id).one_or_none()
    if ans is None:
      abort(404)

    ans.delete()
  except Exception as e:
    error = True
    db.session.rollback()
    if isinstance(e, HTTPException):
      status_code = e.code
    else:
      status_code = 422
    print(f'error deleting user {user_id}: {e}')
  finally:
    db.session.close()
  if error:
    abort(status_code)

  return jsonify({
      'success': True,
      'deleted': user_id
    })

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

@app.errorhandler(403)
def bad_request(error):
  return jsonify({
    "success": False,
    "error": 403,
    "message": "You don't have access to this resource"
    }), 403


if __name__ == '__main__':
  # database_name = "postgres"
  # database_path = "postgresql://{}:{}@{}/{}".format(
  #   'postgres', 'postgres',
  #   'localhost:6432', database_name)
  # app = create_app('development')
  with app.app_context():
    db.create_all()
  # setup_db(app, database_path)

  # binds the app to the current context
  # with app.app_context():
  #   db = SQLAlchemy()
  #   db.init_app(app)
  #   # create all tables
  #   db.create_all()

  app.run(host='0.0.0.0')
