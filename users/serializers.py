from django.contrib.auth import authenticate
from django.contrib.auth.hashers import make_password
from django.contrib.auth.password_validation import validate_password
from django.urls import reverse
from rest_framework import serializers
from rest_framework.exceptions import (AuthenticationFailed, ValidationError)

from .models import User, FriendRequest


class PasswordField(serializers.CharField):
    """Django-форма для пароля"""

    def __init__(self, **kwargs):
        kwargs['style'] = {'input_type': 'password'}
        kwargs.setdefault('write_only', True)
        super().__init__(**kwargs)
        self.validators.append(validate_password)


class CreateUserSerializer(serializers.ModelSerializer):
    """Класс модели сериализатора для создания пользователя"""
    password = PasswordField(required=True)
    password_repeat = PasswordField(required=True, style={'input_type': 'password'}, write_only=True)

    class Meta:
        """Мета-класс для указания модели для сериализатора и полей модели сериализатора"""
        model = User
        fields = ('id', 'username', 'first_name', 'last_name', 'email', 'password', 'password_repeat')

    def validate(self, attrs: dict) -> dict:
        """Метод проверяет, совпадают ли введенные пароли"""
        if attrs['password'] != attrs['password_repeat']:
            raise ValidationError({'password_repeat': 'Passwords must match'})
        return attrs

    def create(self, validated_data: dict) -> User:
        """Проверяет, что пользователь с таким именем уже не существует"""
        if User.objects.filter(username=validated_data['username']).exists():
            raise serializers.ValidationError({'username': 'This username is already taken.'})
        del validated_data['password_repeat']
        validated_data['password'] = make_password(validated_data['password'])
        return super().create(validated_data)


class LoginSerializer(serializers.ModelSerializer):
    """Класс модели сериализатора для проверки данных пользователя на входе"""
    username = serializers.CharField(required=True)
    password = PasswordField(required=True)

    class Meta:
        model = User
        fields = ('id', 'username', 'password', 'first_name', 'last_name', 'email')
        read_only_fields = ('id', 'first_name', 'last_name', 'email')

    def validate(self, data):
        """Метод проводит аутентификацию пользователя"""
        username = data.get('username')
        password = data.get('password')

        if not (user := authenticate(
                username=username,
                password=password,
        )):
            raise AuthenticationFailed('Invalid username or password.')

        data['user'] = user
        return data


class ProfileSerializer(serializers.ModelSerializer):
    """Класс модели сериализатора пользователя"""

    class Meta:
        model = User
        fields = ('id', 'username', 'first_name', 'last_name', 'email')


class UpdatePasswordSerializer(serializers.Serializer):
    """Класс модели сериализатора для смены пароля пользователя"""
    old_password = serializers.CharField(required=True, style={'input_type': 'password'}, write_only=True)
    new_password = PasswordField(required=True)

    def validate_old_password(self, old_password: str) -> str:
        """Метод проверяет, совпадает ли значение поля ['old_password'] с действующим паролем"""
        if not self.instance.check_password(old_password):
            raise ValidationError('Password is incorrect')
        return old_password

    def validate_new_password(self, new_password: str) -> str:
        """Метод проверяет, отличается ли новый пароль от старого"""
        if self.instance.check_password(new_password):
            raise serializers.ValidationError('New password must be different from the old one.')
        return new_password

    def create(self, validated_data) -> User:
        raise NotImplementedError

    def update(self, instance: User, validated_data: dict) -> User:
        """Метод хэширует значение поля ['new_password'] и обновляет пароль пользователя в БД"""
        instance.set_password(validated_data['new_password'])
        instance.save(update_fields=('password',))
        return instance


class FriendSerializer(serializers.ModelSerializer):
    """Сериализатор для модели Friend"""
    friend_username = serializers.ReadOnlyField(source='friend.username')
    friend_email = serializers.ReadOnlyField(source='friend.email')

    class Meta:
        model = User
        fields = ['id', 'friend_username', 'friend_email', 'created_at']


class FriendRequestSerializer(serializers.ModelSerializer):
    """ Сериализатор для модели FriendRequest"""

    class Meta:
        model = FriendRequest
        fields = '__all__'


class UserSerializer(serializers.ModelSerializer):
    friends = FriendSerializer(many=True, read_only=True)
    url = serializers.SerializerMethodField()

    class Meta:
        model = User
        fields = ['id', 'username', 'email', 'first_name', 'last_name', 'friends', 'url']

    def get_url(self, obj):
        request = self.context.get('request')
        if request is None:
            return None
        return request.build_absolute_uri(reverse('user-detail', args=[obj.id]))
