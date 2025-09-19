from flask import Flask, render_template, redirect, url_for
from flask_bootstrap import Bootstrap5
from flask_wtf import FlaskForm, CSRFProtect
from wtforms import SelectField, SelectMultipleField, DateField, SubmitField
from wtforms.validators import DataRequired, Length

import secrets
foo = secrets.token_urlsafe(16)

app = Flask(__name__)
app.secret_key = foo
bootstrap = Bootstrap5(app)
csrf = CSRFProtect(app)

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
    return render_template('index.html', games=game_data)

@app.route('/add', methods=['GET', 'POST'])
def add_game():
    form = GameForm()
    if form.validate_on_submit():
        # flash(f'{ form.name.data } - { form.date.data } play created')
        play_object = {
            "name": form.name.data,
            "date": form.date.data,
            "players": form.players.data,
            "winner": form.winner.data,
            "rps": form.rps.data
        }
        game_data.append(play_object)
        return redirect(url_for('index'))
    return render_template('add_game.html', form = form)

@app.route('/users', methods=['GET', 'POST'])
def users():
    return render_template('users.html')

@app.route('/games')
def games():
    return render_template('games.html')

if __name__ == "__main__":
    app.run(debug=True)