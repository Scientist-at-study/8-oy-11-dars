from django.contrib import admin
from .models import Admin, Teacher, Class, Student

# Register your models here.

admin.site.register(Admin)

@admin.register(Class)
class ClassAdmin(admin.ModelAdmin):
    list_display = ('id', 'name')
    search_fields = ('name',)


@admin.register(Teacher)
class TeacherAdmin(admin.ModelAdmin):
    list_display = ('id', 'full_name', 'price')
    search_fields = ('full_name',)
    filter_horizontal = ('classes',)


@admin.register(Student)
class StudentAdmin(admin.ModelAdmin):
    list_display = ('id', 'full_name', 'class_group')
    search_fields = ('full_name',)
    list_filter = ('class_group',)
