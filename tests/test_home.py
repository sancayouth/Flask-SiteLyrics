from base import BaseTestCase
from app.models import Artist, Album, Lyric
from app.extensions import db
from datetime import datetime


class HomeTestCase(BaseTestCase):

    def test_show_up_on_main_page(self):
        response = self.client.get('/')
        self.assertIn(b'Flask Lyrics - Home', response.data)

    def test_show_up_artists(self):
        a1 = Artist('ARTIST 1', self.user.get_id())
        a2 = Artist('ARTIST 2', self.user.get_id())
        db.session.add_all([a1, a2])
        db.session.commit()
        response = self.client.get('/artists/A')
        self.assertIn(b'Flask Lyrics - Artists', response.data)
        self.assertIn(b'artist1', response.data)
        self.assertIn(b'artist2', response.data)

    def test_show_up_artists_list_lyrics(self):
        a1 = Artist('ARTIST 1', self.user.get_id())
        db.session.add(a1)
        db.session.commit()
        al1 = Album('album 1', datetime.now(), self.user.get_id(), a1.get_id())
        al2 = Album('album 2', datetime.now(), self.user.get_id(), a1.get_id())
        db.session.add_all([al1, al2])
        db.session.commit()
        l1 = Lyric('song to test 1', '', self.user.get_id(), al1.get_id())
        l2 = Lyric('song to test 2', '', self.user.get_id(), al2.get_id())
        db.session.add_all([l1, l2])
        db.session.commit()
        response = self.client.get('/artist/artist1')
        self.assertIn(b'Flask Lyrics - artist 1', response.data)
        self.assertIn(b'album 1', response.data)
        self.assertIn(b'album 2', response.data)
        self.assertIn(b'song to test 1', response.data)
        self.assertIn(b'song to test 2', response.data)

    def test_show_up_lyric_by_artist(self):
        a1 = Artist('ARTIST 1', self.user.get_id())
        db.session.add(a1)
        db.session.commit()
        al1 = Album('album 1', datetime.now(), self.user.get_id(), a1.get_id())
        db.session.add(al1)
        db.session.commit()
        l1 = Lyric('song 1', 'test 1', self.user.get_id(), al1.get_id())
        db.session.add(l1)
        db.session.commit()
        response = self.client.get('/lyrics/artist1/1')
        self.assertIn(b'Flask Lyric - song 1', response.data)
        self.assertIn(b'ARTIST 1 LYRICS', response.data)
        self.assertIn(b'test 1', response.data)