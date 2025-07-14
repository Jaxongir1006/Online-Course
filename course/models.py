from django.db import models
from utils.models import TimeStampedModel
from django_extensions.db.fields import AutoSlugField
from django.utils.timezone import now

class Category(TimeStampedModel):
    name = models.CharField(max_length=100)
    slug = AutoSlugField(populate_from='name', unique=True)
    image = models.ImageField(upload_to='categories/images/', blank=True, null=True)

    def __str__(self):
        return self.name
    
    @property
    def imageURL(self):
        return self.image.url if self.image else None

class SubCategory(TimeStampedModel):
    category = models.ForeignKey(Category, related_name='subcategories', on_delete=models.CASCADE)
    name = models.CharField(max_length=100)
    slug = AutoSlugField(populate_from='name', unique=True)
    image = models.ImageField(upload_to='subcategories/images/', blank=True, null=True)

    def __str__(self):
        return self.name
        
    @property
    def imageURL(self):
        return self.image.url if self.image else None

class Course(TimeStampedModel):
    user = models.ForeignKey('user.User', related_name='courses', on_delete=models.CASCADE)
    title = models.CharField(max_length=200)
    description = models.TextField()
    price = models.DecimalField(max_digits=10, decimal_places=2)
    image = models.ImageField(upload_to='courses/images/', blank=True, null=True)
    slug = AutoSlugField(populate_from='title', unique=True)
    is_deleted = models.BooleanField(default=False)
    deleted_at = models.DateTimeField(null=True, blank=True)
    category = models.ForeignKey(Category, related_name='courses', on_delete=models.CASCADE)

    def delete(self, using =None, keep_parents = False):
        self.is_deleted = True
        self.deleted_at = now()
        self.save()

    def restore(self):
        self.is_deleted = False
        self.deleted_at = None
        self.save() 

    def __str__(self):
        try:
            return f'{self.title} - {self.user.username}'
        except Exception as e:
            return f'{self.title}- UnknownUser ({e})'
        
    @property
    def image_url(self):
        return self.image.url if self.image else None
    

class Lesson(TimeStampedModel):
    course = models.ForeignKey(Course, related_name='lessons', on_delete=models.CASCADE)
    title = models.CharField(max_length=200)
    duration_minutes = models.PositiveIntegerField()
    video_url = models.URLField(blank=True, null=True)
    is_deleted = models.BooleanField(default=False)
    deleted_at = models.DateTimeField(null=True, blank=True)

    def __str__(self):
        return f"{self.title} - {self.course.title}"
    
    @property
    def video_embed_url(self):
        return self.video_url.replace("watch?v=", "embed/") if self.video_url else None
    
    def delete(self, using =None, keep_parents = False):
        self.is_deleted = True
        self.deleted_at = now()
        self.save()

    def restore(self):
        self.is_deleted = False
        self.deleted_at = None
        self.save()