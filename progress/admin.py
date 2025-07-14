from django.contrib import admin
from .models import Progress

@admin.register(Progress)
class ProgressAdmin(admin.ModelAdmin):
    list_display = ('user', 'lesson', 'watched_at', 'watched')
    search_fields = ('user__username', 'lesson__title')
    list_filter = ('user', 'lesson')