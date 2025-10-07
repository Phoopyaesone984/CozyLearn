from django.db import models
from users.models import User
from lessons.models import Lesson

class StudyLog(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='study_logs')
    lesson = models.ForeignKey(Lesson, on_delete=models.CASCADE, null=True, blank=True)
    duration = models.IntegerField(help_text="Duration in minutes")
    notes = models.TextField(blank=True)
    date = models.DateField(auto_now_add=True)
    shared_with_friends = models.BooleanField(default=False)
