from django.contrib import admin
from .models import Comment

@admin.register(Comment)
class CommentAdmin(admin.ModelAdmin):
    list_display = ('user', 'course', 'text', 'parent')
    search_fields = ('user__username', 'course__title')
    list_filter = ('user', 'course')