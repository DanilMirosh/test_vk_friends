from django.contrib.auth import login, logout
from rest_framework import generics, permissions, status
from rest_framework.response import Response

from .models import User, FriendRequest
from .serializers import (CreateUserSerializer, LoginSerializer, ProfileSerializer, UpdatePasswordSerializer,
                          FriendRequestSerializer, UserSerializer)


class SignupView(generics.CreateAPIView):
    """Ручка для регистрации нового пользователя"""
    serializer_class = CreateUserSerializer


class LoginView(generics.CreateAPIView):
    """Ручка для входа пользователя"""
    serializer_class = LoginSerializer

    def create(self, request, *args, **kwargs):
        """Метод производит вход(login) пользователя"""
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        user = serializer.validated_data['user']
        login(request=self.request, user=user)
        return Response(serializer.data, status=status.HTTP_200_OK)


class ProfileView(generics.RetrieveUpdateDestroyAPIView):
    """Ручка для отображения, редактирования и выхода пользователя"""
    queryset = User.objects.all()
    serializer_class = ProfileSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_object(self):
        """Метод возвращает объект пользователя из БД"""
        return self.request.user

    def perform_destroy(self, instance):
        """Метод производит выход(logout) пользователя"""
        instance.delete()
        logout(self.request)


class UpdatePasswordView(generics.UpdateAPIView):
    """Ручка для смены пароля пользователя"""
    permission_classes = [permissions.IsAuthenticated]
    serializer_class = UpdatePasswordSerializer

    def get_object(self):
        """Метод возвращает объект пользователя из БД"""
        return self.request.user


class FriendsView(generics.ListAPIView):
    """Представление для просмотра списка друзей текущего пользователя"""
    serializer_class = UserSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        """Метод возвращает список друзей текущего пользователя"""
        return self.request.user.friends.all()


class FriendRequestsView(generics.ListCreateAPIView):
    """Представление для просмотра списка входящих/исходящих запросов на дружбу и создания нового запроса"""
    serializer_class = FriendRequestSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        """Метод возвращает список входящих/исходящих запросов на дружбу текущего пользователя"""
        return FriendRequest.objects.filter(to_user=self.request.user).order_by('-created_at')

    def perform_create(self, serializer):
        """Метод создает новый запрос на дружбу"""
        serializer.save(from_user=self.request.user)

