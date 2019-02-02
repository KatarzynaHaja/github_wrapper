from django.test import LiveServerTestCase
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from django.contrib.auth.models import User
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By

from github_api.models import GitAuthentication, Repo

class TestAddNewRepo(LiveServerTestCase):

    def setUp(self):
        self.selenium = webdriver.Firefox()
        super(TestAddNewRepo, self).setUp()
        self.user = User.objects.create_user(username='user2',
                                             password='Admin#99')

        self.git = GitAuthentication.objects.create(access_token='05f597ccd35846a3477744e3e7428087545da48f'[::-1])
        self.git.user.add(self.user)
        self.username= 'user2'
        self.password='Admin#99'
        self.selenium.get(self.live_server_url + '/login')
        self.selenium.find_element_by_id("id_username").send_keys(self.username)
        self.selenium.find_element_by_id("id_password").send_keys(self.password)
        self.selenium.find_element_by_id('login_button').click()

    def test_add_new_repo_correctly(self):
        self.repo_name = 'KatarzynaHaja/Test'
        self.selenium.get(self.live_server_url + '/add_new_repo')
        self.selenium.find_element_by_id("id_name").send_keys(self.repo_name)
        self.selenium.find_element_by_id('add_repo_button').click()

        try:
            element = WebDriverWait(self.selenium, 10).until(
                EC.presence_of_element_located((By.CLASS_NAME, "alert.alert-success")))
            self.assertEqual('Repo has been successfully added', element.text)
        finally:
            self.selenium.quit()

    def test_add_new_repo_already_exist(self):
        Repo.objects.create(name='KatarzynaHaja/Test')
        self.repo_name = 'KatarzynaHaja/Test'
        self.selenium.get(self.live_server_url + '/add_new_repo')
        self.selenium.find_element_by_id("id_name").send_keys(self.repo_name)
        self.selenium.find_element_by_id('add_repo_button').click()

        try:
            element = WebDriverWait(self.selenium, 10).until(
                EC.presence_of_element_located((By.CLASS_NAME, "alert.alert-danger")))
            self.assertEqual('This repo has already been in your favourites', element.text)
        finally:
            self.selenium.quit()

    def test_add_new_repo_does_not_exist(self):
        self.repo_name = 'blebleblble'
        self.selenium.get(self.live_server_url + '/add_new_repo')
        self.selenium.find_element_by_id("id_name").send_keys(self.repo_name)
        self.selenium.find_element_by_id('add_repo_button').click()

        try:
            element = WebDriverWait(self.selenium, 10).until(
                EC.presence_of_element_located((By.CLASS_NAME, "alert.alert-danger")))
            self.assertEqual("This repo doesn't exist", element.text)
        finally:
            self.selenium.quit()

    def tearDown(self):
        self.selenium.quit()
