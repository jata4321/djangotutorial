import datetime

from django.db import models
from django.utils import timezone
from users.models import User

# Create your models here.
class Question(models.Model):

    def __str__(self):
        return self.question_text

    def was_published_recently(self):
        now = timezone.now()
        return now >= self.publication_date >= timezone.now() - datetime.timedelta(days=1)

    question_text = models.CharField(max_length=200)
    author = models.ForeignKey(User, on_delete=models.CASCADE, related_name='questions',
                               null=True, blank=True)
    publication_date = models.DateTimeField("date published", default=timezone.now)


class Choice(models.Model):

    def __str__(self):
        return self.choice_text

    question = models.ForeignKey(Question,
                                 on_delete=models.CASCADE,
                                 related_name='choices')
    choice_text = models.CharField(max_length=200)
    votes = models.IntegerField(default=0)


