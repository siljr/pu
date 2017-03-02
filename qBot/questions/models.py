from __future__ import unicode_literals

from django.contrib.auth.models import User
from django.db import models
from django.utils import timezone
from django.conf import settings


# making the question model to contain theese things
class Question(models.Model):
    title = models.CharField(max_length=128)
    body = models.TextField()
    created_at = models.DateTimeField(null=True, blank=True)
    # sets a connection to a user
    user = models.ForeignKey(settings.AUTH_USER_MODEL, default= 1)
    votes = models.ManyToManyField(User, related_name='voted_for_question')

    # adds a timestamp to the question posted
    def save(self, *args, **kwargs):
        if self.created_at is None:
            self.created_at = timezone.now()
        super().save(*args, **kwargs)
