import unittest
from base import BaseTestCase
from app.extensions import db
from app.models import Artist, Album, Lyric
from datetime import datetime


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
        al1 = Album('album 1', datetime.now(), self.user.get_id(), a1.get_id())
        al2 = Album('album 2', datetime.now(), self.user.get_id(), a1.get_id())
        al3 = Album('album 3', datetime.now(), self.user.get_id(), a1.get_id())
        db.session.add_all([al1, al2, al3])
        db.session.commit()
        self.assertEqual(3, len(Album.query.all()))

    def test_albums_deleted(self):
        a1 = Artist('ARTIST', self.user.get_id())
        db.session.add(a1)
        al1 = Album('album 1', datetime.now(), self.user.get_id(), a1.get_id())
        al2 = Album('album 2', datetime.now(), self.user.get_id(), a1.get_id())
        al3 = Album('album 3', datetime.now(), self.user.get_id(), a1.get_id())
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
        al1 = Album('album 1', datetime.now(), self.user.get_id(), a1.get_id())
        self.assertEqual('ALBUM1', al1.get_name_without_spaces())

    def test_albums_are_deleted_when_artist_are_deleted(self):
        a1 = Artist('ARTIST', self.user.get_id())
        a2 = Artist('ARTIST2', self.user.get_id())
        db.session.add_all([a1, a2])
        db.session.commit()
        al1 = Album('album 1', datetime.now(), self.user.get_id(), a1.get_id())
        al2 = Album('album 2', datetime.now(), self.user.get_id(), a1.get_id())
        al3 = Album('album 3', datetime.now(), self.user.get_id(), a1.get_id())
        al1b = Album('al 1_b', datetime.now(), self.user.get_id(), a2.get_id())
        al2b = Album('al 2_b', datetime.now(), self.user.get_id(), a2.get_id())
        al3b = Album('al 3_b', datetime.now(), self.user.get_id(), a2.get_id())
        db.session.add_all([al1, al2, al3, al1b, al2b, al3b])
        db.session.commit()
        db.session.delete(a1)
        db.session.commit()
        al1 = Album.query.filter_by(name='album 1').first()
        self.assertIsNone(al1)
        al1b = Album.query.filter_by(name='al 1_b').first()
        self.assertIsNotNone(al1b)
        self.assertEqual(3, len(Album.query.all()))

    def test_get_artists_by_letter(self):
        a1 = Artist('ARTIST 1', self.user.get_id())
        a2 = Artist('ARTIST 2', self.user.get_id())
        db.session.add_all([a1, a2])
        db.session.commit()
        list_artists = [{'name_ws': u'ARTIST1', 'name': u'ARTIST 1'},
         {'name_ws': u'ARTIST2', 'name': u'ARTIST 2'}]
        artists = Artist.get_artists_by_letter('A')
        self.assertEqual(list_artists, artists)

    def test_get_album_year(self):
        a1 = Artist('ARTIST 1', self.user.get_id())
        date1 = datetime(2008, 1, 1, 00, 00, 00, 000000)
        al1 = Album('album 1', date1, self.user.get_id(), a1.get_id())
        self.assertEqual('2008', al1.get_year())
        date2 = datetime(2015, 1, 1, 00, 00, 00, 000000)
        al2 = Album('album 2', date2, self.user.get_id(), a1.get_id())
        self.assertEqual('2015', al2.get_year())

    def test_lyrics_created(self):
        lyric = '''nanananan nanananan batman
                   nanananan nanananan batman
                   nanananan nanananan batman
                   nanananan nanananan batman'''
        a1 = Artist('ARTIST', self.user.get_id())
        db.session.add(a1)
        al1 = Album('album 1', datetime.now(), self.user.get_id(), a1.get_id())
        db.session.add(al1)
        lyrics = []
        for i in range(1, 10):
            lyrics.append(
                Lyric('NANANA batman', lyric, self.user.get_id(), al1.get_id())
            )
        db.session.add_all(lyrics)
        db.session.commit()
        self.assertEqual(9, len(Lyric.query.all()))

    def test_lyrics_deleted(self):
        a1 = Artist('ARTIST', self.user.get_id())
        db.session.add(a1)
        al1 = Album('album 1', datetime.now(), self.user.get_id(), a1.get_id())
        db.session.add(al1)
        lyrics = []
        for i in range(1, 10):
            lyrics.append(
                Lyric(
                    'NANANA batman ' + str(i),
                    'NaN',
                    self.user.get_id(),
                    al1.get_id()
                )
            )
        db.session.add_all(lyrics)
        db.session.commit()
        self.assertEqual(9, len(Lyric.query.all()))
        l1 = Lyric.query.filter_by(name='NANANA batman 1').first()
        db.session.delete(l1)
        db.session.commit()
        self.assertEqual(8, len(Lyric.query.all()))

    def test_lyric_name_withoutspace(self):
        a1 = Artist('ARTIST', self.user.get_id())
        db.session.add(a1)
        al1 = Album('album 1', datetime.now(), self.user.get_id(), a1.get_id())
        db.session.add(al1)
        l1 = Lyric('A b', 'NaN', self.user.get_id(), al1.get_id())
        db.session.add(l1)
        self.assertEqual('AB', l1.get_name_without_spaces())

if __name__ == '__main__':
    unittest.main()
