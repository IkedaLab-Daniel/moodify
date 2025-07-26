from rest_framework import serializers
from djoser.serializers import UserCreateSerializer as BaseUserCreateSerializer
from djoser.serializers import UserSerializer as BaseUserSerializer
from .models import User, UserProfile


class UserCreateSerializer(BaseUserCreateSerializer):
    """Custom user creation serializer"""
    class Meta(BaseUserCreateSerializer.Meta):
        model = User
        fields = ('id', 'email', 'username', 'password', 'first_name', 'last_name')


class UserSerializer(BaseUserSerializer):
    """Custom user serializer"""
    class Meta(BaseUserSerializer.Meta):
        model = User
        fields = ('id', 'email', 'username', 'first_name', 'last_name', 'is_verified', 'created_at')
        read_only_fields = ('id', 'created_at', 'is_verified')


class UserProfileSerializer(serializers.ModelSerializer):
    """User profile serializer"""
    user = UserSerializer(read_only=True)
    
    class Meta:
        model = UserProfile
        fields = ('user', 'bio', 'mood_preferences', 'avatar', 'notification_preferences', 'created_at', 'updated_at')
        read_only_fields = ('created_at', 'updated_at')


class UserWithProfileSerializer(serializers.ModelSerializer):
    """User serializer with profile information"""
    profile = UserProfileSerializer(read_only=True)
    
    class Meta:
        model = User
        fields = ('id', 'email', 'username', 'first_name', 'last_name', 'is_verified', 'created_at', 'profile')
        read_only_fields = ('id', 'created_at', 'is_verified')
