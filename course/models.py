from django.db import models
from utils.models import TimeStampedModel
from django_extensions.db.fields import AutoSlugField

class Course(TimeStampedModel):
    user = models.ForeignKey('user.User', related_name='courses', on_delete=models.CASCADE)
    title = models.CharField(max_length=200)
    description = models.TextField()
    price = models.DecimalField(max_digits=10, decimal_places=2)
    image = models.ImageField(upload_to='courses/images/', blank=True, null=True)
    slug = AutoSlugField(populate_from='title', unique=True)

    def __str__(self):
        try:
            return f'{self.title} - {self.user.username}'
        except Exception as e:
            return f'{self.title} - UnknownUser ({e})'
        
    @property
    def image_url(self):
        return self.image.url if self.image else None
    

class Lesson(TimeStampedModel):
    course = models.ForeignKey(Course, related_name='lessons', on_delete=models.CASCADE)
    title = models.CharField(max_length=200)
    duration_minutes = models.PositiveIntegerField()
    video_url = models.URLField(blank=True, null=True)

    def __str__(self):
        return f"{self.title} - {self.course.title}"
    
    @property
    def video_embed_url(self):
        return self.video_url.replace("watch?v=", "embed/") if self.video_url else None