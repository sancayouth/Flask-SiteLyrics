from flask.ext.script import Manager
from app import create_app
from app.extensions import db
from app.models import User, Artist, Album, Lyric
from config import DevelopmentConfig


app = create_app(DevelopmentConfig)
manager = Manager(app)


@manager.command
def run():
    app.run()


@manager.command
def test():
    import unittest
    tests = unittest.TestLoader().discover('tests')
    unittest.TextTestRunner(verbosity=2).run(tests)


@manager.command
def adduser(email, username):
    from getpass import getpass
    password = getpass()
    password2 = getpass(prompt='Confirm: ')
    if password != password2:
        import sys
        sys.exit('Error: passwords do not match.')
    db.create_all()
    user = User(email=email, username=username, password=password)
    db.session.add(user)
    db.session.commit()


@manager.command
def filldb():
    from datetime import datetime
    import random
    usr = User.query.get(1)
    artists = []
    for i in 'ABCDEFGHIJKLMNOPQRSTUVWXYZ':
        for j in range(1, 200):
            artists.append(Artist(i + ' ARTIST ' + str(j), usr.get_id()))
    db.session.add_all(artists)
    db.session.commit()
    arts = Artist.query.all()
    albums = []
    for artist in arts:
        for i in range(1, 3):
            albums.append(
                Album('ALBUM ' + str(i), datetime.now(),
                    usr.get_id(), artist.get_id()))
    db.session.add_all(albums)
    db.session.commit()
    albs = Album.query.all()
    lyrics = []
    song_ly = ''' nananananana
                  <br>
                  nanananananan
                  <br>
                  nananananana
                  <br>
                  nananananana
                  <br>
                  <br>
                  nananananana
                  <br>
                  nanananananan
                  <br>
                  nananananana
                  <br>
                  nananananana
                  <br>
                  batman batman'''
    words = ['music', 'letter', 'pop', 'rock', 'lyric', 'love', 'peace']
    for album in albs:
        for i in range(1, 8):
            lyrics.append(
                Lyric(
                    ' '.join(random.choice(words) for l in range(5)),
                    song_ly,
                    usr.get_id(),
                    album.get_id()
                )
            )
    db.session.add_all(lyrics)
    db.session.commit()


if __name__ == '__main__':
    manager.run()
