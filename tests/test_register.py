from django.test import LiveServerTestCase
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.firefox.webdriver import WebDriver
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.firefox.webdriver import WebDriver


class TestRegister(LiveServerTestCase):

    def setUp(self):
        self.selenium = webdriver.Firefox()
        super(TestRegister, self).setUp()
        self.username = 'user'
        self.password1 ='Admin#99'
        self.password2 ='Admin#99'

    def test_correct_registration(self):
        self.selenium.get('http://127.0.0.1:8000/register/')
        self.selenium.find_element_by_id("id_username").send_keys(self.username)
        self.selenium.find_element_by_id("id_password1").send_keys(self.password1)
        self.selenium.find_element_by_id("id_password2").send_keys(self.password2)
        self.selenium.find_element_by_id('sign_up_button').click()

        WebDriverWait(self.selenium, 10)

        self.assertEqual('http://127.0.0.1:8000', 'http://127.0.0.1:8000' )



    def tearDown(self):

        self.selenium.quit()
