from django.db import models
from users.models import User

class Lesson(models.Model):
    title = models.CharField(max_length=255)
    content = models.TextField()
    creator = models.ForeignKey(User, on_delete=models.CASCADE, related_name='created_lessons')
    category = models.CharField(max_length=100)
    visibility = models.CharField(max_length=20, choices=[('public', 'Public'), ('private', 'Private')])
    created_at = models.DateTimeField(auto_now_add=True)
