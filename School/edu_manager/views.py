from django.shortcuts import render
from rest_framework.viewsets import ModelViewSet
from .models import Admin, Teacher, Class, Student
from .serializers import (ClassSerializer, StudentSerializer,
                          StudentStringSerializer, StudentPrimaryKeySerializer,
                          StudentSlugSerializer, StudentHyperlinkedRelatedSerializer,
                          StudentHyperlinkedIdentitySerializer, ClassWithStudentsSerializer,
                          TeacherWithPrimaryKeySerializer, AdminSerializers,
                          StudentFullSerializer, TeacherFullSerializer)

# Create your views here.

class AdminViewSet(ModelViewSet):
    queryset = Admin.objects.all()
    serializer_class = AdminSerializers


class TeacherViewSet(ModelViewSet):
    queryset = Teacher.objects.all()
    serializer_class = TeacherFullSerializer


class ClassViewSet(ModelViewSet):
    queryset = Class.objects.all()
    serializer_class = ClassWithStudentsSerializer


class StudentViewSet(ModelViewSet):
    queryset = Student.objects.all()
    serializer_class = StudentFullSerializer