from django.contrib.auth.models import AbstractUser
from django.db import models

# Create your models here.


class User(AbstractUser):
    role = models.CharField(max_length=20, choices=[
        ("admin", "Admin"),
        ('teacher', "Teacher"),
        ('student', "Student")
    ])


class Admin(models.Model):
    user = models.OneToOneField('User', on_delete=models.CASCADE)
    phone_number = models.CharField(max_length=13, default="ph_num")
    address = models.CharField(max_length=250)


class Class(models.Model):
    name = models.CharField(max_length=150)

    def __str__(self):
        return self.name


class Teacher(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    full_name = models.CharField(max_length=250)
    phone_number = models.CharField(max_length=13, default="ph_num")
    address = models.CharField(max_length=250, default="Address not specified")
    price = models.DecimalField(max_digits=8, decimal_places=2)
    classes = models.ManyToManyField(Class, related_name="teachers")

    def __str__(self):
        return self.full_name


class Student(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    full_name = models.CharField(max_length=250)
    phone_number = models.CharField(max_length=13, default="ph_num")
    address = models.CharField(max_length=250, default="Address not specified")
    class_group = models.ForeignKey(Class, on_delete=models.CASCADE)

    def __str__(self):
        return f"F.I.O {self.full_name} sinfiz {self.class_group}"