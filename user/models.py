from django.db import models
from django.contrib.auth.models import AbstractUser


class User(AbstractUser): 
    class UserType(models.TextChoices):
        STUDENT = 'student', 'Student'
        TEACHER = 'teacher', 'Teacher'
        ADMIN = 'admin', 'Admin'

    user_type = models.CharField(max_length=50, default='student', choices=UserType.choices)
    class Meta:
        verbose_name = "User"
        verbose_name_plural = "Users"
        ordering = ['-date_joined']
    
    def __str__(self):
        return self.username
    
