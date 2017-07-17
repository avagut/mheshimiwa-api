"""Main app file."""
from flask import Flask
from flask_restplus import Api
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)
app.config.from_object('config')
db = SQLAlchemy(app)
api = Api(app,default='Mheshimiwa API Version 2.0', default_label='',
          version='2.0',doc='/docs')


from api_files import views
# from api_files.models import Constituency