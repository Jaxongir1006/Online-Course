from django.contrib import admin
from .models import Rating



@admin.register(Rating)
class RatingAdmin(admin.ModelAdmin):
    list_display = ('user', 'course', 'stars')
    search_fields = ('user__username', 'course__title')
    list_filter = ('user', 'course')