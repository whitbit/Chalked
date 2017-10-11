import server
from unittest import TestCase
from model import connect_to_db, db, example_data


class MyAppUnitTestCase(TestCase):

    def test_allowed_file(self):

        self.assertTrue(server.allowed_file('file.png'))

class FlaskTestsBasic(TestCase):

    def setUp(self):

        self.client = server.app.test_client()
        server.app.config['TESTING'] = True

    def test_index(self):

        result = self.client.get('/')
        
        self.assertEqual(result.status_code, 200)


class FlaskTestsDatabase(TestCase):

    def setUp(self):

        self.client = server.app.test_client()
        server.app.config['TESTING'] = True

        connect_to_db(app, "postgresql:///testdb")
        db.create_all()
        example_data()

    def tearDown(self):

        db.session.close()
        db.drop_all()


    def test_upload(self):

        pass

    def test_register_form(self):

        result = client.post('/register', data={ 'username': 'username',
                                                 'password': 'pw',
                                                 'level': 'int',
                                                 'email': 'email@gmail.com'})

        self.assertIn('Successfully registered!', result.data)


if __name__ == '__main__':
    import unittest

    unittest.main()