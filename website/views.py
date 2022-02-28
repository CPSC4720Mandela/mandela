# stores the url endpoints for the actual functioning of website
# standard routes(url) to our webpage other than authentication
from flask import Blueprint, render_template

views = Blueprint('views', __name__)

@views.route('/') #decorator
def home():
    return render_template("home.html")