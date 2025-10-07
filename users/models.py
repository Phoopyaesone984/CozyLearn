from django.contrib.auth.models import AbstractUser, Group, Permission
from django.db import models

class User(AbstractUser):
    bio = models.TextField(blank=True)
    profile_pic = models.ImageField(upload_to='profiles/', blank=True, null=True)

    # Fix reverse accessor clashes
    groups = models.ManyToManyField(
        Group,
        related_name='custom_user_set',  # changed from default 'user_set'
        blank=True,
        help_text='The groups this user belongs to.',
        verbose_name='groups'
    )
    user_permissions = models.ManyToManyField(
        Permission,
        related_name='custom_user_permissions_set',  # changed from default
        blank=True,
        help_text='Specific permissions for this user.',
        verbose_name='user permissions'
    )
