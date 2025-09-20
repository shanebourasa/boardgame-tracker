from flask import Blueprint, render_template, redirect, url_for
from .forms import GameForm, PlayerForm, PlayForm
from .models import db, Player, Play, Game

main = Blueprint("main", __name__)

@main.route('/')
def index():
    games = Play.query.order_by(Play.date.desc()).limit(10).all()
    return render_template('index.html', games=games)

@main.route('/add', methods=['GET', 'POST'])
def add_play():
    form = PlayForm()

    if form.validate_on_submit():
        # Handle Game dynamically
        selected_game = Game.query.get(form.game.data)
        if not selected_game:
            # fallback: create a new game if somehow the selected id doesn't exist
            selected_game = Game(name="Unknown")
            db.session.add(selected_game)
            db.session.commit()

        play = Play(
            game=selected_game,
            date=form.date.data
        )

        # Players: create new ones if they don't exist
        for pid in form.players.data:
            player = Player.query.get(pid)
            if not player:
                # This shouldn’t happen normally, but fallback
                player = Player(name=f"Player {pid}")
                db.session.add(player)
                db.session.commit()
            play.players.append(player)

        # Winner
        winner = Player.query.get(form.winner.data)
        if winner:
            play.winner = winner
        else:
            # fallback: create dynamically
            winner = Player(name=f"Winner {form.winner.data}")
            db.session.add(winner)
            db.session.commit()
            play.winner = winner

        # RPS
        rps_player = Player.query.get(form.rps.data)
        if rps_player:
            play.rps = rps_player
        else:
            rps_player = Player(name=f"RPS {form.rps.data}")
            db.session.add(rps_player)
            db.session.commit()
            play.rps = rps_player

        db.session.add(play)
        db.session.commit()
        return redirect(url_for('main.index'))

    return render_template('add_play.html', form=form)

@main.route('/add_player', methods=['GET', 'POST'])
def add_player():
    form = PlayerForm()
    if form.validate_on_submit():
        db.session.add(Player(name=form.name.data))
        db.session.commit()
        return redirect(url_for('main.add_play'))
    return render_template('add_player.html', form=form)

@main.route('/add_game', methods=['GET', 'POST'])
def add_game():
    form = GameForm()
    if form.validate_on_submit():
        db.session.add(Game(name=form.name.data))
        db.session.commit()
        return redirect(url_for('main.add_play'))
    return render_template('add_player.html', form=form)

@main.route('/users')
def users():
    return render_template('users.html')

@main.route('/games')
def games():
    return render_template('games.html')
