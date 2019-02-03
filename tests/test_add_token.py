from selenium.webdriver.common.keys import Keys
from selenium.webdriver.firefox.webdriver import WebDriver
from selenium.webdriver.support.wait import WebDriverWait
from django.test import LiveServerTestCase
from selenium import webdriver
from selenium.webdriver.firefox.webdriver import WebDriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from django.contrib.auth.models import User
from github_api.models import GitAuthentication, Repo


class TestAddToken(LiveServerTestCase):

    def setUp(self):
        self.selenium = webdriver.Firefox()
        self.username = 'user1'
        super(TestAddToken, self).setUp()

        self.user = User.objects.create_user(username='user2',
                                             password='Admin#99')

        self.token = '05f597ccd35846a3477744e3e7428087545da48f'[::-1]
        self.username = 'user2'
        self.password = 'Admin#99'

        self.selenium.get(self.live_server_url + '/login')
        self.selenium.find_element_by_id("id_username").send_keys(self.username)
        self.selenium.find_element_by_id("id_password").send_keys(self.password)
        self.selenium.find_element_by_id('login_button').click()

    def test_add_token_successfully(self):
        self.selenium.get(self.live_server_url)
        self.selenium.find_element_by_id('access_token_button').click()

        self.selenium.find_element_by_id("id_access_token").send_keys(self.token)
        self.selenium.find_element_by_id('token_button').click()

        try:
            element = WebDriverWait(self.selenium, 10).until(
                EC.presence_of_element_located((By.CLASS_NAME, "alert.alert-success")))
            self.assertEqual('Your token has been successfully added', element.text)
        finally:
            self.selenium.quit()

    def test_add_wrong_token(self):
        self.token = 'blebleble'
        self.selenium.get(self.live_server_url)
        self.selenium.find_element_by_id('access_token_button').click()

        self.selenium.find_element_by_id("id_access_token").send_keys(self.token)
        self.selenium.find_element_by_id('token_button').click()

        try:
            element = WebDriverWait(self.selenium, 10).until(
                EC.presence_of_element_located((By.CLASS_NAME, "alert.alert-danger")))
            self.assertEqual('Wrong access token!', element.text)
        finally:
            self.selenium.quit()
