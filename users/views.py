from django.shortcuts import render

from .models import User
from .serializers import (CreateUserSerializer, LoginSerializer, ProfileSerializer, UpdatePasswordSerializer)
from django.contrib.auth import login, logout
from rest_framework import generics, permissions, status
from rest_framework.response import Response


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
        login(request=self.request, user=serializer.save())
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
        logout(self.request)


class UpdatePasswordView(generics.UpdateAPIView):
    """Ручка для смены пароля пользователя"""
    permission_classes = [permissions.IsAuthenticated]
    serializer_class = UpdatePasswordSerializer

    def get_object(self):
        """Метод возвращает объект пользователя из БД"""
        return self.request.user
