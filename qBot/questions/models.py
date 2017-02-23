from __future__ import unicode_literals

from django.contrib.auth.models import User
from django.db import models
from django.utils import timezone


# making the question model to contain theese things
class Question(models.Model):
    title = models.CharField(max_length=128)
    body = models.TextField()
    created_at = models.DateTimeField(null=True, blank=True)
    # sets a connection to a user
    user = models.ForeignKey(User, related_name='is_made_by')
    votes = models.IntegerField(default = 0)

    # adds a timestamp to the question posted
    def save(self, *args, **kwargs):
        if self.created_at is None:
            self.created_at = timezone.now()
        super().save(*args, **kwargs)

    def upvote_question(self, user):
        self.question_votes.create(user=user, question=self, vote_type="up")
        self.votes += 1
        self.save()

    def downvote_question(self, user):
        self.question_votes.create(user=user, question=self, vote_type="down")
        self.votes -= 1
        self.save()

class UserVotes(models.Model):
    user = models.ForeignKey(User, related_name="user_votes")
    question = models.ForeignKey(Question, related_name="post_votes")
    vote_type = models.CharField(max_length=16)

    class Meta:
        unique_together = ('user', 'question', 'vote_type')