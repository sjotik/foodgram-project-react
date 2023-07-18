from django.contrib.auth.models import AbstractUser
from django.contrib.auth.validators import UnicodeUsernameValidator
from django.db import models


USER_ROLES = (
    ('user', 'user'),
    ('admin', 'admin'),
)


class User(AbstractUser):
    username = models.CharField(
        verbose_name='Имя пользователя',
        max_length=150,
        unique=True,
        blank=False,
        validators=[UnicodeUsernameValidator()],
        error_messages={
            'unique': "Такой пользователь уже существует.",
        },
    )
    email = models.EmailField(
        verbose_name='Email',
        max_length=254,
        blank=False,
        unique=True,
        error_messages={
            'unique': "Такой email уже зарегистрирован.",
        },
    )
    first_name = models.CharField(
        verbose_name='Имя',
        max_length=150,
        blank=True,
    )

    last_name = models.CharField(
        verbose_name='Фамилия',
        max_length=150,
        blank=True,
    )

    role = models.CharField(
        verbose_name='Роль',
        max_length=15,
        choices=USER_ROLES,
        default='user',
    )

    class Meta:
        verbose_name = 'Пользователь'
        verbose_name_plural = 'Пользователи'
        ordering = ('id',)

        constraints = [
            models.UniqueConstraint(
                fields=['username', 'email'],
                name='unique_username_email',
            ),
        ]

    @property
    def is_admin(self):
        return self.role == 'admin'

    def __str__(self):
        return self.username
