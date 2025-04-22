# accounts/serializers.py

from rest_framework import serializers
from .models import CustomUser, NotificationSettings

class RegisterSerializer(serializers.ModelSerializer):
    password = serializers.CharField(write_only=True)

    class Meta:
        model = CustomUser
        fields = ['email', 'password', 'role', 'full_name']

    def create(self, validated_data):
        return CustomUser.objects.create_user(
            email=validated_data['email'],
            full_name=validated_data['full_name'],
            password=validated_data['password'],
            role=validated_data.get('role', 'user')  # default to 'user' if not provided
        )

class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = CustomUser
        exclude = ['password']

class UserUpdateSerializer(serializers.ModelSerializer):
    class Meta:
        model = CustomUser
        fields = ['full_name', 'avatar', 'country', 'city', 'primary_language', 'foreign_language', 'ui_language']

class NotificationSettingsSerializer(serializers.ModelSerializer):
    class Meta:
        model = NotificationSettings
        fields = ['email_notifications', 'push_notifications', 'learning_reminders', 'weekly_progress', 'new_features', 'marketing']
