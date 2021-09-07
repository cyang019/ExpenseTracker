import os
import sys
from flask import Flask, request, abort, jsonify
from flask_sqlalchemy import SQLAlchemy
from flask_cors import CORS
sys.path.insert(0, os.path.dirname(os.path.dirname(__file__)))
from application.models import (
  setup_db, db, migrate,
  User, Card, Category, Transaction
)

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
  def post_transaction(transaction_id:int):
    pass

  @app.route('/transactions/<int:transaction_id>', methods=['PATCH'])
  def patch_transaction(transaction_id:int):
    pass

  @app.route('/transactions/<int:transaction_id>', methods=['DELETE'])
  def delete_transaction(transaction_id:int):
    pass

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
  database_name = "postgres"
  database_path = "postgresql://{}:{}@{}/{}".format(
    'postgres', 'postgres',
    'localhost:6432', database_name)
  app = create_app()
  # setup_db(app, database_path)

  # binds the app to the current context
  # with app.app_context():
  #   db = SQLAlchemy()
  #   db.init_app(app)
  #   # create all tables
  #   db.create_all()
  
  app.run(host='127.0.0.1')
