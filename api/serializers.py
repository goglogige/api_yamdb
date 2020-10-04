from rest_framework import serializers

from .models import User


class UserSerializer(serializers.ModelSerializer):

    class Meta:
        model = User
        fields = ['id', 'first_name', 'last_name', 'username', 'bio', 'email', 'role']


class EmailSerializer(serializers.Serializer):
    email = serializers.EmailField(max_length=75)


class UserCreateSerializer(serializers.Serializer):
    email = serializers.EmailField(max_length=75)
    confirmation_code = serializers.CharField(max_length=10)
