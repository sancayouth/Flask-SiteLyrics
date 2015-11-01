from flask.ext.script import Manager
from app import create_app
from app.extensions import db
from app.models import User


app = create_app()
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


if __name__ == '__main__':
    manager.run()
