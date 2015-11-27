from base import BaseTestCase


class FlaskTestCase(BaseTestCase):

    def test_index(self):
        response = self.client.get('/login', content_type='html/text')
        self.assertEqual(response.status_code, 200)