from rest_framework import serializers
from .models import LinguaUser


class LinguaUserSerializer(serializers.ModelSerializer):
    password = serializers.CharField(write_only=True)
    birthdate = serializers.DateField(write_only=True)
    date_joined = serializers.DateTimeField(read_only=True)

    class Meta:
        model = LinguaUser
        fields = [
            'id',
            'email',
            'username',
            'password',
            'first_name',
            'last_name',
            'birthdate',
            'gender',
            'date_joined'
        ]


class ValidateUserSerializer(serializers.Serializer):
    username = serializers.CharField()
    code = serializers.CharField()

class AuthSerializer(serializers.Serializer):
    username=serializers.CharField()
    password = serializers.CharField()
