from django.test import TestCase
from django.test import Client
from django.core.urlresolvers import reverse

from questions.models import Question, Answer
from django.contrib.auth.models import User

class QuestionsCreateTestCase(TestCase):
    # setup a user
    def setUp(self):
        # create user with username test

        self.user = User.objects.create_superuser('admin', 'test@test.com', 'password123')
        #self.client.post('/register/',
                         #{'username': 'test','first_name': 'test','last_name': 'test',
                         # 'email': 'test@test.no', 'password1': 'password123',
                         # 'password2': 'password123'}, follow=True)

        # login with username test
        self.client.login(username="admin", password="password123")

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
        self.assertEqual(q1.user.__str__(), "admin")

    def test_user_vote_up(self):
        q1 = Question.objects.get(title="tittel")
        q1.upvote_question(self.user)
        self.assertEqual(q1.votes, 1)
        self.assertIn(self.user.__str__(), q1.user_votes)

    def test_user_vote_down(self):
        q1 = Question.objects.get(title="tittel2")
        q1.upvote_question(self.user)
        q1.downvote_question(self.user)
        self.assertEqual(q1.votes, 0)
        self.assertNotIn(self.user.__str__(), q1.user_votes)

    class QuestionsAnswerTestCase(TestCase):
        def setUp(self):
            # create user with username test

            self.user = User.objects.create_superuser('admin', 'test@test.com', 'password123')

            # login with username test
            self.client.login(username="admin", password="password123")

            self.q = Question.objects.create(title="tittel", body="body test")

            Answer.objects.create(body = "answer body", answer_to = self.q)

        def createQ(self, title, body):
            # Create question objects
            return Question.objects.create(title=title, body=body)

        def createA(self, body, answer_to):
            # Create answer object
            return Answer.objects.create(body=body, answer_to=answer_to)

        def test_answer(self):
            # test if answer model works
            a = Answer.objects.get(answer_to=self.q)

            self.assertEqual(a.body, "answer body")
            self.assertEqual(a.votes, 0)

        def test_answers(self):
            a = self.createA("second body", self.q)
            self.assertEqual(a.votes, 0)

            # check to see if there are two answer objects to question q
            qAnswers = Answer.objects.get(answer_to=self.q)
            self.assertEqual(len(qAnswers), 2)

        def test_answer_votes(self):
            # test up vote
            a = Answer.objects.get(answer_to=self.q)
            a.upvote_answer(self.user)

            self.assertEqual(a.votes, 1)
            self.assertIn(self.user.__str__(), a.user_votes_up)

            # test up vote regret
            a.upvote_regret(self.user)
            self.assertEqual(a.votes, 0)
            self.assertNotIn(self.user.__str__(), a.user_votes_up)

            # test down vote
            a.downvote_answer(self.user)
            self.assertEqual(a.votes, -1)
            self.assertIn(self.user.__str__(), a.user_votes_down)

            # test down vote regret
            a.downvote_regret(self.user)
            self.assertEqual(a.votes, 0)
            self.assertNotIn(self.user.__str__(), a.user_votes_down)






