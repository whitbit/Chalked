import server
from server import app
from unittest import TestCase
from model import connect_to_db, db, example_data


class MyAppUnitTestCase(TestCase):

    def test_allowed_file(self):

        self.assertTrue(server.allowed_file('file.png'))

class FlaskTestsBasic(TestCase):

    def setUp(self):

        self.client = app.test_client()
        app.config['TESTING'] = True

    def test_index(self):

        result = self.client.get('/')
        
        self.assertEqual(result.status_code, 200)


class FlaskTestsDatabase(TestCase):

    def setUp(self):

        self.client = app.test_client()
        app.config['TESTING'] = True

        connect_to_db(app, "postgresql:///testdb")
        db.create_all()
        example_data()
        # import pdb; pdb.set_trace()

    def tearDown(self):

        db.session.close()
        db.drop_all()


    def test_upload(self):

        pass

    def test_registeration(self):

        result = self.client.post('/register', data={ 'username': 'username',
                                                       'password': 'pw',
                                                       'level': 'int',
                                                       'email': 'email@gmail.com'},
                                               follow_redirects=True)


        self.assertIn('Successfully registered!', result.data)

    def test_already_registered(self):

        result = self.client.post('/register', data={ 'username': 'Bart'},
                                               follow_redirects=True)

        self.assertIn('Please login!', result.data)

    def test_valid_login(self):

        result = self.client.post('/login', data={ 'username': 'bart', 'password': 'kfneklwnf'},
                                            follow_redirects=True)

        self.assertIn('Welcome, bart', result.data)

    def test_invalid_login(self):

        result = self.client.post('/login', data={ 'username': 'bart', 'password': 'wrongpw'},
                                            follow_redirects=True)

        self.assertIn('Invalid password. Please try again!', result.data)



if __name__ == '__main__':
    import unittest

    unittest.main()