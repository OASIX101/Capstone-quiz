from rest_framework import serializers
from .models import CustomUser


class LogInSerializer(serializers.Serializer):
    username = serializers.CharField(max_length=100, min_length=1)
    password = serializers.CharField(max_length=100, min_length=8)

class LogOutSerializer(serializers.Serializer):
    refresh_token = serializers.CharField(max_length=500)

class RegisterSerializer(serializers.ModelSerializer):
    password = serializers.CharField(max_length=68, min_length=6, write_only=True)

    default_error_messages = {
        'username': 'The username should only contain alphanumeric characters'}

    class Meta:
        model = CustomUser
        fields = ['username', 'email', 'password', 'gender']

    def create(self, validated_data):
        return CustomUser.objects.create_user(**validated_data)

class ChangePasswordSerializer(serializers.Serializer):
    model = CustomUser

    """
    Serializer for password change endpoint.
    """
    old_password = serializers.CharField(required=True)
    new_password = serializers.CharField(required=True)

class RegisterSerializer2(serializers.ModelSerializer):

    default_error_messages = {
        'username': 'The username should only contain alphanumeric characters'}

    class Meta:
        model = CustomUser
        fields = ['username', 'email', 'gender']
