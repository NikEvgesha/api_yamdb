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

    @property
    def is_user(self):
        return self.role == self.USER

    @property
    def is_admin(self):
        return self.role == self.ADMIN

    @property
    def is_moderator(self):
        return self.role == self.MODERATOR

    def __str__(self):
        return self.username
