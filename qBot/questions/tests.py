from django.test import TestCase
from django.test import Client
from django.core.urlresolvers import reverse
from django.contrib.auth.models import User

from questions.models import Question



class QuestionCreateTestCase(TestCase):
    # sets up a "dummy database"
    def setUp(self):
        User.objects.create(username="andrroy")


    def test_register_question_view(self):
        client = Client()
        # sends a request with these data
        response = client.post(reverse('create_question'), {
            'user': 'andrroy',
            'title': 'dette er noe',
            'body': 'Dette er teksten',
        })
        # 200 = evrything ok
        assert response.status_code == 200
        questions = Question.objects.all()
        # expects only one database entry - because we sent only one
        assert len(questions) == 1


        # to see if something is equal to, use self.assertEqual(cat.speak(), 'The cat says "meow"')