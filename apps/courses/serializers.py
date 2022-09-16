from dataclasses import field
from ..utils.serializers import DynamicFieldsModelSerializer
from .models import Course, Resource, Like, Department
from rest_framework import serializers
from django.conf import settings
from ..authentication.models import User


class DepartmentSerializer(DynamicFieldsModelSerializer):

    class Meta:
        model = Department
        fields = ['name']

class CourseSerializer(DynamicFieldsModelSerializer):

    department = DepartmentSerializer()

    class Meta:
        model = Course
        fields = '__all__'

class LikeSerializer(serializers.ModelSerializer):

    class Meta:
        model = Like
        fields = ['is_liked']


class UserSerializer(DynamicFieldsModelSerializer):

    class Meta:
        model = User
        fields = '__all__'


class ResourceSerializer(DynamicFieldsModelSerializer):

    user = UserSerializer(fields=['id','username'])

    class Meta:
        model = Resource
        fields = ['id', 'user' ,'title', 'url', 'description','date_added', 'likes_count']