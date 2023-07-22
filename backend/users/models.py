from django.contrib.auth.models import AbstractUser
from django.contrib.auth.validators import UnicodeUsernameValidator
from django.db import models


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
        blank=False,
    )
    last_name = models.CharField(
        verbose_name='Фамилия',
        max_length=150,
        blank=False,
    )
    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['username', 'first_name', 'last_name']

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
