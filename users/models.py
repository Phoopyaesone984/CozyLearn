from django.contrib.auth.models import AbstractUser
from django.db import models
from django.utils import timezone

class User(AbstractUser):
    bio = models.TextField(blank=True)
    profile_picture = models.ImageField(upload_to='profiles/', blank=True)
    created_at = models.DateTimeField(default=timezone.now)

    def get_lessons_created(self):
        return self.lessons_created.all()

    def get_enrolled_lessons(self):
        return self.enrolled_lessons.all()

    def __str__(self):
        return self.username