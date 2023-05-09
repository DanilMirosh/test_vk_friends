from django.contrib.auth.models import AbstractUser
from django.db import models


class User(AbstractUser):
    """Модель пользователя"""

    class Meta:
        """Мета-класс для корректного отображения полей пользователя в админ панели"""
        verbose_name = 'Пользователь'
        verbose_name_plural = 'Пользователи'
        # Добавим сортировку по полям
        ordering = ('username',)


class Friendship(models.Model):
    STATUS_CHOICES = (
        ('pending', 'Pending'),
        ('accepted', 'Accepted'),
        ('rejected', 'Rejected')
    )
    """Модель дружбы"""
    from_user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='initiated_friendships')
    to_user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='received_friendships')
    status = models.CharField(max_length=10, choices=STATUS_CHOICES, default='pending')

    class Meta:
        indexes = [
            models.Index(fields=['from_user', 'to_user'])
        ]

    def __str__(self):
        return f'{self.from_user.username} - {self.to_user.username}'


class FriendRequest(models.Model):
    """Модель заявки в друзья"""
    from_user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='sent_friend_requests')
    to_user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='received_friend_requests')
    created_at = models.DateTimeField(auto_now_add=True)
    status = models.IntegerField(choices=Friendship.STATUS_CHOICES, default=Friendship.STATUS_CHOICES[0][0])

    class Meta:
        unique_together = ('from_user', 'to_user')

    def accept(self):
        """Метод для принятия заявки в друзья"""
        from_user = self.from_user
        to_user = self.to_user
        Friendship.objects.create(from_user=from_user, to_user=to_user, status='accepted')
        Friendship.objects.create(from_user=to_user, to_user=from_user, status='accepted')
        self.delete()

    def reject(self):
        """Метод для отклонения заявки в друзья"""
        self.delete()
