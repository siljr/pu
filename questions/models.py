from __future__ import unicode_literals

from django.contrib.auth.models import User
from django.db import models
from django.utils import timezone
from django.conf import settings
import json

#for tags
from taggit.managers import TaggableManager
from django.template.defaultfilters import slugify

# The question class containing multiple data and methods
class Question(models.Model):

    # Basic and essential data
    title = models.CharField(max_length=128)
    body = models.TextField()
    created_at = models.DateTimeField(null=True, blank=True)  # is being set at save method

    # Connection to the user making the question
    user = models.ForeignKey(settings.AUTH_USER_MODEL, default=1, related_name='question_made_by')

    # Data for votes, including voters and vote counter
    user_votes = models.TextField(editable=True, default='[]')  # JSON-text, works as a list of user in string-format
    votes = models.IntegerField(default = 0)
    button_list = models.ManyToManyField(User, related_name="active_button")  # Upvote button.

    # Field for Users who has marked this as one of their favourite questions
    pinned_by = models.ManyToManyField(User, related_name="pinned_py")

    # The tags
    tags = TaggableManager(blank=True)  # Tags are optional

    # Adds a timestamp to the question posted
    def save(self, *args, **kwargs):
        if self.created_at is None:
            self.created_at = timezone.now()
        super().save(*args, **kwargs)

    # String method used e.g. in admin panel
    def __str__(self):
        return str(self.id) + '. ' + self.title

    # Upvotes the question
    def upvote_question(self, user):
        self.votes += 1
        user_list = self.create_json_list(self.user_votes)     # decodes the JSON-text to a list
        user_list.append(str(user))                             # appends the user
        self.user_votes = self.create_json_str(user_list)        # encodes the list to JSON-string, user_votes
        self.save()

    # Downvotes the question
    def downvote_question(self, user):
        self.votes -= 1
        user_list = self.create_json_list(self.user_votes)
        user_list.remove(str(user))                             # same as of upvote_question(), only remove instead of append (check above)
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

# The answer class containing multiple data and methods
class Answer(models.Model):

    # Basic and essential data
    body = models.TextField()
    created_at = models.DateTimeField(null=True, blank=True)

    # Connection to the user giving the answer
    user = models.ForeignKey(settings.AUTH_USER_MODEL, default=1, related_name='answer_made_by')

    # Connection to the question being answered
    answer_to = models.ForeignKey(Question, related_name='answer_to')

    # Vote counter and fields for voting up and down
    votes = models.IntegerField(default=0)
    user_votes_up = models.TextField(editable=True,default='[]')  # JSON-text, works as a list of user in string-format 
    user_votes_down = models.TextField(editable=True, default='[]')# JSON-text, works as a list of user in string-format 

    # Lists to see if the user has voted for an answer (active button graphic)
    button_up = models.ManyToManyField(User, related_name= 'up_button')
    button_down = models.ManyToManyField(User, related_name= 'down_button')

    # Adds a timestamp to the answer posted
    def save(self, *args, **kwargs):

        if self.created_at is None:
            self.created_at = timezone.now()
        super().save(*args, **kwargs)

    # Upvote an answer. Similar to upvote_question, but some more logic.
    def upvote_answer(self, user):

        user_list_up = self.create_json_list(self.user_votes_up)  # decodes the JSON-text to a list 
        user_list_up.append(str(user))  # appends the user 
        self.user_votes_up = self.create_json_str(user_list_up)     # encodes the list to JSON-string

        if self.is_in_user_votes_down(user):                                #removes user from downvote_list if user upvotes.
            user_list_down = self.create_json_list(self.user_votes_down)    #Gives 2 points if user has already downvoted question, and 1 point if not.
            user_list_down.remove(str(user))
            self.user_votes_down = self.create_json_str(user_list_down)
            self.votes += 2
        else:
            self.votes += 1
        self.save()

    def downvote_answer(self, user):

        user_list_down = self.create_json_list(self.user_votes_down)  # opposite of upvote (check above) 
        user_list_down.append(str(user))

        if self.is_in_user_votes_up(user):
            user_list_up = self.create_json_list(self.user_votes_up)
            user_list_up.remove(str(user))
            self.user_votes_up = self.create_json_str(user_list_up)
            self.votes -= 2  # Subtracting 2 as the user already had voted up
        else:
            self.votes -= 1

        self.user_votes_down = self.create_json_str(user_list_down)
        self.save()

    # Gives answer a point if user has already downvoted, but regrets this, and presses the downvote button one more time.
    def upvote_regret(self, user):

        self.votes += 1
        user_list_down = self.create_json_list(self.user_votes_down)
        user_list_down.remove(str(user))
        self.user_votes_down = self.create_json_str(user_list_down)
        self.save()

    # Same as above, only opposit. Substracts a point if you regret an upvote.
    def downvote_regret(self, user):

        self.votes -= 1
        user_list_up = self.create_json_list(self.user_votes_up)
        user_list_up.remove(str(user))
        self.user_votes_up = self.create_json_str(user_list_up)
        self.save()

    # Checks if user is in user_list_up
    def is_in_user_votes_up(self, user):

        user_list_up = self.create_json_list(self.user_votes_up)
        if str(user) in user_list_up:
            return True
        else:
            return False

    # Checks if user in user_list_down
    def is_in_user_votes_down(self, user):

        user_list_down = self.create_json_list(self.user_votes_down)
        if str(user) in user_list_down:
            return True
        else:
            return False

    # Creates a list from the JSON-text format
    def create_json_list(self, input):
        jsonDec = json.decoder.JSONDecoder()
        return jsonDec.decode(input)

    # Creates a JSON-text from a list
    def create_json_str(self, input):
        return json.dumps(input)


class UserVotes(models.Model):

    user = models.ForeignKey(User, related_name="user_votes")
    question = models.ForeignKey(Question, related_name="question_votes")
    vote_type = models.CharField(max_length=16)

    class Meta:
        unique_together = ('user', 'question', 'vote_type')

