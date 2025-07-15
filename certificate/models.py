from django.db import models
from utils.models import TimeStampedModel

class Certificate(TimeStampedModel):
    user = models.ForeignKey('user.User', related_name='certificates', on_delete=models.CASCADE)
    course = models.ForeignKey('course.Course', related_name='certificates', on_delete=models.CASCADE)
    issued_at = models.DateTimeField(auto_now_add=True)
    certificate_file = models.FileField(upload_to='certificates/')

    def __str__(self):
        return f"{self.user} - {self.course}"
    
    class Meta:
        unique_together = ['user', 'course']
        verbose_name = 'Certificate'
        verbose_name_plural = 'Certificates'