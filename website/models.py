#used to store our database models
from . import db
from flask_login import UserMixin
from sqlalchemy.sql import func

class Game(db.Model):
    id = db.Column(db.Integer, primary_key = True)
    dateofpuzzle = db.Column(db.String(30))
    file1 = db.Column(db.String(350))
    file2 = db.Column(db.String(350))
    correct_option = db.Column(db.String(50))
    
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
    points = db.Column(db.Float)