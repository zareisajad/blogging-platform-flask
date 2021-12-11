from flask import Flask
from flask_migrate import Migrate
from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager
from config import Config


app = Flask(__name__)
db = SQLAlchemy(app)
migrate = Migrate(app, db)
login = LoginManager(app)
app.config.from_object(Config)
login.login_view = 'signup'
login.login_message = """if youre new here please fill the form to sign up!
                            otherwise login to your account."""
login.login_message_category = 'danger'

from app import app, routes