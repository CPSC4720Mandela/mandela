# stores the url endpoints for the actual functioning of website
# standard routes(url) to our webpage other than authentication
from flask import Blueprint, render_template
from flask_login import login_required, current_user

views = Blueprint('views', __name__)


@views.route('/') # decorator
def home():
    return render_template("home.html", user = current_user)

@views.route('/leaderboard')
def leaderboard():
    return render_template("leaderboard.html", user = current_user)

@views.route('/settings')
def settings():
    return render_template("settings.html", user = current_user)

@views.route('/game', methods=['GET', 'POST'])
def game():
    return render_template("game.html", user = current_user)

'''
def game():
    if request.method == 'GET':
        # get the questions and send to the front end
    elif request.method == 'POST':
        # get score from front end and send to db
    return render_template("game.html", user = current_user)
    
'''
@views.route('/about')
def about():
    return render_template("about.html", user = current_user)
