#used to store our database models
from . import db
from flask_login import UserMixin
from sqlalchemy.sql import func

class Game(db.Model):
    id = db.Column(db.Integer, primary_key = True)
    desc = db.Column(db.String(150))
    date = db.Column(db.DateTime(timezone = True), default = func.now())
    score = db.Column(db.Integer)

class Question(db.Model):
    id = db.Column(db.Integer, primary_key = True)
    question = db.Column(db.String(200))
    correct_option = db.Column()
    other_option = db.Column()
    score_value = db.Column(db.Integer)
    
class User(db.Model, UserMixin):
    id = db.Column(db.Integer, primary_key = True)
    userName = db.Column(db.String(30), unique = True)
    password = db.Column(db.String(50))
    stats = db.relationship('Leaderboard')
    
class Leaderboard(db.Model):   
    id = db.Column(db.Integer, primary_key = True)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'))
    game_id = db.Column(db.Integer, db.ForeignKey('game.id'))
    date = db.Column(db.DateTime(timezone = True), default = func.now())
    points = db.Column(db.Integer)