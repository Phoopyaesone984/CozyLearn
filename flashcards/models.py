from django.db import models
from lessons.models import Lesson
from users.models import User
from django.utils import timezone

class FlashcardSet(models.Model):
    title = models.CharField(max_length=200)
    description = models.TextField(null=True,blank=True)
    lesson = models.ForeignKey(Lesson, on_delete=models.CASCADE, related_name='flashcard_sets')
    created_by = models.ForeignKey(User, on_delete=models.CASCADE)
    created_at = models.DateTimeField(default=timezone.now)

class Flashcard(models.Model):
    flashcard_set = models.ForeignKey(
        FlashcardSet,
        on_delete=models.CASCADE,
        related_name='flashcards',
        null=True,  # Add this temporarily
        blank=True  # Add this temporarily
    )
    question = models.TextField()
    answer = models.TextField()
    created_at = models.DateTimeField(default=timezone.now)