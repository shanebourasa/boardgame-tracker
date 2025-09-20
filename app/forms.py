from flask_wtf import FlaskForm
from wtforms import SelectField, SelectMultipleField, DateField, SubmitField, StringField
from wtforms.validators import DataRequired
from .models import Player, Game
from flask import current_app

class PlayForm(FlaskForm):
    game = SelectField('Game name:', coerce=int, validators=[DataRequired()])
    date = DateField('Date played:', validators=[DataRequired()])
    players = SelectMultipleField('Players:', coerce=int, validators=[DataRequired()])
    winner = SelectField('Winner:', coerce=int)
    rps = SelectField('RPS:', coerce=int)
    submit = SubmitField('Submit')

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        # Dynamically populate from database
        self.players.choices = [(p.id, p.name) for p in Player.query.order_by(Player.name).all()]
        self.winner.choices = [(p.id, p.name) for p in Player.query.order_by(Player.name).all()]
        self.rps.choices = [(p.id, p.name) for p in Player.query.order_by(Player.name).all()]
        self.game.choices = [(g.id, g.name) for g in Game.query.order_by(Game.name).all()]

class PlayerForm(FlaskForm):
    name = StringField('Player name:')
    submit = SubmitField('Submit')
    
class GameForm(FlaskForm):
    name = StringField('Game name:')
    submit = SubmitField('Submit')