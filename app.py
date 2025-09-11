from flask import Flask, render_template, redirect, url_for
from flask_bootstrap import Bootstrap5
from flask_wtf import FlaskForm, CSRFProtect
from wtforms import SelectField, SelectMultipleField, DateField, SubmitField
from wtforms.validators import DataRequired, Length
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy.sql import text
from sqlalchemy import create_engine

engine = create_engine('sqlite:///boardgames.db')
db = SQLAlchemy()
db_name = 'boardgames.db'

import secrets
foo = secrets.token_urlsafe(16)

app = Flask(__name__)
app.secret_key = foo
bootstrap = Bootstrap5(app)
csrf = CSRFProtect(app)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///' + db_name
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = True

db.init_app(app)

game_data = [
    {
        'name': 'Catan',
        'date': '2024-03-24',
        'players': ['Shane', 'Brea'],
        'winner': 'Shane',
        'rps': 'Brea'
    },
    {
        'name': 'Chess',
        'date': '2024-06-22',
        'players': ['Shane', 'Brea'],
        'winner': 'Shane',
        'rps': 'Brea'
    },
    {
        'name': 'Power Hungry Pets',
        'date': '2024-12-13',
        'players': ['Shane', 'Brea', 'Zach', 'Owen'],
        'winner': 'Owen'
    }
]
player_list = ['Shane', 'Brea', 'Zach', 'Owen']
game_list = ['Catan', 'Chess', 'Power Hungry Pets', 'Battleship', 'Scrabble']

class GameForm(FlaskForm):
    name = SelectField('Game name:', choices=game_list)
    date = DateField('Date played:')
    players = SelectMultipleField('Players:', choices=player_list)
    winner = SelectField('Winner:', choices=player_list)
    rps = SelectField('RPS:', choices=player_list)
    submit = SubmitField('Submit')

@app.route('/', methods=['GET', 'POST'])
def index():
    form = GameForm()
    return render_template('index.html', games=game_data, form=form)

@app.route('/game/<name>')
def game_list(name):
    return render_template('games.html')

@app.route('/testdb')
def testdb():
    try:
        db.session.query(text('1')).from_statement(text('SELECT 1')).all()
        return '<h1>It works.</h1>'
    except Exception as e:
        error_text = "<p>The error:<br>" + str(e) + "</p>"
        hed = '<h1>Something is broken.</h1>'
        return hed + error_text

if __name__ == "__main__":
    app.run(debug=True)