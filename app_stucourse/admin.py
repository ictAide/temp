from django.contrib import admin

# Register your models here.
from django.contrib import admin
from app_stucourse.models import Student, Course

# Customize the Student admin interface
@admin.register(Student)
class StudentAdmin(admin.ModelAdmin):
    list_display = ('id', 'name', 'email')  # Columns displayed in the list view
    search_fields = ('name', 'email')  # Search functionality
    list_filter = ('name',)  # Filters in the sidebar
    ordering = ('id',)  # Default ordering
    fields = ('name', 'email')  # Fields displayed in the edit form

# Customize the Course admin interface
@admin.register(Course)
class CourseAdmin(admin.ModelAdmin):
    list_display = ('id', 'title')  # Columns displayed in the list view
    search_fields = ('title',)  # Search functionality
    list_filter = ('title',)  # Filters in the sidebar
    ordering = ('id',)  # Default ordering
    fields = ('title',)  # Fields displayed in the edit form
