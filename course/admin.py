from django.contrib import admin
from .models import Course, Lesson

@admin.register(Course)
class CourseAdmin(admin.ModelAdmin):
    list_display = ('title', 'user', 'price')
    search_fields = ('title', 'user__username')
    list_filter = ('user',)


@admin.register(Lesson)
class LessonAdmin(admin.ModelAdmin):
    list_display = ('title', 'course', 'duration_minutes')
    search_fields = ('title', 'course__title')
    list_filter = ('course',)