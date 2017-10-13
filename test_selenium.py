from selenium import webdriver
from unittest import TestCase

class TestRouteSearch(TestCase):

    def setUp(self):
        self.browser = webdriver.Firefox(executable_path="/Users/whit/src/project/geckodriver")


    def tearDown(self):
        self.browser.quit()

    def test_title(self):
        self.browser.get('http://localhost:5000/')
        self.assertEqual(self.browser.title, 'WELCOME')

    def test_login(self):
        self.browser.get('http://localhost:5000/')
        username = self.browser.find_element_by_id('username')
        username.send_keys('whitney')
        password = self.browser.find_element_by_id('password')
        password.send_keys('123')

        btn = self.browser.find_element_by_id('login')
        btn.click()

        self.assertEqual(self.browser.title, 'Dashboard')


    def test_dashboard(self):

        self.browser.get('http://localhost:5000/')
        username = self.browser.find_element_by_id('username')
        username.send_keys('whitney')
        password = self.browser.find_element_by_id('password')
        password.send_keys('123')

        btn = self.browser.find_element_by_id('login')
        btn.click()

        self.browser.get('http://localhost:5000/dashboard')
        
        self.assertEqual(self.browser.title, 'Dashboard')

        log_btn = self.browser.find_element_by_id('log-climb-btn')
        log_btn.click()

        state = self.browser.find_element_by_id('state')
        state.selectByVisibleText('California')
        


if __name__ == '__main__':
    import unittest
    unittest.main()