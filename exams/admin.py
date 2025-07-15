from django.contrib import admin
from .models import ExamQuestion,Exam, ExamResult, QuestionOption


@admin.register(ExamQuestion)
class ExamQuestionAdmin(admin.ModelAdmin):
    list_display = ('text', 'image', 'correct_option', 'id')
    search_fields = ('text',)
    list_filter = ('exam', 'correct_option')


@admin.register(QuestionOption)
class QuestionOptionAdmin(admin.ModelAdmin):
    list_display = ('question', 'label', 'id')
    list_filter = ('question',)
    search_fields = ('question__text', 'question__course__title')


@admin.register(ExamResult)
class ExamResultAdmin(admin.ModelAdmin):
    list_display = ('user__username', 'exam', 'score', 'total_questions', 'correct_answers', 'submitted_at')
    list_filter = ('user', 'exam', 'submitted_at')


@admin.register(Exam)
class ExamAdmin(admin.ModelAdmin):
    list_display = ('title', 'course', 'id')
    search_fields = ('title', 'course__title')
    list_filter = ('course',)