from flask import Blueprint, render_template, redirect, url_for, request
from .forms import GameForm, PlayerForm, PlayForm
from .models import db, Player, Play, Game
from sqlalchemy import select

main = Blueprint("main", __name__)

@main.route('/')
def index():
    games = Play.query.order_by(Play.date.desc()).order_by(Play.created_at.desc()).limit(10).all()
    return render_template('index.html', games=games)

@main.route('/add', methods=['GET', 'POST'])
def add_play():
    form = PlayForm()

    if form.validate_on_submit():
        selected_game = Game.query.get(form.game.data)

        play = Play(
            game=selected_game,
            date=form.date.data
        )

        for pid in form.players.data:
            player = Player.query.get(pid)
            play.players.append(player)

        winner = Player.query.get(form.winner.data)
        if winner:
            play.winner = winner

        rps_player = Player.query.get(form.rps.data)
        if rps_player:
            play.rps = rps_player

        db.session.add(play)
        db.session.commit()
        return redirect(url_for('main.index'))

    return render_template('add_play.html', form=form)

@main.route('/add_player', methods=['GET', 'POST'])
def add_player():
    form = PlayerForm()
    if form.validate_on_submit():
        db.session.add(Player(name=form.name.data.title()))
        db.session.commit()
        return redirect(url_for('main.add_play'))
    return render_template('add_player.html', form=form)

@main.route('/add_game', methods=['GET', 'POST'])
def add_game():
    form = GameForm()
    if form.validate_on_submit():
        db.session.add(Game(name=form.name.data.title()))
        db.session.commit()
        return redirect(url_for('main.add_play'))
    return render_template('add_player.html', form=form)

@main.route('/players')
def players():
    player_list = Player.query.order_by(Player.name).all()
    return render_template('players.html', player_list=player_list)

@main.route('/players/<int:id>')
def player_profile(id):
    player = Player.query.get(id)
    recent_plays = Play.query.filter(Play.players.any(id=id)).order_by(Play.date.desc()).all()
    return render_template('player.html', player=player, recent_plays=recent_plays)

@main.route('/games')
def games():
    game_list = Game.query.order_by(Game.name).all()
    return render_template('games.html', game_list=game_list)

@main.route('/games/<int:id>')
def game_profile(id):
    game = Game.query.get(id)
    recent_plays = Play.query.filter(Play.game_id == id).order_by(Play.date.desc()).all()
    return render_template('game.html', game=game, recent_plays=recent_plays)
