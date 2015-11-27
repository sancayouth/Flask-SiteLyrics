# -*- coding: utf-8 -*-
from flask import Blueprint, render_template, redirect, url_for
from app.models import Artist, Lyric

home = Blueprint('home', __name__, template_folder='templates')


@home.route('/')
def home_():
    return render_template('index.html', title='Flask Lyrics - Home')


@home.route('/artists/<letter>')
def artists_by_letter(letter):
    if  len(letter) == 1 and letter.isalpha():
        artists = Artist.get_artists_by_letter(letter)
        left = []
        right = []
        for i, artist in enumerate(artists):
            if i % 2 == 0:
                left.append(artist)
            else:
                right.append(artist)
        return render_template('artists.html', title='Flask Lyrics - Artists',
                                left=left, right=right, letter=letter)
    return redirect(url_for('home.home_'))


@home.route('/artist/<artist_ws>')
def albums_by_artist(artist_ws):
    artist = Artist.query.filter_by(name_ws=artist_ws).first()
    if artist:
        return render_template(
                    'artist.html',
                    title='Flask Lyrics - ' + artist.name, artist=artist)
    return redirect(url_for('home.home_'))


@home.route('/lyrics/<artist_ws>/<int:lyric_id>')
def lyric_by_artist(artist_ws, lyric_id=None):
    artist = Artist.query.filter_by(name_ws=artist_ws).first()
    if artist and lyric_id:
        lyric = Lyric.query.filter_by(id=lyric_id).first()
        if lyric:
            return render_template(
                        'lyric.html',
                        title='Flask Lyric - ' + lyric.name, artist=artist,
                        lyric=lyric)
    return redirect(url_for('home.home_'))
