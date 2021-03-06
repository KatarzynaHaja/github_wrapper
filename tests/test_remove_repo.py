from selenium.webdriver.support.wait import WebDriverWait
from django.test import LiveServerTestCase
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from django.contrib.auth.models import User
from github_api.models import GitAuthentication, Repo, Issue


class TestRepo(LiveServerTestCase):

    def setUp(self):
        self.selenium = webdriver.Firefox()
        super(TestRepo, self).setUp()

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

    def test_remove_repo(self):
        self.selenium.get(
            self.live_server_url + '/remove_repo/{}/'.format(Repo.objects.filter(name=self.repo_name).first().id))
        if_repo = Repo.objects.filter(name=self.repo_name).exists()
        self.assertFalse(if_repo)

    def tearDown(self):
        self.selenium.quit()
