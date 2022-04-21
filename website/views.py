# stores the url endpoints for the actual functioning of website
# standard routes(url) to our webpage other than authentication
from flask import Blueprint, render_template, request
from .models import Game, User, Leaderboard
from flask_login import login_required, current_user
from sqlalchemy import update
from . import db
import datetime

views = Blueprint('views', __name__)

@views.route('/') # decorator
def home():
    return render_template("home.html", user = current_user)

@views.route('/leaderboard', methods=['GET', 'POST'])
def leaderboard():
    
    return render_template("leaderboard.html", user = current_user)

@views.route('/settings')
def settings():
    return render_template("settings.html", user = current_user)

@views.route('/game', methods=['GET', 'POST'])
def game():
    if request.method == 'POST':
        try:
            check_val = request.form['Option1']
        except:
            check_val = request.form['Option2']
            
        game = Game.query.filter_by(dateofpuzzle = str(datetime.date.today())).first()
          
        if check_val == game.correct_option and current_user.is_authenticated: # answer is correct and the user is authenticated
            leaderboard = Leaderboard.query.filter_by(game_id = game.id, user_id = current_user.get_id()).first()
            
            if leaderboard is None:
                new_entry = Leaderboard(game_id = game.id, user_id = current_user.get_id(), points = 10)
                db.session.add(new_entry) # adds new entry to database
                db.session.commit()
                check = "It's the right answer your score has been updated in the Leaderboard!"
                
            else:
                check = 'You have already played the game!'
            return render_template("test.html", test = check)
        
        elif check_val == game.correct_option:
            check = "Congratulations, it's the right answer!"
            return render_template("test.html", test = check) # right answer but user in not authenticated
        
        else:
            check = "Oops, that's the wrong answer!"
            return render_template("test.html", test = check) # the wrong answer
    
    else:
        game = Game.query.filter_by(dateofpuzzle = str(datetime.date.today())).first() # Load the initial page
        return render_template("game.html", user = current_user, path1 = '..' + game.file1, path2 = '..' + game.file2)

@views.route('/about')
def about():
    return render_template("about.html", user = current_user)
