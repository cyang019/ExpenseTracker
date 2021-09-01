import os
import sys
from flask import Flask, request, abort, jsonify
from flask_sqlalchemy import SQLAlchemy
from flask_cors import CORS
sys.path.insert(0, os.path.dirname(__file__))
from database.models import setup_db, db, User, Card, Category


def create_app(test_config=None):
  app = Flask(__name__)
  setup_db(app)

  CORS(app, resources={r"/api/*": {"origins": "*"}})

  @app.after_request
  def after_request(response):
    response.headers.add(
      'Access-Control-Allow-Headers', 'Content-Type,Authorization,true')
    response.headers.add(
      'Access-Control-Allow-Methods', 'GET,PUT,POST,DELETE,OPTIONS')
    return response

  @app.route('/transactions', method=['GET'])
  def get_transactions():
    pass

  @app.route('/transactions/<int:transaction_id>', methods=['GET'])
  def get_transaction(transaction_id:int):
    pass

  @app.route('/transactions', methods=['POST'])
  def post_transaction(transaction_id:int):
    pass

  @app.route('transactions/<int:transaction_id>', method=['PATCH'])
  def patch_transaction(transaction_id:int):
    pass

  @app.route('transactions/<int:transaction_id>', method=['DELETE'])
  def delete_transaction(transaction_id:int):
    pass

  @app.route('/cards', method=['GET'])
  def get_cards():
    pass

  @app.route('/cards/<int:card_id>', method=['GET'])
  def get_card(card_id:int):
    pass

  @app.route('/cards', method=['POST'])
  def post_card(card_id:int):
    pass

  @app.route('/cards/<int:card_id>', method=['DELETE'])
  def delete_card(card_id:int):
    pass

  @app.route('/categories', method=['GET'])
  def get_categories():
    pass

  @app.route('/categories/<int:category_id>', method=['GET'])
  def get_category(category_id:int):
    pass

  @app.route('/categories', method=['POST'])
  def post_category(category_id:int):
    pass

  @app.route('/categories/<int:category_id>', method=['DELETE'])
  def delete_category(category_id:int):
    pass

  @app.route('/currencies', method=['GET'])
  def get_currencies():
    pass

  @app.route('/currencies/<int:currency_id>', method=['GET'])
  def get_currency(currency_id:int):
    pass

  @app.route('/currencies', method=['POST'])
  def post_currency(currency_id:int):
    pass

  @app.route('/currencies/<int:currency_id>', method=['DELETE'])
  def delete_currency(currency_id:int):
    pass

  @app.route('/users', method=['GET'])
  def get_users():
    pass

  @app.route('/users/<int:user_id>', method=['GET'])
  def get_user(user_id:int):
    pass

  @app.route('/users', method=['POST'])
  def post_user(user_id:int):
    pass

  @app.route('/users/<int:user_id>', method=['DELETE'])
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

