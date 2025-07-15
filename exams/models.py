from django.db import models
from utils.models import TimeStampedModel


class Exam(TimeStampedModel):
    course = models.ForeignKey('course.Course', on_delete=models.CASCADE)
    title = models.CharField(max_length=200)

class ExamQuestion(TimeStampedModel):
    exam = models.ForeignKey(Exam, on_delete=models.CASCADE, related_name='questions', blank=True, null=True)
    text = models.TextField()
    image = models.ImageField(upload_to='exams/%Y/%m/%d', blank=True, null=True)
    correct_option = models.CharField(max_length=1, choices=[
        ('A', 'Option A'),
        ('B', 'Option B'),
        ('C', 'Option C'),
        ('D', 'Option D'),
    ])

class QuestionOption(models.Model):
    question = models.ForeignKey(ExamQuestion, on_delete=models.CASCADE, related_name='options')
    label = models.CharField(max_length=1, choices=[
        ('A', 'A'),
        ('B', 'B'),
        ('C', 'C'),
        ('D', 'D'),
    ])
    text = models.TextField()


class ExamResult(models.Model):
    user = models.ForeignKey("user.User", on_delete=models.CASCADE)
    exam = models.ForeignKey(Exam, on_delete=models.CASCADE)
    score = models.FloatField()
    total_questions = models.PositiveIntegerField()
    correct_answers = models.PositiveIntegerField()
    submitted_at = models.DateTimeField(auto_now_add=True)
