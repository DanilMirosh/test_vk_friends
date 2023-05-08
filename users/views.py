from django.contrib.auth import login, logout
from django.db.models import Q
from django.shortcuts import get_object_or_404
from rest_framework import generics, permissions, status
from rest_framework.response import Response

from .models import User, Friendship
from .serializers import (CreateUserSerializer, LoginSerializer, ProfileSerializer, UpdatePasswordSerializer,
                          UserFriendshipSerializer, FriendRequestSerializer, FriendStatusSerializer,
                          FriendshipSerializer)


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


class UserFriendshipView(generics.ListAPIView):
    """Представление для просмотра друзей пользователя"""
    serializer_class = UserFriendshipSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        """Получение списка друзей пользователя"""
        return Friendship.objects.filter(
            Q(from_user=self.request.user) | Q(to_user=self.request.user),
            status='accepted'
        ).select_related('to_user')


class FriendRequestView(generics.ListCreateAPIView):
    """Представление для создания и просмотра заявок в друзья"""
    serializer_class = FriendRequestSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        """Получение списка заявок в друзья пользователя"""
        return Friendship.objects.filter(
            to_user=self.request.user, status=Friendship.STATUS_CHOICES
        ).select_related('from_user', 'to_user')

    def perform_create(self, serializer):
        """Создание заявки в друзья"""
        to_user = get_object_or_404(User, username=self.request.data['to_user'])
        friendship_1 = Friendship.objects.create(from_user=self.request.user, to_user=to_user, status=Friendship.STATUS_CHOICES)
        friendship_2 = Friendship.objects.create(from_user=to_user, to_user=self.request.user, status=Friendship.STATUS_CHOICES)
        friendship_1.save()
        friendship_2.save()
        serializer.instance = friendship_1


class FriendRequestDetailView(generics.UpdateAPIView):
    """Представление для принятия или отклонения заявки в друзья"""
    serializer_class = FriendStatusSerializer
    permission_classes = [permissions.IsAuthenticated]
    lookup_url_kwarg = 'username'

    def dispatch(self, request, *args, **kwargs):
        return super().dispatch(request, *args, **kwargs)

    def get_object(self):
        """Получение объекта заявки в друзья"""
        from_user = get_object_or_404(User, username=self.kwargs['username'])
        to_user = get_object_or_404(User, username=self.request.data.get('to_user'))
        friendship = get_object_or_404(
            Friendship, from_user=from_user, to_user=to_user, status=Friendship.STATUS_CHOICES[0]
        )
        return friendship

    def check_friendship(self, from_user, to_user):
        """Проверка, что пользователи не являются уже друзьями"""
        if Friendship.objects.filter(
                from_user=from_user,
                to_user=to_user,
                status=Friendship.STATUS_CHOICES[1]
        ).exists():
            return Response({'detail': 'Пользователи уже друзья'}, status=status.HTTP_400_BAD_REQUEST)

    def update(self, request, *args, **kwargs):
        """Принятие или отклонение заявки в друзья"""
        friendship = self.get_object()
        self.check_friendship(friendship.from_user, friendship.to_user)

        serializer = self.get_serializer(friendship, data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save()

        if friendship.status == Friendship.STATUS_CHOICES[1]:
            if Friendship.objects.filter(
                    from_user=friendship.to_user,
                    to_user=friendship.from_user,
                    status=Friendship.STATUS_CHOICES[1]
            ).exists():
                return Response

class FriendshipDetailView(generics.DestroyAPIView):
    """Представление для удаления дружбы"""
    serializer_class = FriendshipSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_object(self):
        """Получение объекта дружбы"""
        friendship = get_object_or_404(Friendship, from_user=self.request.user,
                                       to_user__username=self.kwargs['username'], status=Friendship.STATUS_CHOICES)
        return friendship

    def delete(self, request, *args, **kwargs):
        friendship = self.get_object()
        friendship.status = Friendship.STATUS_CHOICES
        friendship.save()
        return Response(status=status.HTTP_204_NO_CONTENT)
