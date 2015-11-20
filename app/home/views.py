# -*- coding: utf-8 -*-
from flask import Blueprint, render_template, redirect, url_for
from app.models import Artist

home = Blueprint('home', __name__, template_folder='templates')


@home.route('/')
def home_():
    return render_template('index.html', title='Flask Lyrics')


@home.route('/<letter>')
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
