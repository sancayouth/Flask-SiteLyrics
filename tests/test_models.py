import unittest
from app.extensions import db
from app.models import Artist, Album, Lyric
from base import BaseTestCase


class ModelsTestCase(BaseTestCase):

    def test_artists_created(self):
        a1 = Artist('INTERPOL', self.user.get_id())
        a2 = Artist('BOOM BOOM KID', self.user.get_id())
        a3 = Artist('BECK', self.user.get_id())
        db.session.add_all([a1, a2, a3])
        db.session.commit()
        self.assertEqual(3, len(Artist.query.all()))

    def test_artist_deleted(self):
        a1 = Artist('INTERPOL', self.user.get_id())
        a2 = Artist('BOOM BOOM KID', self.user.get_id())
        a3 = Artist('BECK', self.user.get_id())
        db.session.add_all([a1, a2, a3])
        a1 = Artist.query.filter_by(name='INTERPOL').first()
        db.session.delete(a1)
        db.session.commit()
        self.assertEqual(2, len(Artist.query.all()))
        a1 = Artist.query.filter_by(name='INTERPOL').first()
        self.assertIsNone(a1)

    def test_artist_name_withoutspace(self):
        a1 = Artist('BOOM BOOM KID', self.user.get_id())
        self.assertEqual('BOOMBOOMKID', a1.get_name_without_spaces())

    def test_albums_created(self):
        a1 = Artist('ARTIST', self.user.get_id())
        db.session.add(a1)
        al1 = Album('album 1', self.user.get_id(), a1.get_id())
        al2 = Album('album 2', self.user.get_id(), a1.get_id())
        al3 = Album('album 3', self.user.get_id(), a1.get_id())
        db.session.add_all([al1, al2, al3])
        db.session.commit()
        self.assertEqual(3, len(Album.query.all()))

    def test_albums_deleted(self):
        a1 = Artist('ARTIST', self.user.get_id())
        a2 = Artist('THE ARTIST', self.user.get_id())
        db.session.add(a1)
        al1 = Album('album 1', self.user.get_id(), a1.get_id())
        al2 = Album('album 2', self.user.get_id(), a1.get_id())
        al3 = Album('album 3', self.user.get_id(), a1.get_id())
        db.session.add_all([al1, al2, al3])
        db.session.commit()
        al1 = Album.query.filter_by(name='album 1').first()
        db.session.delete(al1)
        db.session.commit()
        self.assertEqual(2, len(Album.query.all()))
        al1 = Album.query.filter_by(name='album 1').first()
        self.assertIsNone(al1)

    def test_album_name_withoutspace(self):
        a1 = Artist('ARTIST', self.user.get_id())
        db.session.add(a1)
        al1 = Album('album 1', self.user.get_id(), a1.get_id())
        self.assertEqual('ALBUM1', al1.get_name_without_spaces())

    def test_albums_are_deleted_when_artist_are_deleted(self):
        a1 = Artist('ARTIST', self.user.get_id())
        a2 = Artist('ARTIST2', self.user.get_id())
        db.session.add_all([a1, a2])
        db.session.commit()
        al1 = Album('album 1', self.user.get_id(), a1.get_id())
        al2 = Album('album 2', self.user.get_id(), a1.get_id())
        al3 = Album('album 3', self.user.get_id(), a1.get_id())
        al1b = Album('album 1_b', self.user.get_id(), a2.get_id())
        al2b = Album('album 2_b', self.user.get_id(), a2.get_id())
        al3b = Album('album 3_b', self.user.get_id(), a2.get_id())
        db.session.add_all([al1, al2, al3, al1b, al2b, al3b])
        db.session.commit()
        db.session.delete(a1)
        db.session.commit()
        al1 = Album.query.filter_by(name='album 1').first()
        self.assertIsNone(al1)
        al1b = Album.query.filter_by(name='album 1_b').first()
        self.assertIsNotNone(al1b)
        self.assertEqual(3, len(Album.query.all()))

    def test_get_artists_by_letter(self):
        a1 = Artist('ARTIST 1', self.user.get_id())
        a2 = Artist('ARTIST 2', self.user.get_id())
        db.session.add_all([a1, a2])
        db.session.commit()
        list_artists = [{'numb_w_s': u'ARTIST1', 'name': u'ARTIST 1'},
         {'numb_w_s': u'ARTIST2', 'name': u'ARTIST 2'}]
        artists = Artist.get_artists_by_letter('A')
        self.assertEqual(list_artists, artists)

if __name__ == '__main__':
    unittest.main()
