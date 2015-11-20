from flask.ext.script import Manager
from app import create_app
from app.extensions import db
from config import DevelopmentConfig
from app.models import User, Artist


app = create_app(DevelopmentConfig)
manager = Manager(app)


@manager.command
def run():
    app.run()


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
    usr = User.query.get(1)
    artists = []
    for i in 'ABCDEFGHIJKLMNOPQRSTUVWXYZ':
        for j in range(1, 200):
            artists.append(Artist(i +' ARTIST '+ str(j), usr.get_id()))
    db.session.add_all(artists)
    db.session.commit()

if __name__ == '__main__':
    manager.run()
