from django.contrib import admin
from .models import Course

@admin.register(Course)
class CourseAdmin(admin.ModelAdmin):
    list_display = ('title', 'user', 'price')
    search_fields = ('title', 'user__username')
    list_filter = ('user',)