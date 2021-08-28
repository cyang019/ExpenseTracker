import os
from sqlalchemy import Column, String, Integer
from flask_sqlalchemy import SQLAlchemy
import ast
import json

database_name = "expenses"
database_path = "postgresql://{}/{}".format("localhost:5432", database_filename))

db = SQLAlchemy()

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


