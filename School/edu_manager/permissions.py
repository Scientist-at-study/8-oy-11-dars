from rest_framework import permissions
from .models import Teacher, Class, Student


class IsAdmin(permissions.BasePermission):
    def has_permission(self, request, view):
        if not request.user or not request.user.is_authenticated:
            return False

        if request.user.role == 'admin':
            return True

        return request.method in permissions.SAFE_METHODS

    def has_object_permission(self, request, view, obj):
        if not request.user or not request.user.is_authenticated:
            return False

        if request.user.role == 'admin':
            return True

        return request.method in permissions.SAFE_METHODS


class IsTeacher(permissions.BasePermission):
    def has_permission(self, request, view):
        if not request.user or not request.user.is_authenticated:
            return False

        return request.user.role in ['teacher', 'admin']

    def has_object_permission(self, request, view, obj):
        if not request.user or not request.user.is_authenticated:
            return False

        if request.user.role == 'admin':
            return True

        if request.user.role != 'teacher':
            return False

        if request.method in permissions.SAFE_METHODS:
            return True

        if isinstance(obj, Teacher) and obj.user == request.user:
            return True

        if isinstance(obj, Class) and obj.teachers.filter(user=request.user).exists():
            return True

        if isinstance(obj, Student) and obj.class_group.teachers.filter(user=request.user).exists():
            return True

        return False


class IsStudent(permissions.BasePermission):
    def has_permission(self, request, view):
        if not request.user or not request.user.is_authenticated:
            return False

        return request.user.role in ['admin', 'teacher', 'student']

    def has_object_permission(self, request, view, obj):
        if not request.user or not request.user.is_authenticated:
            return False

        if request.user.role == 'admin':
            return True

        if request.user.role == 'teacher':
            if isinstance(obj, Student) and obj.class_group.teachers.filter(user=request.user).exists():
                return True
            if isinstance(obj, Class) and obj.teachers.filter(user=request.user).exists():
                return True
            return request.method in permissions.SAFE_METHODS

        if request.user.role != 'student':
            return False

        if request.method in permissions.SAFE_METHODS:
            if isinstance(obj, Student) and obj.user == request.user:
                return True
            if isinstance(obj, Class) and obj.student_set.filter(user=request.user).exists():
                return True
            return False

        if isinstance(obj, Student) and obj.user == request.user:
            return True

        return False