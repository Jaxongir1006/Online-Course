from django.db import models


class Progress(models.Model):
    user = models.ForeignKey("user.User", on_delete=models.CASCADE, related_name='progresses')
    lesson = models.ForeignKey("course.Lesson", on_delete=models.CASCADE, related_name='progresses')
    watched_at = models.DateTimeField(auto_now_add=True)
    watched = models.BooleanField(default=False)