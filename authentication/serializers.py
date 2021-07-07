from django.db.models import fields
from django.contrib.auth import authenticate
from .models import User
from rest_framework import serializers
from .services import username_validation, password_validation


class RegistrationSerializer(serializers.ModelSerializer):
    username = serializers.CharField(
        max_length=150,
        min_length=1,
        validators=[username_validation])
    password = serializers.CharField(
        max_length=128,
        min_length=1,
        validators=[password_validation]
    )
    token = serializers.CharField(max_length=255, read_only=True)

    class Meta:
        model = User
        fields = ['username', 'password', 'token']
        # fields = ['username', 'password']

    def create(self, validated_data):
        return User.objects.create_user(**validated_data)


class LoginSerializer(serializers.Serializer):
    username = serializers.CharField(max_length=150)
    password = serializers.CharField(max_length=128, write_only=True)
    token = serializers.CharField(max_length=255, read_only=True)

    def validate(self, data):
        username = data.get('username', None)
        password = data.get('password', None)

        if username is None:
            raise serializers.ValidationError(
                'Username is required to login.'
            )

        if password is None:
            raise serializers.ValidationError(
                'Password is required to login.'
            )

        user = authenticate(username=username, password=password)
        if user is None:
            raise serializers.ValidationError(
                'A user with this username and password was not found.'
            )

        if not user.is_active:
            raise serializers.ValidationError(
                'This user has been deactivated.'
            )

        return {
            'username': username,
            'password': password,
            'token': user.token
        }


class UserSerializer(serializers.ModelSerializer):
    password = serializers.CharField(
        max_length=128,
        min_length=1,
        write_only=True
    )

    class Meta:
        model = User
        fields = ('username', 'password', 'token')
        read_only_fields = ('token',)

    def update(self, instance, validated_data):
        # Retrive this data field in the beginning
        # due to another method of setting this attr
        password = validated_data.pop('password', None)

        for key, value in validated_data.items():
            setattr(instance, key, value)

        if password is not None:
            instance.set_password(password)

        instance.save()
