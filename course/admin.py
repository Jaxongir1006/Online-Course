from django.contrib import admin
from .models import Course, Lesson,Category,SubCategory

@admin.register(Course)
class CourseAdmin(admin.ModelAdmin):
    list_display = ('title', 'user', 'price', 'id')
    search_fields = ('title', 'user__username')
    list_filter = ('user',)


@admin.register(Lesson)
class LessonAdmin(admin.ModelAdmin):
    list_display = ('title', 'course', 'duration_minutes', 'id')
    search_fields = ('title', 'course__title')
    list_filter = ('course',)


@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    list_display = ('name', 'id')
    search_fields = ('name',)
    list_filter = ('name',)


@admin.register(SubCategory)
class SubCategoryAdmin(admin.ModelAdmin):
    list_display = ('name', 'category', 'id')
    search_fields = ('name', 'category__name')
    list_filter = ('category',)