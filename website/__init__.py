#converts the website folder into a python package, executes everytime we import the website package
from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from os import path

db = SQLAlchemy()
DB_NAME = "mandela.db"

def create_app():
    app = Flask(__name__) #initialize our app
    app.config['SECRET_KEY'] = 'asdaysda jyhdajhdbaj' #encrypts cookies or session data related to the website
    app.config['SQLALCHEMY_DATABASE_URI'] = f'sqlite:///{DB_NAME}' #f-string can take python code in {} and will be evalluated as a string
    db.init_app(app)

    # import blueprints
    from .views import views
    from .auth import auth

    app.register_blueprint(views, url_prefix = '/')
    app.register_blueprint(auth, url_prefix = '/') 
    
    from .models import User, Game, Leaderboard #runs the class files before database has been created
    
    create_database(app)
    return app

def create_database(app):
    if not path.exists('website/' + DB_NAME): #check if DB exists and create it
        db.create_all(app = app)
        print('Created Database!')