from django.db import models
from django.db.models import Avg


class Rating(models.Model):
    user = models.ForeignKey('user.User', on_delete=models.CASCADE)
    course = models.ForeignKey('course.Course', on_delete=models.CASCADE)
    stars = models.PositiveSmallIntegerField()  # 1–5

    class Meta:
        unique_together = ('user', 'course')


    def __str__(self):
        return f'{self.user.username} - {self.course.title} - {self.stars}'
    
    def calculate_rating(self) -> float:
        """
        Kurs boyicha ortacha reytingni hisoblaydi
        """
        avg = Rating.objects.filter(course=self.course).aggregate(Avg('stars'))['stars__avg']
        return round(avg or 0.0, 2)