import datetime

from django.utils import timezone
from django.db import models


class Poll(models.Model):
    question = models.CharField(max_length=242)
    pub_date = models.DateTimeField('date published')

    def __str__(self):
        return self.question

    def was_published_recently(self):
        now = timezone.now()
        return now - datetime.timedelta(days=1) <= self.pub_date < now


class Choice(models.Model):
    poll = models.ForeignKey(Poll)
    choice_text = models.CharField(max_length=242)
    votes = models.IntegerField(default=0)

    def __str__(self):
        return self.choice_text
