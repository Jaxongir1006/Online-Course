from django.contrib import admin
from .models import User

@admin.register(User)
class UserAdmin(admin.ModelAdmin):
    list_display = ('username', 'email', 'date_joined', 'is_active', 'id')
    search_fields = ('username', 'email')
    list_filter = ('is_active', 'is_staff')
    ordering = ('-date_joined',)