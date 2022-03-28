#converts the website folder into a python package, executes everytime we import the website package
from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from os import path
from flask_login import LoginManager

db = SQLAlchemy()
DB_NAME = "mandela.db"

def create_app():
    app = Flask(__name__) #initialize our app
    app.config['SECRET_KEY'] = 'asdaysda jyhdajhdbaj' #encrypts cookies or session data related to the website
    app.config['SQLALCHEMY_DATABASE_URI'] = f'sqlite:///{DB_NAME}' #f-string can take python code in {} and will be evalluated as a string
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
    db.init_app(app)
   

    # import blueprints
    from .views import views
    from .auth import auth

    app.register_blueprint(views, url_prefix = '/')
    app.register_blueprint(auth, url_prefix = '/') 
    
    from .models import User, Game, Leaderboard #runs the class files before database has been created
    create_database(app)
    
    login_manager = LoginManager()
    login_manager.login_view = 'auth.login' #if login required where to redirect
    login_manager.init_app(app)
    
    @login_manager.user_loader
    def load_user(id):
        return User.query.get((int(id))) #tells flask how user is loaded - get looks for primary key by default
    return app

def create_database(app):
    if not path.exists('website/' + DB_NAME): #check if DB exists and create it
        db.create_all(app = app)
        print('Created Database!')