from . import db
from datetime import datetime

# Association table for many-to-many
play_players = db.Table(
    'play_players',
    db.Column('play_id', db.Integer, db.ForeignKey('play.id'), primary_key=True),
    db.Column('player_id', db.Integer, db.ForeignKey('player.id'), primary_key=True)
)

class Player(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), unique=True, nullable=False)

    def __repr__(self):
        return f"<Player {self.name}>"

class Game(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), unique=True, nullable=False)

    def __repr__(self):
        return f"<Game {self.name}>"

class Play(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    game_id = db.Column(db.Integer, db.ForeignKey('game.id'), nullable=False)
    date = db.Column(db.Date, nullable=False)
    winner_id = db.Column(db.Integer, db.ForeignKey('player.id'))
    rps_id = db.Column(db.Integer, db.ForeignKey('player.id'))
    created_at = db.Column(db.DateTime, default=datetime.now)

    # Relationships
    game = db.relationship('Game', backref='plays', foreign_keys=[game_id])
    players = db.relationship('Player', secondary=play_players, backref='plays')
    winner = db.relationship('Player', foreign_keys=[winner_id])
    rps = db.relationship('Player', foreign_keys=[rps_id])

    def __repr__(self):
        return f"<Play {self.game.name} on {self.date}>"
