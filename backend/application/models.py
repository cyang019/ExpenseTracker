import os
import math
from sqlalchemy import Column, String, Integer, Float, DateTime
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
import ast
import json

database_name = "expenses"
database_path = "postgresql://{}/{}".format("localhost:5432", database_name)

db = SQLAlchemy()
migrate = Migrate()

'''
setup_db(app)
    binds a flask application and a SQLAlchemy service
'''


def setup_db(app, database_path=database_path):
    app.config["SQLALCHEMY_DATABASE_URI"] = database_path
    app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False
    db.app = app
    db.init_app(app)
    db.create_all()


class User(db.Model):
    __tablename__ = "user"

    id = Column(Integer, primary_key=True)
    name = Column(String)
    email = Column(String)

    def __init__(self, name, email):
        self.name = name
        self.email = email

    def __repr__(self):
        return f'<User {self.id} {self.name}>'
    
    def insert(self):
        db.session.add(self)
        db.session.commit()

    def update(self):
        db.session.commit()

    def delete(self):
        db.session.delete(self)
        db.session.commit()

    def format(self):
        return {
            'id': self.id,
            'name': self.name,
            'email': self.email
        }


class Card(db.Model):
    __tablename__ = "card"

    id = Column(Integer, primary_key=True)
    user_id = Column(Integer, db.ForeignKey('user.id'), nullable=False)
    number = Column(String)
    code = Column(String)
    processor = Column(String)

    def __repr__(self):
        return f'<Card {self.id} {self.user_id} {self.processor} {self.number}>'

    def __init__(self, user_id, number, code, processor):
        self.user_id = user_id
        self.number = number
        self.code = str(code)
        self.processor = str(processor).lower()
    
    def insert(self):
        db.session.add(self)
        db.session.commit()

    def update(self):
        db.session.commit()

    def delete(self):
        db.session.delete(self)
        db.session.commit()

    def format(self):
        return {
            'id': self.id,
            'user_id': self.user_id,
            'number': self.number,
            'code': self.code,
            'processor': self.processor
        }


class Category(db.Model):
    __tablename__ = "category"

    id = Column(Integer, primary_key=True)
    name = Column(String)

    def __repr__(self):
        return f'<Category {self.id} {self.name}>'

    def __init__(self, name):
        self.name = str(name)

    def insert(self):
        db.session.add(self)
        db.session.commit()

    def update(self):
        db.session.commit()

    def delete(self):
        db.session.delete(self)
        db.session.commit()

    def format(self):
        return {
            'id': self.id,
            'name': self.name
        }

class Currency(db.Model):
    __tablename__ = "currency"

    id = Column(Integer, primary_key=True)
    name = Column(String)

    def __init__(self, name):
        self.name = str(name)

    def insert(self):
        db.session.add(self)
        db.session.commit()

    def update(self):
        db.session.commit()

    def delete(self):
        db.session.delete(self)
        db.session.commit()

    def format(self):
        return {
            'id': self.id,
            'name': self.name
        }


class Transaction(db.Model):
    __tablename__ = "transaction"

    id = Column(Integer, primary_key=True)
    card_id = Column(Integer, db.ForeignKey('card.id'), nullable=False)
    category_id = Column(Integer, db.ForeignKey('category.id'), nullable=False)
    amount = Column(Integer)    # in cents
    currency_id = Column(Integer, db.ForeignKey('currency.id'), nullable=False)
    time = Column(DateTime)
    description = Column(String)
    receipt_no = Column(String)

    def __init__(self, card_id, category_id, amount, currency_id, time, description, receipt_no):
        self.card_id = card_id
        self.category_id = category_id
        self.amount = int(amount)   # in cents
        self.currency_id = currency_id
        self.time = time
        self.description = str(description)
        self.receipt_no = str(receipt_no)
    
    def insert(self):
        db.session.add(self)
        db.session.commit()

    def update(self):
        db.session.commit()

    def delete(self):
        db.session.delete(self)
        db.session.commit()

    def __repr__(self):
        return f'<Transaction {self.id} {amount} {time} {receipt_no}>'

    def format(self):
        return {
            'id': self.id,
            'card_id': self.card_id,
            'category_id': self.category_id,
            'amount': self.amount,
            'currency_id': self.currency_id,
            'time': self.time,
            'description': self.description,
            'receipt_no': self.receipt_no
        }
