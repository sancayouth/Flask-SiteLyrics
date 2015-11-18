from flask.ext.testing import TestCase
from app import create_app
from app.extensions import db
from app.models import User
from config import TestConfig


class BaseTestCase(TestCase):

    def create_app(self):
        app = create_app(TestConfig)
        return app

    def setUp(self):
        db.create_all()
        db.session.add(User(username="admin", email="ad@email.com",
                             password="admin"))
        db.session.commit()
        self.user = User.query.filter_by(username='admin').first()

    def login(self, username, password):
        return self.app.post('/login', data=dict( username=username,
                           password=password ), follow_redirects=True)

    def logout(self):
        return self.app.get('/logout', follow_redirects=True)

    def tearDown(self):
        db.session.remove()
        db.drop_all()
