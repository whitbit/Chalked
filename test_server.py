import server
from server import app
from unittest import TestCase
from model import connect_to_db, db, example_data, UserLog
from flask import session
from selenium import webdriver
from datetime import datetime


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
                                  data={ 'username': 'Bart',
                                         'password': 'kfneklwnf' },
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


    def test_not_registered(self):

        result = self.client.post('/login', 
                                  data={ 'username': 'annie'},
                                  follow_redirects=True)

        self.assertIn('Please register first', result.data)

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
                                     'date': '2014-11-08 23:56:52',
                                     'photo': 'C:\\fakepath\\photo.jpg'})


        self.assertIsNotNone(UserLog.query.filter_by(notes='check').first())

    def test_user_log_json(self):
        """Tests that correct json info is returned, such as coordinates, 
        route names, links for user in session."""

        with self.client as c:
            with c.session_transaction() as sess:
                sess['user_id'] = 3

        result = self.client.get('/user-info.json')

        self.assertIn('39.95', result.data)
        self.assertNotIn('39.9315', result.data)
        self.assertIn('North Face', result.data)
        self.assertIn('link2', result.data)

    def test_user_chart_info(self):
        """Tests that correct json info is sent to chart.js"""

        with self.client as c:
            with c.session_transaction() as sess:
                sess['user_id'] = 3

        result = self.client.get('/user-chart.json')

        self.assertIn('V3', result.data)
        self.assertIn('rgba(193,46,12,0.8)', result.data)

    def test_upload_route(self):
        """Tests file upload route."""

        pass

    def test_route_search(self):
        """Tests route search query."""

        with self.client as c:
            with c.session_transaction() as sess:
                sess['user_id'] = 3

        result = self.client.get('/search.json', data={ 'state': 'Colorado'} )
        
        self.assertIn('Colorado', result.data)

    def test_log_update(self):
        """Tests route that updates userlog entry."""

        with self.client as c:
            with c.session_transaction() as sess:
                sess['user_id'] = 3

        result = self.client.post('/update-log.json', data={ 'review_id': 1,
                                                             'notes': 'Updated!',
                                                             'completed': True,
                                                             'rating': 5,
                                                             'date': datetime.today() 
                                                            })
        
        self.assertEqual(result.status_code, 200)

    def test_log_delete(self):

        result = self.client.post('/delete-log.json', data= { 'review_id': 4} )

        self.assertEqual(result.status_code, 200)
        self.assertIsNone(UserLog.query.filter_by(review_id=4).first())


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

    def test_user_map(self):

        result = self.client.get('/user-map')

        self.assertIn('Places I\'ve climbed', result.data)


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