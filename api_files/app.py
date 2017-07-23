"""Main app file acting as main entry point of the system."""
from flask import Flask
from flask_restplus import Api
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)
app.config.from_object('config')
db = SQLAlchemy(app)
api = Api(app,default='Mheshimiwa API Version 0.2', default_label='',
          version='0.2',doc='/docs')

from api_files import views
