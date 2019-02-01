from django.test import LiveServerTestCase
from selenium import webdriver
from selenium.webdriver.common.keys import Keys


class TestLogIn(LiveServerTestCase):

    def setUp(self):
        self.selenium = webdriver.Firefox()
        super(TestLogIn, self).setUp()


    def tearDown(self):
        self.selenium.quit()
