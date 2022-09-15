from ..utils.serializers import DynamicFieldsModelSerializer
from .models import Course, Resource, Like
from rest_framework import serializers
from django.conf import settings

class CourseSerializer(DynamicFieldsModelSerializer):

    class Meta:
        model = Course
        fields = '__all__'

class LikeSerializer(serializers.Serializer):

    class Meta:
        model = Like
        fields = ['is_liked','user']


class UserSerializer(serializers.Serializer):

    class Meta:
        model = settings.AUTH_USER_MODEL
        fields = ['username']


class ResourceSerializer(DynamicFieldsModelSerializer):

    user = UserSerializer()
    likes = LikeSerializer(many=True)

    class Meta:
        model = Resource
        fields = ['id','user','title','url','description','date_added','likes']
        read_only_fields = ['id','user','likes']