from flask import Blueprint, render_template, request, flash, redirect, url_for
from .models import User
from werkzeug.security import generate_password_hash, check_password_hash
from . import db
from flask_login import login_user, login_required, logout_user, current_user

auth = Blueprint('auth', __name__)

@auth.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        userName = request.form.get('userName')
        password = request.form.get('password')

        user = User.query.filter_by(userName=userName).first()
        if user:
            if check_password_hash(user.password, password):
                flash('Logged in successfully!', category='success')
                login_user(user, remember=True)
                return redirect(url_for('views.home'))
            else:
                flash('Incorrect password, try again.', category='error')
        else:
            flash('User name does not exist.', category='error')

    return render_template("login.html", user=current_user)

@auth.route('/logout')
@login_required
def logout():
    logout_user()
    return redirect(url_for('auth.login'))

@auth.route('/signup', methods = ['GET', 'POST'])
def sign_up():
    if request.method == 'POST':
        user_name = request.form.get('userName')
        password1 = request.form.get('password1')
        password2 = request.form.get('password2')
        
        user = User.query.filter_by(userName = user_name).first()
        
        if user:
            flash('User already exists', category = 'error')
        elif len(user_name) < 2:
            flash('First name must be greater than 2 character.', category='error')
        elif password1 != password2:
            flash('Passwords don\'t match.', category='error')
        elif len(password1) < 7:
            flash('Password must be at least 7 characters.', category='error')
        else:
            #add to database
            new_user = User(userName = user_name, password = generate_password_hash(password1, method= 'sha256'))
            db.session.add(new_user) #adds entry to database
            db.session.commit()
            login_user(user, remember = True)  # remembers the user is logged in until the user clears their session
            flash('Account created', category='success')
            return redirect(url_for('views.home'))
            
    return render_template("signup.html", user = current_user)