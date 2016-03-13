from __future__ import unicode_literals
from django.db import models
from django.contrib.auth.models import User


class QuestionManager(models.Manager):
    def last(self):
        return self.order_by('-id')
    def popular(self):
        return self.order_by('-rating')


class Question(models.Model):
    title = models.CharField(max_length=255)
    text = models.TextField()
    added_at = models.DateTimeField(auto_now_add=True)
    rating = models.IntegerField(default=0)
    author = models.ForeignKey(User, on_delete=models.CASCADE, default=1)
    likes = models.ManyToManyField(User, related_name= 'likes')

    objects = QuestionManager()

    def get_url(self):
        return reverse('questions:question-show', {'pk': self.id})



class Answer(models.Model):
    text = models.TextField()
    added_at = models.DateTimeField(auto_now_add=True)

    question = models.ForeignKey(Question, on_delete=models.CASCADE)

    author = models.ForeignKey(User, on_delete=models.CASCADE, default=1)
