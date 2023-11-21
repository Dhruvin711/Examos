from django.db import models

# Create your models here.

class Question(models.Model):
    question = models.TextField()
    subject = models.CharField(max_length=255)
    topic = models.CharField(max_length=255)
    difficulty = models.CharField(max_length=10)
    marks = models.IntegerField()

    def __str__(self):
        return self.question