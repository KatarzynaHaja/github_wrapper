from django.test import LiveServerTestCase
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from django.contrib.auth.models import User
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By

class TestLogIn(LiveServerTestCase):

    def setUp(self):
        self.selenium = webdriver.Firefox()
        super(TestLogIn, self).setUp()
        self.user = User.objects.create_user(username='user2',
                                             password='Admin#99')

    def test_correct_credentials(self):
        self.username = 'user2'
        self.password = 'Admin#99'
        self.selenium.get(self.live_server_url + '/login')
        self.selenium.find_element_by_id("id_username").send_keys(self.username)
        self.selenium.find_element_by_id("id_password").send_keys(self.password)
        self.selenium.find_element_by_id('login_button').click()

        try:
            element = WebDriverWait(self.selenium, 10).until(
                EC.presence_of_element_located((By.ID, "access_token_alert")))
        finally:
            self.selenium.quit()

    def test_bad_credentials(self):
        self.username = 'user2'
        self.password = 'Admi'
        self.selenium.get(self.live_server_url + '/login')
        self.selenium.find_element_by_id("id_username").send_keys(self.username)
        self.selenium.find_element_by_id("id_password").send_keys(self.password)
        self.selenium.find_element_by_id('login_button').click()

        try:
            element = WebDriverWait(self.selenium, 10).until(
                EC.presence_of_element_located((By.CLASS_NAME, "alert.alert-block.alert-danger")))
        finally:
            self.selenium.quit()



    def tearDown(self):
        self.selenium.quit()
