import os
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

    def __repr__(self):
        return f'<User {self.id} {self.name}>'


class Card(db.Model):
    __tablename__ = "card"

    id = Column(Integer, primary_key=True)
    user_id = Column(Integer, db.ForeignKey('user.id'), nullable=False)
    number = Column(String)
    code = Column(String)
    processor = Column(String)

    def __repr__(self):
        return f'<Card {self.id} {self.user_id} {self.processor} {self.number}>'


class Category(db.Model):
    __tablename__ = "category"

    id = Column(Integer, primary_key=True)
    name = Column(String)

    def __repr__(self):
        return f'<Category {self.id} {self.name}>'

class Currency(db.Model):
    __tablename__ = "currency"

    id = Column(Integer, primary_key=True)
    name = Column(String)


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

    def __repr__(self):
        return f'<Transaction {self.id} {amount} {time} {receipt_no}>'
