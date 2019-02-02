from django.test import LiveServerTestCase
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.firefox.webdriver import WebDriver
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.firefox.webdriver import WebDriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC


class TestRegister(LiveServerTestCase):

    def setUp(self):
        self.selenium = webdriver.Firefox()
        super(TestRegister, self).setUp()
        self.username = 'aasasas'
        self.password1 ='Admin#99'
        self.password2 ='Admin#99'

    def test_correct_registration(self):
        self.selenium.get('http://127.0.0.1:8000/register/')
        self.selenium.find_element_by_id("id_username").send_keys(self.username)
        self.selenium.find_element_by_id("id_password1").send_keys(self.password1)
        self.selenium.find_element_by_id("id_password2").send_keys(self.password2)
        self.selenium.find_element_by_id('sign_up_button').click()

        try:
            element = WebDriverWait(self.selenium, 10).until(
                EC.presence_of_element_located((By.ID, "access_token_alert")))
        finally:
            self.selenium.quit()

        # self.assertEqual(element.text, 'Add your personal Github token . It allows you to use all functionalities.' )





    def tearDown(self):

        self.selenium.quit()
