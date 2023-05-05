from django.contrib.auth.models import AbstractUser


class User(AbstractUser):
    """Модель пользователя"""

    class Meta:
        """Мета-класс для корректного отображения полей пользователя в админ панели"""
        verbose_name = 'Пользователь'
        verbose_name_plural = 'Пользователи'
        # Добавим сортировку по полям
        ordering = ('username',)
