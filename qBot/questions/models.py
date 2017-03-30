from __future__ import unicode_literals

from django.contrib.auth.models import User
from django.db import models
from django.utils import timezone
from django.conf import settings
import json



# making the question model to contain theese things
class Question(models.Model):
    title = models.CharField(max_length=128)
    body = models.TextField()
    created_at = models.DateTimeField(null=True, blank=True)
    # sets a connection to a user
    # user = models.ForeignKey(User, related_name='is_made_by')
    user = models.ForeignKey(settings.AUTH_USER_MODEL, default=1, related_name='is_made_by')
    votes = models.IntegerField(default = 0)
    user_votes = models.TextField(editable=True, default='[]')  # JSON-text, works as a list of user in string-format
    pinned_by = models.ManyToManyField(User)

    # adds a timestamp to the question posted
    def save(self, *args, **kwargs):
        if self.created_at is None:
            self.created_at = timezone.now()
        super().save(*args, **kwargs)

    def __str__(self):
        return str(self.id) + '. ' + self.title
    # upvotes the question
    def upvote_question(self, user):
        self.votes += 1
        jsonDec = json.decoder.JSONDecoder()
        liste = jsonDec.decode(self.user_votes) #decodes the JSON-text to a list
        liste.append(str(user))                 #appends the user
        self.user_votes = json.dumps(liste)     #encodes the list to JSON-string, user_votes
        self.save()

    # downvotes the question
    def downvote_question(self, user):
        self.votes -= 1
        user_list = self.create_json_list(self.user_votes)  #opposit as upvote (check above)
        user_list.remove(str(user))
        self.user_votes = self.create_json_str(user_list)
        self.save()


    # Checks if user is in user_votes
    def is_in_user_votes(self, user):
        user_list = self.create_json_list(self.user_votes)
        if str(user) in user_list:
            return True
        else:
            return False


    # creates a list from the JSON-text format
    def create_json_list(self, input):
        jsonDec = json.decoder.JSONDecoder()
        return jsonDec.decode(input)


    # creates a JSON-text from a list
    def create_json_str(self, input):
        return json.dumps(input)


class Answer(models.Model):
    body = models.TextField()
    created_at = models.DateTimeField(null=True, blank=True)
    user = models.ForeignKey(settings.AUTH_USER_MODEL, default=1)
    # votes = models.IntegerField(default=0)
    # voters = models.ManyToManyField(User,related_name='voted_for_question')
    answer_to = models.ForeignKey(Question, related_name='answer_to')

    # adds a timestamp to the question posted
    def save(self, *args, **kwargs):
        if self.created_at is None:
            self.created_at = timezone.now()
        super().save(*args, **kwargs)


class UserVotes(models.Model):
    user = models.ForeignKey(User, related_name="user_votes")
    question = models.ForeignKey(Question, related_name="question_votes")
    vote_type = models.CharField(max_length=16)

    class Meta:
        unique_together = ('user', 'question', 'vote_type')



#<a href="/questions/vote?question={{ question.id }}&votetype=up" id ="approve_button" type="button" {% if active_button == "True"%} class="btn btn-default btn- active" {% else%} class="btn btn-default btn" {% endif %} >