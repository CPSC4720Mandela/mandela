#converts the website folder into a python package, executes everytime we import the website package
from flask import Flask

def create_app():
    app = Flask(__name__) #initialize our app
    app.config['SECRET_KEY'] = 'asdaysda jyhdajhdbaj' #encrypts cookies or session data related to the website

    # import blueprints
    from .views import views
    from .auth import auth

    app.register_blueprint(views, url_prefix = '/')
    app.register_blueprint(auth, url_prefix = '/') 

    return app