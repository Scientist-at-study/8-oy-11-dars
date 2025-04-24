from django.shortcuts import render
from rest_framework.viewsets import ModelViewSet
from .models import Admin, Teacher, Class, Student
from .serializers import (ClassSerializer, StudentSerializer,
                          StudentStringSerializer, StudentPrimaryKeySerializer,
                          StudentSlugSerializer, StudentHyperlinkedRelatedSerializer,
                          StudentHyperlinkedIdentitySerializer, ClassWithStudentsSerializer,
                          TeacherWithPrimaryKeySerializer, AdminSerializers,
                          StudentFullSerializer, TeacherFullSerializer)

from .permissions import IsAdmin, IsStudent, IsTeacher

# Create your views here.

class AdminViewSet(ModelViewSet):
    queryset = Admin.objects.all()
    serializer_class = AdminSerializers
    permission_classes = [IsAdmin]


class TeacherViewSet(ModelViewSet):
    queryset = Teacher.objects.all()
    serializer_class = TeacherFullSerializer
    permission_classes = [IsTeacher | IsAdmin]


class ClassViewSet(ModelViewSet):
    queryset = Class.objects.all()
    serializer_class = ClassWithStudentsSerializer
    permission_classes = [IsAdmin | IsTeacher | IsStudent]


class StudentViewSet(ModelViewSet):
    queryset = Student.objects.all()
    serializer_class = StudentFullSerializer
    permission_classes = [IsAdmin | IsTeacher | IsStudent]