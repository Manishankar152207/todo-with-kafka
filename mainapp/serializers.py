# serializers.py
from rest_framework import serializers
from django.contrib.auth.models import User
from .models import ActivityFeed

class UserRegistrationSerializer(serializers.Serializer):
    username = serializers.CharField()
    email = serializers.EmailField()
    password = serializers.CharField(write_only=True)

    def validate(self, data):
        if User.objects.filter(username = data['username']):
            raise serializers.ValidationError("Username already Exist.")

        if User.objects.filter(email = data['email']):
            raise serializers.ValidationError("Email already Exist.")
        
        return data

    def create(self, validated_data):
        user = User.objects.create_user(
            username=validated_data['username'],
            email=validated_data['email'],
            password=validated_data['password']
        )
        return user

class UserLoginSerializer(serializers.Serializer):
    username = serializers.EmailField()
    password = serializers.CharField()

class ActivityFeedSerializer(serializers.ModelSerializer):
    class Meta:
        model = ActivityFeed
        fields = '__all__'
 