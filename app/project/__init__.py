
# Import various modules

from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate 
from flask_login import LoginManager

# Setting up the app instance of FLask
app = Flask(__name__)

# Importing the configurations from app\config.py as an object
app.config.from_object("config.DevelopmentConfig")

# Initializing the modules
db = SQLAlchemy(app)
migrate = Migrate(app,db)
login_manager = LoginManager(app)
login_manager.login_view = 'login'

from project import views

