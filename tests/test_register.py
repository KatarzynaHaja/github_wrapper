from django.test import LiveServerTestCase
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.firefox.webdriver import WebDriver
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.firefox.webdriver import WebDriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from django.contrib.auth.models import User


class TestRegister(LiveServerTestCase):

    def setUp(self):
        self.selenium = webdriver.Firefox()
        self.username = 'user1'
        super(TestRegister, self).setUp()


    def test_correct_registration(self):
        self.username = 'user2'
        self.password1 = 'Admin#99'
        self.password2 = 'Admin#99'
        self.selenium.get(self.live_server_url + '/register/')
        self.selenium.find_element_by_id("id_username").send_keys(self.username)
        self.selenium.find_element_by_id("id_password1").send_keys(self.password1)
        self.selenium.find_element_by_id("id_password2").send_keys(self.password2)
        self.selenium.find_element_by_id('sign_up_button').click()

        try:
            element = WebDriverWait(self.selenium, 10).until(
                EC.presence_of_element_located((By.ID, "access_token_alert")))
        finally:
            self.selenium.quit()

    def test_not_the_same_password(self):
        self.username = 'user2'
        self.password1 = 'Admin#99'
        self.password2 = 'Admin#9'
        self.selenium.get(self.live_server_url + '/register/')
        self.selenium.find_element_by_id("id_username").send_keys(self.username)
        self.selenium.find_element_by_id("id_password1").send_keys(self.password1)
        self.selenium.find_element_by_id("id_password2").send_keys(self.password2)
        self.selenium.find_element_by_id('sign_up_button').click()

        try:
            element = WebDriverWait(self.selenium, 10).until(
                EC.presence_of_element_located((By.ID, "error_1_id_password2")))
        finally:
            self.selenium.quit()

    def test_user_already_exist(self):
        self.user = User.objects.create_user(username='user2',
                                             password='Admin#99')
        self.username = 'user2'
        self.password1 = 'Admin#99'
        self.password2 = 'Admin#99'
        self.selenium.get(self.live_server_url+'/register')
        self.selenium.find_element_by_id("id_username").send_keys(self.username)
        self.selenium.find_element_by_id("id_password1").send_keys(self.password1)
        self.selenium.find_element_by_id("id_password2").send_keys(self.password2)
        self.selenium.find_element_by_id('sign_up_button').click()

        try:
            element = WebDriverWait(self.selenium, 10).until(
                EC.presence_of_element_located((By.ID, "error_1_id_username")))
        finally:
            self.selenium.quit()


    def tearDown(self):

        self.selenium.quit()
        super(TestRegister, self).tearDown()
