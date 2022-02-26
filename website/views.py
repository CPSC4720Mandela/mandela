# stores the url endpoints for the actual functioning of website
# standard routes(url) to our webpage other than authentication
from flask import Blueprint

views = Blueprint('views', __name__)

@views.route('/') #decorator
def home():
    return "<h1>Test</h1>"
    
