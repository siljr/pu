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
    # setup a user
    def setUp(self):
        # create user with username test
        self.client.post('/register/',
                         {'username': 'test', 'email': 'test@test.no', 'password1': 'test',
                          'password2': 'test'}, follow=True)

        # login with username test
        self.client.login(username="test", password="test")

        # Create question objects
        Question.objects.create(title = "tittel", body = "ipsum lorem")
        Question.objects.create(title="tittel2", body="ipsum lorem2")

    # tests if questions page is empty
    def test_questions_page(self):

        response = self.client.get(reverse('questions:index'), follow=True)

        # print(response.context["questions"])

        # check if index.html is in the list of used templates
        self.assertTemplateUsed(response, 'index.html')

        # get all titles
        all = Question.objects.all()
        allQ = [x.title for x in all]

        # see if the right title is in the object list
        self.assertIn("tittel", allQ)

        # see if the number of Question objects is correct
        self.assertEqual(len(allQ), 2)

    def test_add_question(self):
        # tests to see if title and body is correct
        q1 = Question.objects.get(title = "tittel")

        self.assertEqual(q1.body, "ipsum lorem")
        q2 = Question.objects.get(title = "tittel2")
        self.assertEqual(q2.body, "ipsum lorem2")

    def test_question_object(self):
        q1 = Question.objects.get(title = "tittel")
        self.assertEqual(q1.user.__str__(), "test")
