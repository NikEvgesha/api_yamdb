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

    # username, first_name, last_name:
    # ограничения из документации совпадают с базовой моделью

    email = models.EmailField(
        'Е-мейл',
        blank=False,
        unique=True,
        max_length=254
    )
    role = models.CharField(
        verbose_name='Роль',
        choices=ROLE_CHOICES,
        max_length=20,
        default=USER
    )
    bio = models.TextField(
        'Биография',
        blank=True
    )
    confirmation_code = models.TextField(
        'Код подтверждения',
        blank=True,
        null=True
    )
    password = None

    def __str__(self):
        return self.username
