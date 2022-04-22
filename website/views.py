# stores the url endpoints for the actual functioning of website
# standard routes(url) to our webpage other than authentication
from flask import Blueprint, render_template, request, flash
from .models import Game, User, Leaderboard
from flask_login import login_required, current_user
from sqlalchemy import update, text, exc
from . import db
import datetime
from werkzeug.security import generate_password_hash, check_password_hash

views = Blueprint('views', __name__)

@views.route('/') # decorator
def home():
    return render_template("home.html", user = current_user)

@views.route('/leaderboard')
def leaderboard():
    query = 'select user_id, sum(points) from leaderboard group by game_id, user_id order by sum(points) desc limit 5;'
    query = text(query)
    scores = db.engine.execute(query)
    points = [(row[0], row[1]) for row in scores]
    return render_template("test.html", test = points)
    #return render_template("leaderboard.html", user = current_user)

@views.route('/settings', methods=['GET', 'POST'])
def settings():
    
    if request.method == 'POST':
        
        if request.form['submit_button'] == 'del_account':
            db.engine.execute('delete from leaderboard where user_id = ?', current_user.get_id())
            db.engine.execute('delete from user where id = ?', current_user.get_id())         
            return render_template("test.html", test = 'Deleted user account!')
        
        elif request.form['submit_button'] == 'change_username':
            if request.form['uname']:
                new_userName = request.form['uname']
                try:
                    db.engine.execute('update user set userName = ? where id = ?', new_userName, current_user.get_id())
                    return render_template("test.html", test = 'User name updated')
                except exc.IntegrityError:
                    return render_template("test.html", test = 'User name already exists.')
            else:
                return render_template("test.html", test = 'User name not provided')
        
        elif request.form['submit_button'] == 'change_password':
            
            check_pwd = User.query.filter_by(id = current_user.get_id()).first().password
            
            if check_password_hash(check_pwd, request.form['org_pwd']):
                
                if len(request.form['new_pwd']) < 7:
                    flash('Password must be at least 7 characters.', category='error')
                else:
                    pwd = generate_password_hash(request.form['new_pwd'], method= 'sha256')
                    db.engine.execute('update user set password = ? where id = ?', pwd, current_user.get_id())
                    flash('Passwords has been changed successfully.', category='success')
                
            elif check_password_hash(request.form['org_pwd'], db.engine.execute('select password from user where id = ?', current_user.get_id())):
                flash('Passwords don\'t match.', category='error')        
            
            else:
                flash('You seem to have entered wrong passwords.', category='error')
    
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
