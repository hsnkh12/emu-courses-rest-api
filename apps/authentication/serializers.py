from rest_framework import serializers
from .models import User
from django.contrib.auth.password_validation import validate_password
from ..utils.serializers import DynamicFieldsModelSerializer


class RegistrationSerializer(serializers.ModelSerializer):

    password = serializers.CharField(write_only=True, required=True, validators=[validate_password])
    password2 = serializers.CharField(write_only=True, required=True)

    class Meta:
        model = User
        fields = ('id','email','username', 'password', 'password2')


    def validate(self, attrs):
        if attrs['password'] != attrs['password2']:
            raise serializers.ValidationError({"password": "Password fields didn't match."})

        return attrs

    def create(self, validated_data):
        user = User.objects.create(
            username=validated_data['username'],
            email=validated_data['email'],
        )

        
        user.set_password(validated_data['password'])
        user.save()

        return user


class ProfileSerializer(DynamicFieldsModelSerializer):

    class Meta:
        model = User
        fields = ['id', 'username', 'email']