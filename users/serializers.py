from django.contrib.auth import authenticate, get_user_model
from django.contrib.auth.hashers import make_password
from django.contrib.auth.password_validation import validate_password
from rest_framework import serializers
from rest_framework.exceptions import (AuthenticationFailed, ValidationError)

from .models import User, Friendship


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
        fields = ('id', 'username', 'password', 'password_repeat')

    def validate(self, attrs: dict) -> dict:
        """Метод проверяет, совпадают ли введенные пароли"""
        if attrs['password'] != attrs['password_repeat']:
            raise ValidationError({'password_repeat': 'Passwords must match'})
        return attrs

    def create(self, validated_data: dict) -> User:
        """Метод удаляет значение поля [password_repeat], хэширует пароль и создает пользователя"""

        del validated_data['password_repeat']
        validated_data['password'] = make_password(validated_data['password'])
        return super().create(validated_data)


class LoginSerializer(serializers.ModelSerializer):
    """Класс модели сериализатора для проверки данных пользователя на входе"""
    username = serializers.CharField(required=True)
    password = PasswordField(required=True)

    class Meta:
        model = User
        fields = ('id', 'username', 'password')
        read_only_fields = ('id', 'username')

    def create(self, validated_data: dict) -> User:
        """Метод проводит аутентификацию пользователя"""
        if not (user := authenticate(
                username=validated_data['username'],
                password=validated_data['password'],
        )):
            raise AuthenticationFailed
        return user


class ProfileSerializer(serializers.ModelSerializer):
    """Класс модели сериализатора пользователя"""

    class Meta:
        model = User
        fields = ('id', 'username')


class UpdatePasswordSerializer(serializers.Serializer):
    """Класс модели сериализатора для смены пароля пользователя"""
    old_password = serializers.CharField(required=True, style={'input_type': 'password'}, write_only=True)
    new_password = PasswordField(required=True)

    def validate_old_password(self, old_password: str) -> str:
        """Метод проверяет, совпадает ли значение поля ['old_password'] с действующим паролем"""
        if not self.instance.check_password(old_password):
            raise ValidationError('Password is incorrect')
        return old_password

    def create(self, validated_data) -> User:
        raise NotImplementedError

    def update(self, instance: User, validated_data: dict) -> User:
        """Метод хэширует значение поля ['new_password'] и обновляет пароль пользователя в БД"""
        instance.set_password(validated_data['new_password'])
        instance.save(update_fields=('password',))
        return instance


class UserFriendshipSerializer(serializers.ModelSerializer):
    """Сериализатор для друзей пользователя"""
    friend = serializers.StringRelatedField()

    class Meta:
        model = Friendship
        fields = ('friend',)


class FriendRequestSerializer(serializers.ModelSerializer):
    """Сериализатор для создания запроса на добавление в друзья"""
    from_user = serializers.ReadOnlyField(source='from_user.username')
    to_user = serializers.ReadOnlyField(source='to_user.username')

    class Meta:
        model = Friendship
        fields = ['id', 'from_user', 'to_user', 'status']
        read_only_fields = ['id', 'from_user', 'to_user', 'status']

    def create(self, validated_data):
        to_user = get_user_model().objects.get(username=validated_data['to_user'])
        from_user = self.context['request'].user
        friendship_1 = Friendship(from_user=from_user, to_user=to_user, status=Friendship.STATUS_CHOICES[0][0])
        friendship_2 = Friendship(from_user=to_user, to_user=from_user, status=Friendship.STATUS_CHOICES[0][0])
        friendship_1.save()
        friendship_2.save()
        return friendship_1


class FriendStatusSerializer(serializers.ModelSerializer):
    """Сериализатор для принятия/отклонения запроса на добавление в друзья"""
    status = serializers.ChoiceField(choices=Friendship.STATUS_CHOICES)

    class Meta:
        model = Friendship
        fields = ('status',)


class FriendshipSerializer(serializers.ModelSerializer):
    """Сериализатор для удаления друга"""

    class Meta:
        model = Friendship
        fields = ()
