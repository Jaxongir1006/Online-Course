from django.db import models
from utils.models import TimeStampedModel


class Comment(TimeStampedModel):
    user = models.ForeignKey('user.User', on_delete=models.CASCADE, related_name='comments')
    course = models.ForeignKey('course.Course', on_delete=models.CASCADE, related_name='comments')
    text = models.TextField()
    parent = models.ForeignKey('self', on_delete=models.SET_NULL, null=True, blank=True)

