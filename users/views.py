from django.contrib.auth import login, logout
from django.db.models import Q
from django.shortcuts import get_object_or_404
from rest_framework import generics, permissions, status
from rest_framework.exceptions import ValidationError
from rest_framework.response import Response
from .models import User, Friendship
from .serializers import (CreateUserSerializer, LoginSerializer, ProfileSerializer, UpdatePasswordSerializer,
                          UserFriendshipSerializer, FriendRequestSerializer, FriendStatusSerializer,
                          FriendshipSerializer)


class SignupView(generics.CreateAPIView):
    """Представление для регистрации нового пользователя"""
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
    """Представление для отображения, редактирования и выхода пользователя"""
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
    """Представление для смены пароля пользователя"""
    permission_classes = [permissions.IsAuthenticated]
    serializer_class = UpdatePasswordSerializer

    def get_object(self):
        """Метод возвращает объект пользователя из БД"""
        return self.request.user


class FriendRequestView(generics.ListCreateAPIView):
    """Представление для создания и просмотра заявок в друзья"""
    serializer_class = FriendRequestSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        """Получение списка заявок в друзья пользователя"""
        return Friendship.objects.filter(
            to_user=self.request.user, status=Friendship.STATUS_CHOICES[0]
        ).select_related('from_user', 'to_user')

    def perform_create(self, serializer):
        """Создание заявки в друзья"""
        to_user = get_object_or_404(User, username=self.request.data['to_user'])

        # Проверяем, существует ли уже заявка в обоих направлениях
        friendship_1 = Friendship.objects.filter(from_user=self.request.user, to_user=to_user).first()
        if friendship_1 is not None:
            serializer.instance = friendship_1
            return

        friendship_2 = Friendship.objects.filter(from_user=to_user, to_user=self.request.user).first()
        if friendship_2 is not None:
            serializer.instance = friendship_2
            return

        # Если заявки не существует, то создаем ее
        friendship_1 = Friendship.objects.create(from_user=self.request.user, to_user=to_user,
                                                 status=Friendship.STATUS_CHOICES[0])
        serializer.instance = friendship_1


class UserFriendshipView(generics.ListAPIView):
    """Представление для просмотра друзей пользователя"""
    serializer_class = UserFriendshipSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        """Получение списка друзей пользователя"""
        return Friendship.objects.filter(
            Q(from_user=self.request.user) | Q(to_user=self.request.user),
            status=Friendship.STATUS_CHOICES[1]
        )


class FriendRequestDetailView(generics.UpdateAPIView):
    """Представление для принятия или отклонения заявки в друзья"""

    serializer_class = FriendStatusSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_object(self, queryset=None):
        username = self.kwargs.get('username')
        return get_object_or_404(User, username=username)

    def patch(self, request, *args, **kwargs):
        """Принятие или отклонение заявки в друзья"""
        friend = self.get_object()
        friendship = get_object_or_404(Friendship, from_user=friend, to_user=request.user,
                                       status=Friendship.STATUS_CHOICES[0])

        serializer = self.get_serializer(friendship, data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save()

        if friendship.status == Friendship.STATUS_CHOICES[1]:
            if Friendship.objects.filter(from_user=friend, to_user=request.user,
                                         status=Friendship.STATUS_CHOICES[1]).exists():
                return Response({'detail': 'Заявка в друзья уже отправлена и принята'},
                                status=status.HTTP_400_BAD_REQUEST)

        return Response(serializer.data, status=status.HTTP_200_OK)

    def check_object_permissions(self, request, obj):
        """Проверка, что пользователи не являются уже друзьями"""
        if Friendship.objects.filter(from_user=request.user, to_user=obj, status=Friendship.STATUS_CHOICES[1]).exists():
            raise ValidationError({'detail': 'Пользователи уже друзья'})


class FriendshipDetailView(generics.DestroyAPIView):
    """
    Представление для удаления дружбы. При удалении дружбы создаются новые записи в таблице Friendship,
    чтобы пользователи могли отправлять друг другу новые заявки в друзья.
    """
    serializer_class = FriendshipSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_object(self):
        """
        Получение объекта дружбы. Должен вернуть объект дружбы со статусом "друзья" между текущим пользователем
        и пользователем, имя которого передано в URL.
        """
        friendship = get_object_or_404(Friendship, from_user=self.request.user,
                                       to_user__username=self.kwargs['username'], status=Friendship.STATUS_CHOICES[1])
        return friendship

    def delete(self, request, *args, **kwargs):
        """
        Удаление дружбы. Сначала меняем статус дружбы на "не друзья", а затем создаем новую запись в таблице
        Friendship, чтобы пользователи могли отправлять друг другу новые заявки в друзья.
        """
        friendship = self.get_object()
        friendship.status = Friendship.STATUS_CHOICES[0]
        friendship.save()

        # Создаем новую запись в таблице Friendship, чтобы пользователи могли отправлять друг другу новые заявки в друзья.
        new_friendship = Friendship(from_user=friendship.from_user, to_user=friendship.to_user)
        new_friendship.save()

        return Response(status=status.HTTP_204_NO_CONTENT)


