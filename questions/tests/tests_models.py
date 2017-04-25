from django.test import TestCase
from django.test import Client
from django.core.urlresolvers import reverse

from questions.models import Question

class QuestionsCreateTestCase(TestCase):
    # setup a user
    def setUp(self):
        # create user with username test
        self.client.post('/register/',
                         {'username': 'test','first_name': 'test','last_name': 'test',
                          'email': 'test@test.no', 'password1': 'password123',
                          'password2': 'password123'}, follow=True)

        # login with username test
        self.client.login(username="test", password="password123")

        # Create question objects
        Question.objects.create(title = "tittel", body = "ipsum lorem")
        Question.objects.create(title="tittel2", body="ipsum lorem2")

    # tests if questions page is empty
    def test_questions_page(self):

        response = self.client.get(reverse('questions:index'), follow=True)

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