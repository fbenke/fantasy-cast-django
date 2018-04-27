from django.contrib.auth import password_validation, authenticate
from django.core.exceptions import ValidationError

from rest_framework import fields, serializers

from account.models import CustomUser as User


class PasswordSerializer(serializers.Serializer):

    password1 = fields.CharField(label='Password')
    password2 = fields.CharField(label='Password confirmation')

    def validate_password1(self, value):
        'Wrap Django password validation.'
        try:
            password_validation.validate_password(value)
            return value
        except ValidationError as e:
            raise serializers.ValidationError(e.messages)

    def validate(self, data):
        if data.get('password1') != data.get('password2'):
            raise serializers.ValidationError('Passwords do not match')
        return data


class SignupSerializer(PasswordSerializer):

    email = fields.EmailField(label='Email')

    def validate_email(self, value):
        'Validate that the e-mail address is unique.'

        if User.objects.filter(email__iexact=value):
            raise serializers.ValidationError('Email is already use')
        return value

    def create(self, validated_data):

        return User.objects.create_user(email=validated_data.get('email'),
                                        password=validated_data.get('password1'))
