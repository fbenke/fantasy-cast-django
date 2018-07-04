from django.contrib.auth import password_validation
from django.core.exceptions import ValidationError as _ValidationError

from rest_framework.serializers import Serializer, ModelSerializer, ValidationError
from rest_framework import fields

from account.models import CustomUser as User


class PasswordSerializer(Serializer):

    password1 = fields.CharField(label='Password')
    password2 = fields.CharField(label='Password confirmation')

    def validate_password1(self, value):
        'Wrap Django password validation.'
        try:
            password_validation.validate_password(value)
            return value
        except _ValidationError as e:
            raise ValidationError(e.messages)

    def validate(self, data):
        if data.get('password1') != data.get('password2'):
            raise ValidationError('Passwords do not match')
        return data


class SignupSerializer(PasswordSerializer):

    email = fields.EmailField(label='Email')
    username = fields.CharField(label='Username')

    def validate_username(self, value):
        'Validate that the username is unique.'

        if User.objects.filter(username__iexact=value):
            raise ValidationError('Username is already in use')
        return value

    def validate_email(self, value):
        'Validate that the e-mail address is unique.'

        if User.objects.filter(email__iexact=value):
            raise ValidationError('Email is already in use')
        return value

    def create(self, validated_data):

        return User.objects.create_user(
            email=validated_data.get('email'),
            password=validated_data.get('password1'),
            username=validated_data.get('username')
        )


class UserSerializer(ModelSerializer):

    class Meta:
        model = User
        fields = ('username',)
        depth = 1


class UserDetailSerializer(ModelSerializer):

    class Meta:
        model = User
        fields = ('username', 'email', 'id')
        depth = 1
