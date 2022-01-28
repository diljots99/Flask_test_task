from flask import Flask
from flask_sqlalchemy import SQLAlchemy 
from datetime import datetime
from sqlalchemy.orm import relationship

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///db.sqlite3'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db = SQLAlchemy(app)

# user_channel = db.Table('User',
#     db.Column('id', db.Integer, db.ForeignKey('User.id')),
#     db.Column('user_game_rating_id', db.Integer, db.ForeignKey('USER_GAME_RATING.id'))
# )

# game_channel = db.Table('Game',
#     db.Column('id', db.Integer, db.ForeignKey('Game.id')),
#     db.Column('user_game_rating_id', db.Integer, db.ForeignKey('USER_GAME_RATING.id'))
# )

class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    Date_Created = db.Column(db.DateTime, server_default=db.func.current_timestamp())
    Last_Accessed = db.Column(db.DateTime, server_default=db.func.current_timestamp())
    first_name = db.Column(db.String(20))
    last_name = db.Column(db.String(20))
    # user_id = relationship(USER_GAME_RATING, backref="user", cascade="all, delete-orphan")

    def __repr__(self):
        return f'<User: {self.first_name}>'

class Game(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(20))
    Platform = db.Column(db.String(20))
    Avg_Rating = db.Column(db.String(20))

    def __repr__(self):
        return f'<Game: {self.name}>'

class USER_GAME_RATING(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    Rating = db.Column(db.String(20))
    user_id = relationship(User, backref="user", cascade="all, delete-orphan")
    game_id = relationship(Game, backref="game", cascade="all, delete-orphan")

    def __repr__(self):
        return f'<Rating: {self.Rating}>'