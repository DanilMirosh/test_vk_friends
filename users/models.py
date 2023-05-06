from django.contrib.auth.models import AbstractUser
from django.db import models


class User(AbstractUser):
    """Модель пользователя"""
    friends = models.ManyToManyField('self', blank=True)

    class Meta:
        """Мета-класс для корректного отображения полей пользователя в админ панели"""
        verbose_name = 'Пользователь'
        verbose_name_plural = 'Пользователи'
        # Добавим сортировку по полям
        ordering = ('username',)


class FriendRequest(models.Model):
    from_user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='friend_requests_sent')
    to_user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='friend_requests_received')
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.from_user.username} -> {self.to_user.username}"
