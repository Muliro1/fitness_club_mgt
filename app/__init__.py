from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_bcrypt import Bcrypt
from flask_login import LoginManager
import mysql.connector
from flask_migrate import Migrate


app = Flask(__name__)
#mydb = mysql.connector.connect(host='localhost', user='muliro', passwd='nihilpraeteroptimum')
#cur = mydb.cursor()
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///fitness.db'
app.config['SECRET_KEY'] = 'relapse'
app.config.from_object('config')
db = SQLAlchemy(app)
with app.app_context():
    db.create_all()
bcrypt = Bcrypt(app)
login_manager = LoginManager(app)
login_manager.login_view = 'users.login'
migrate = Migrate(app, db)

from app import  models

from app.users.routes import users
from app.posts.routes import posts
from app.main.routes import main

app.register_blueprint(users)
app.register_blueprint(posts)
app.register_blueprint(main)





# Now we can access the configuration variables via app.config["VAR_NAME"].