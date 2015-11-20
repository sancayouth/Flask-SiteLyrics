# -*- coding: utf-8 -*-
from app import db, bcrypt
from flask import jsonify


class User(db.Model):

    __tablename__ = 'users'

    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String, nullable=False, unique=True)
    email = db.Column(db.String, nullable=False)
    password = db.Column(db.String)
    artists_creator = db.relationship('Artist', lazy='dynamic', backref='author')
    albums_creator = db.relationship('Album', lazy='dynamic', backref='author')
    lyrics_creator = db.relationship('Lyric', lazy='dynamic', backref='author')

    def __init__(self, username, email, password):
        self.username = username
        self.email = email
        self.password = bcrypt.generate_password_hash(password)

    def is_authenticated(self):
        return True

    def is_active(self):
        return True

    def is_anonymous(self):
        return False

    def get_id(self):
        return unicode(self.id)

    def __repr__(self):
        return '<Users (username=%r)>' % (self.username)


class Artist(db.Model):

    __tablename__ = 'artists'

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String, nullable=False)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'))
    albums_artist = db.relationship('Album', backref=db.backref('artist'),
                                     cascade='all, delete')

    def __init__(self, name, user_id):
        self.name = name
        self.user_id = user_id

    def get_id(self):
        return unicode(self.id)

    def get_name_without_spaces(self):
        return self.name.replace(' ', '').upper()

    @staticmethod
    def get_artists_by_letter(letter):
        artists = Artist.query.filter(Artist.name.like(letter+'%'))\
                .order_by('name').all()
        artists_list = []
        for artist in artists:
            art_dic = {}
            art_dic['name'] =  artist.name
            art_dic['name_ws'] = artist.name.replace(' ', '').upper()
            artists_list.append(art_dic)
        return artists_list

    def __repr__(self):
        return '<Artists (name=%r)>' % (self.name)


class Album(db.Model):

    __tablename__ = 'albums'

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String, nullable=False)
    year = db.Column(db.DateTime)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'))
    artist_id = db.Column(db.Integer, db.ForeignKey('artists.id'))
    lyrics_album = db.relationship('Lyric', lazy='dynamic', backref='album')

    def __init__(self, name, user_id, artist_id):
        self.name = name
        self.user_id = user_id
        self.artist_id = artist_id

    def get_id(self):
        return unicode(self.id)

    def get_name_without_spaces(self):
        return self.name.replace(' ', '').upper()

    def __repr__(self):
        return '<Albums (name=%r)>' % (self.name)


class Lyric(db.Model):

    __tablename__ = 'lyrics'

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String, nullable=False)
    lyric_song = db.Column(db.Text)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'))
    album_id = db.Column(db.Integer, db.ForeignKey('albums.id'))

    def __init__(self, name, lyric_song, user_id, artist_id):
        self.name = name
        self.user_id = user_id
        self.album_id = album_id
        self.lyric_song = lyric_song

    def get_name_without_spaces(self):
        return self.name.replace(' ', '').upper()

    def __repr__(self):
        return '<Lyrics (name=%r)>' % (self.name)
