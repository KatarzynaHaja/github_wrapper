from django.test import LiveServerTestCase
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.firefox.webdriver import WebDriver
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.firefox.webdriver import WebDriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from django.contrib.auth.models import User
from github_api.models import GitAuthentication, Repo


class TestAddNewIssue(LiveServerTestCase):

    def setUp(self):
        self.selenium = webdriver.Firefox()
        self.username = 'user1'
        super(TestAddNewIssue, self).setUp()

        self.user = User.objects.create_user(username='user2',
                                             password='Admin#99')

        self.git = GitAuthentication.objects.create(access_token='05f597ccd35846a3477744e3e7428087545da48f'[::-1])
        self.git.user.add(self.user)
        self.username = 'user2'
        self.password = 'Admin#99'
        self.selenium.get(self.live_server_url + '/login')
        self.selenium.find_element_by_id("id_username").send_keys(self.username)
        self.selenium.find_element_by_id("id_password").send_keys(self.password)
        self.selenium.find_element_by_id('login_button').click()

        self.repo_name = 'KatarzynaHaja/Test'
        self.selenium.get(self.live_server_url + '/add_new_repo')
        self.selenium.find_element_by_id("id_name").send_keys(self.repo_name)
        self.selenium.find_element_by_id('add_repo_button').click()

        self.title = 'Test11'
        self.body = 'This is test issue'
        self.label = 'Done'
        self.milestone = 'New'

    def test_add_new_issue_without_milestone(self):
        self.selenium.get(self.live_server_url + '/repo/{}/add_issue/'.format(
            Repo.objects.filter(name='KatarzynaHaja/Test').first().id))
        self.selenium.find_element_by_id("id_title").send_keys(self.title)
        self.selenium.find_element_by_id("id_body").send_keys(self.body)
        self.selenium.find_element_by_id("id_label").send_keys(self.label)
        self.selenium.find_element_by_id('add_issue_button').click()

        try:
            element = WebDriverWait(self.selenium, 10).until(
                EC.presence_of_element_located((By.CLASS_NAME, "alert.alert-success")))
            self.assertEqual('Your issue has been successfully added', element.text)
        finally:
            self.selenium.quit()

    def test_add_new_issue_with_milestone(self):
        self.selenium.get(self.live_server_url + '/repo/{}/add_issue/'.format(
            Repo.objects.filter(name='KatarzynaHaja/Test').first().id))
        self.selenium.find_element_by_id("id_title").send_keys(self.title)
        self.selenium.find_element_by_id("id_body").send_keys(self.body)
        self.selenium.find_element_by_id("id_label").send_keys(self.label)
        self.selenium.find_element_by_id('id_milestone').send_keys(self.milestone)
        self.selenium.find_element_by_id('add_issue_button').click()

        try:
            element = WebDriverWait(self.selenium, 10).until(
                EC.presence_of_element_located((By.CLASS_NAME, "alert.alert-success")))
            self.assertEqual('Your issue has been successfully added', element.text)
        finally:
            self.selenium.quit()

    def tearDown(self):
        self.selenium.quit()
