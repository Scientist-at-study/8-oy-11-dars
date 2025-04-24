from rest_framework import serializers
from .models import User, Admin, Teacher, Class, Student


class UserSerializers(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['username', 'email', 'password', 'first_name', 'last_name', 'role']
        extra_kwargs = {'password': {'write_only': True}}
        read_only_fields = ['role']


class AdminSerializers(serializers.ModelSerializer):
    user = UserSerializers()

    class Meta:
        model = Admin
        fields = ['id', 'user', 'phone_number', 'address']

    def create(self, validated_data):
        user_data = validated_data.pop("user")
        password = user_data.pop("password")
        user = User.objects.create_user(**user_data, role='admin')
        user.set_password(password)
        user.save()

        admin = Admin.objects.create(user=user, **validated_data)
        return admin

    def update(self, instance, validated_data):
        user = instance.user
        user_data = validated_data.pop("user", {})
        for attr, value in user_data.items():
            if attr == 'password':
                user.set_password(value)
            else:
                setattr(user, attr, value)
        user.save()

        for attr, value in validated_data.items():
            setattr(instance, attr, value)
        instance.save()
        return instance


class ClassSerializer(serializers.ModelSerializer):
    class Meta:
        model = Class
        fields = ['id', 'name']


class StudentSerializer(serializers.ModelSerializer):
    class Meta:
        model = Student
        fields = ['id', 'full_name']


# StringRelatedField
class StudentStringSerializer(serializers.ModelSerializer):
    class_group = serializers.StringRelatedField()

    class Meta:
        model = Student
        fields = ['id', 'full_name', 'class_group']


# PrimaryKeyRelatedField
class StudentPrimaryKeySerializer(serializers.ModelSerializer):
    class_group = serializers.PrimaryKeyRelatedField(queryset=Class.objects.all())

    class Meta:
        model = Student
        fields = ['id', 'full_name', 'class_group']


# SlugRelatedField
class StudentSlugSerializer(serializers.ModelSerializer):
    class_group = serializers.SlugRelatedField(slug_field='name', queryset=Class.objects.all())

    class Meta:
        model = Student
        fields = ['id', 'full_name', 'class_group']


# HyperlinkedRelatedField
class StudentHyperlinkedRelatedSerializer(serializers.HyperlinkedModelSerializer):
    class_group = serializers.HyperlinkedRelatedField(view_name='class-detail', queryset=Class.objects.all())

    class Meta:
        model = Student
        fields = ['id', 'url', 'full_name', 'class_group']


# HyperlinkedIdentityField
class StudentHyperlinkedIdentitySerializer(serializers.HyperlinkedModelSerializer):
    url = serializers.HyperlinkedIdentityField(view_name='student-detail')

    class Meta:
        model = Student
        fields = ['id', 'url', 'full_name', 'class_group']


# Nested relationship (Class -> Students)
class ClassWithStudentsSerializer(serializers.ModelSerializer):
    students = StudentSerializer(many=True, read_only=True, source='student_set')

    class Meta:
        model = Class
        fields = ['id', 'name', 'students']


# Teacher with PrimaryKey
class TeacherWithPrimaryKeySerializer(serializers.ModelSerializer):
    classes = serializers.PrimaryKeyRelatedField(many=True, queryset=Class.objects.all())

    class Meta:
        model = Teacher
        fields = ['id', 'full_name', 'price', 'classes']


# Teacher with nested class
class TeacherWithNestedClassesSerializer(serializers.ModelSerializer):
    classes = ClassSerializer(many=True)

    class Meta:
        model = Teacher
        fields = ['id', 'full_name', 'price', 'classes']

    def create(self, validated_data):
        classes_data = validated_data.pop('classes')
        teacher = Teacher.objects.create(**validated_data)
        for class_data in classes_data:
            class_obj, _ = Class.objects.get_or_create(**class_data)
            teacher.classes.add(class_obj)
        return teacher

    def update(self, instance, validated_data):
        classes_data = validated_data.pop('classes')
        instance.full_name = validated_data.get('full_name', instance.full_name)
        instance.price = validated_data.get('price', instance.price)
        instance.save()
        instance.classes.clear()
        for class_data in classes_data:
            class_obj, _ = Class.objects.get_or_create(**class_data)
            instance.classes.add(class_obj)
        return instance


class TeacherFullSerializer(serializers.ModelSerializer):
    user = UserSerializers()
    classes = serializers.PrimaryKeyRelatedField(many=True, queryset=Class.objects.all())

    class Meta:
        model = Teacher
        fields = ['id', 'user', 'full_name', 'phone_number', 'address', 'price', 'classes']

    def create(self, validated_data):
        user_data = validated_data.pop("user")
        password = user_data.pop("password")
        user = User.objects.create_user(**user_data, role='teacher')
        user.set_password(password)
        user.save()

        classes = validated_data.pop("classes")
        teacher = Teacher.objects.create(user=user, **validated_data)
        teacher.classes.set(classes)
        return teacher

    def update(self, instance, validated_data):
        user_data = validated_data.pop("user", {})
        user = instance.user
        for attr, value in user_data.items():
            if attr == 'password':
                user.set_password(value)
            else:
                setattr(user, attr, value)
        user.save()

        for attr, value in validated_data.items():
            if attr == 'classes':
                instance.classes.set(value)
            else:
                setattr(instance, attr, value)
        instance.save()
        return instance


class StudentFullSerializer(serializers.ModelSerializer):
    user = UserSerializers()

    class Meta:
        model = Student
        fields = ['id', 'user', 'full_name', 'phone_number', 'address', 'class_group']

    def create(self, validated_data):
        user_data = validated_data.pop("user")
        password = user_data.pop("password")
        user = User.objects.create_user(**user_data, role='student')
        user.set_password(password)
        user.save()

        student = Student.objects.create(user=user, **validated_data)
        return student

    def update(self, instance, validated_data):
        user_data = validated_data.pop("user", {})
        user = instance.user
        for attr, value in user_data.items():
            if attr == 'password':
                user.set_password(value)
            else:
                setattr(user, attr, value)
        user.save()

        for attr, value in validated_data.items():
            setattr(instance, attr, value)
        instance.save()
        return instance
