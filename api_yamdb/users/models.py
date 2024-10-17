from django.contrib.auth.models import AbstractUser
from django.db import models


class User(AbstractUser):
    USER = 'user'
    MODERATOR = 'moderator'
    ADMIN = 'admin'

    ROLE_CHOICES = [
        (USER, 'Пользователь'),
        (MODERATOR, 'Модератор'),
        (ADMIN, 'Администратор')
    ]
    role = models.CharField(
        verbose_name='Роль',
        choices=ROLE_CHOICES,
        max_length=20,
        default=USER
    )
    bio = models.TextField('Биография', blank=True)

    def __str__(self):
        return self.username
