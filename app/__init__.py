from flask import Flask
from flask_migrate import Migrate
from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager
from flask_mail import Mail
from config import Config

app = Flask(__name__)
app.config.from_object(Config) 
mail = Mail(app)
db = SQLAlchemy(app)
migrate = Migrate(app, db)
login = LoginManager(app)
login.login_view = 'signin'
login.login_message = """
  if your are new here please use following link to sign up!
  otherwise login to your account.
  """
login.login_message_category = 'danger'

from app import app, routes
