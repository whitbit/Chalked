import server
from server import app
from unittest import TestCase
from model import connect_to_db, db, example_data, UserLog
from flask import session


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
        self.assertIn('Welcome!', result.data)


class FlaskTestsDatabase(TestCase):

    def setUp(self):

        self.client = app.test_client()
        app.config['TESTING'] = True

        connect_to_db(app, "postgresql:///testdb")
        db.create_all()
        example_data()

    def tearDown(self):

        db.session.close()
        db.drop_all()


    def test_upload(self):

        pass

    def test_new_registeration(self):

        result = self.client.post('/register', 
                                  data={ 'username': 'username',
                                         'password': 'pw',
                                         'level': 'int',
                                         'email': 'email@gmail.com'},
                                  follow_redirects=True)


        self.assertIn('Successfully registered!', result.data)

    def test_already_registered(self):

        result = self.client.post('/register', 
                                  data={ 'username': 'Bart' },
                                  follow_redirects=True)

        self.assertIn('Please login!', result.data)

    def test_valid_login(self):
        
        with self.client as c:
            result = c.post('/login', 
                            data={ 'username': 'bart', 'password': 'kfneklwnf'},
                            follow_redirects=True)

            self.assertEqual(session['username'], 'bart')
            self.assertIn('Welcome, bart', result.data)


    def test_invalid_login(self):

        result = self.client.post('/login', 
                                  data={ 'username': 'bart', 'password': 'wrongpw'},
                                  follow_redirects=True)

        self.assertIn('Invalid password. Please try again!', result.data)

    def test_new_userlog(self):
        """Tests that log form info is sent to logs table in database"""

        with self.client as c:
            with c.session_transaction() as sess:
                sess['user_id'] = 3
            
            self.client.post('/log-climb.json',
                              data={ 'route_id': 1,
                                     'complete': True,
                                     'notes': 'check',
                                     'rating': 5,
                                     'date': '2014-11-08 23:56:52'})


        self.assertIsNotNone(UserLog.query.filter_by(notes='check').first())



class FlaskTestsLoggedIn(TestCase):
    """Tests if user logged in session."""

    def setUp(self):

        app.config['TESTING'] = True
        app.config['SECRET_KEY'] = 'ABC'
        self.client = app.test_client()

        with self.client as c:
            with c.session_transaction() as sess:
                sess['username'] = 'bart'


    def test_dashboard(self):

        result = self.client.get('/dashboard')

        self.assertIn('Welcome, bart!', result.data)


class FlaskTestsLoggedOut(TestCase):
    """Tests if user logged in session."""

    def setUp(self):

        app.config['TESTING'] = True
        self.client = app.test_client()

    def test_dashboard(self):

        result = self.client.get('/dashboard', follow_redirects=True)

        self.assertNotIn('V-points', result.data)
        self.assertIn('Please log in', result.data)

    def test_logout(self):

        with self.client as c:
            with c.session_transaction() as sess:
                sess['username'] = 'jenny'
                sess['user_id'] = 2

            result = self.client.post('/logout', follow_redirects=True)

            self.assertNotIn('username', session)
            self.assertIn('logged out successfully', result.data)

# /upload.json, /uploads/filename, /requireslogin, /map


if __name__ == '__main__':
    import unittest

    unittest.main()