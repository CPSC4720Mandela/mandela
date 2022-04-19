# stores the url endpoints for the actual functioning of website
# standard routes(url) to our webpage other than authentication
from flask import Blueprint, render_template
from .models import Game
from flask_login import login_required, current_user
import datetime

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
    today = datetime.date.today()
    game = Game.query.filter_by(date=today).first()
    path1 = game.file1
    path2 = game.file2
    return render_template("game.html", path1, path2, user = current_user)

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
