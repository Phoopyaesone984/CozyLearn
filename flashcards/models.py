from django.db import models
from lessons.models import Lesson
from users.models import User

class Flashcard(models.Model):
    lesson = models.ForeignKey(Lesson, on_delete=models.CASCADE, related_name='flashcards')
    question = models.TextField()
    answer = models.TextField()
    creator = models.ForeignKey(User, on_delete=models.CASCADE)
    mastered = models.BooleanField(default=False)
