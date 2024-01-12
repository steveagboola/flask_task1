from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from config import Config


#creating an instance of the Flask class(it takes one input)
app = Flask(__name__)

app.config.from_object(Config)

# Instanciate sqlalchemy and migrate
db = SQLAlchemy(app)
migrate = Migrate(app, db)

from . import routes, models