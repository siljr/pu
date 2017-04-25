from django.test import TestCase
from django.test import Client
from django.core.urlresolvers import reverse

from questions.models import Question
from django.contrib.auth.models import User


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
        test = self.client.post('/register/',
                         {'username': 'test', 'first_name': 'test', 'last_name': 'test',
                          'email': 'test@test.no', 'password1': 'password123',
                          'password2': 'password123'}, follow=True)
        # login with username test
        response = self.client.post('/login/', {'username': 'test', 'password': 'password123'}, follow=True)
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

    def setUp(self):
        # create user with username test
        self.client.post('/register/',
                         {'username': 'test', 'email': 'test@test.no', 'password1': 'test',
                          'password2': 'test'}, follow=True)
        # login with username test
        self.client.login(username="test", password="test")

        # make a question
        self.client.post('/questions/create_question/',
                         {'title': 'title', 'body': 'Ipsum lorem', 'tags': 'ipsum,test'})

    def create_object(self):
        return Question.objects.create(title = 'test', body = 'this is only a test', tags = 'valid,tags')

    def test_answers(self):
        # check if answer view is working
        response = self.client.get('/questions/1/', follow=True)

        self.assertEqual(response.status_code, 200)

    def test_tags(self):
        # check if tag views are working
        response = self.client.get('/questions/tag/test/')

        self.assertEqual(response.status_code, 200)

    def test_myquestions(self):
        # check if myquestions view is working
        response = self.client.get('/questions/myquestions/', follow=True)

        self.assertEqual(response.status_code, 200)

class TestSortAndPin(TestCase):
    def setUp(self):
        # create user with username test

        self.user = User.objects.create_superuser('admin', 'test@test.com', 'password123')

        # login with username test
        self.client.login(username="admin", password="password123")

        self.q = Question.objects.create(title="tittel", body="body test")
        Question.objects.create(title="tittel2", body="ipsum lorem")


    def test_pinned_questions(self):
        response = self.client.get("/questions/pinned/", follow=True)

        self.assertEqual(response.status_code, 200)

    def test_newest_sort(self):
        response = self.client.get("/questions/newest/", follow=True)

        self.assertEqual(response.status_code, 200)

    def test_oldest_sort(self):
        response = self.client.get("/questions/oldest/", follow=True)

        self.assertEqual(response.status_code, 200)

    def test_votes_sort(self):
        response = self.client.get("/questions/popular/", follow=True)

        self.assertEqual(response.status_code, 200)


