from django.db import models
from user.models import User
from utils.models import TimeStampedModel

class Enrollment(TimeStampedModel):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='enrollments')
    course = models.ForeignKey('course.Course', on_delete=models.CASCADE, related_name='enrollments')
    enrolled_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        unique_together = ['user', 'course']
    

    def create(self, **kwargs):
        self.user = kwargs.pop('user')
        self.course = kwargs.pop('course')
        self.create(**kwargs)
        self.save()