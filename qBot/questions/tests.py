from django.test import TestCase
from django.test import Client
from django.core.urlresolvers import reverse

from questions.models import Question


class QuestionLoginTestCase(TestCase):
    # tests to see if you can enter Questions page without loging in.
    def test_question_when_not_logged_in(self):
        response = self.client.post('/questions/', follow=True)
        self.assertNotEqual(response.request['PATH_INFO'], '/questions/')
        self.assertEqual(response.status_code, 200)

    # tests to see if redirection to login page is succesfull
    def test_login_view(self):
        response = self.client.get('/login/', follow=True)
        self.assertEqual(response.status_code, 200)

    # tests to see if successful login redirects you to /questions/ page
    def test_successful_login(self):
        # create user with username test
        self.client.post('/register/',
                         {'username': 'test', 'email': 'test@test.no', 'password1': 'test',
                          'password2': 'test'}, follow=True)

        # login with username test
        response = self.client.post('/login/', {'username': 'test', 'password': 'test'}, follow=True)
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.request['PATH_INFO'], '/questions/')

    # tests if login attempt is unsuccessful
    def test_unsuccessful_login(self):
        # create user with username test
        self.client.post('/register/',
                         {'username': 'test', 'email': 'test@test.no', 'password1': 'test',
                          'password2': 'test'}, follow=True)

        # login with username test
        response = self.client.post('/login/', {'username': 'test', 'password': 'feil'}, follow=True)
        self.assertEqual(response.status_code, 200)
        self.assertNotEqual(response.request['PATH_INFO'], '/questions/')

    # tests logout attempt
    def test_logout(self):
        # create user with username test
        self.client.post('/register/',
                         {'username': 'test', 'email': 'test@test.no', 'password1': 'test',
                          'password2': 'test'}, follow=True)
        # login with username test
        self.client.login(username="test", password="test")

        # logout
        response = self.client.post('/logout/', follow=True)

        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.request["PATH_INFO"], "/login/")


class QuestionsCreateTestCase(TestCase):
    # tests if questions page is empty
    def test_empty_questions_page(self):
        # create user with username test
        self.client.post('/register/',
                         {'username': 'test', 'email': 'test@test.no', 'password1': 'test',
                          'password2': 'test'}, follow=True)

        # login with username test
        self.client.login(username="test", password="test")
        response = self.client.get(reverse('questions:index'), follow=True)

        #print(response.context["questions"])
        t = response.templates
