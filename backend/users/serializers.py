from rest_framework import serializers

from .models import User


class UserSerializer(serializers.ModelSerializer):
    """Сериализатор для модели User."""

    class Meta:
        model = User
        fields = (
            'username',
            'email',
            'first_name',
            'last_name',
            'bio',
            'role'
        )

    def validate_username(self, value):
        """
        Валидация 'me'.
        """
        if value == 'me':
            raise serializers.ValidationError(
                "Имя \'me\' зарезервировано системой.")
        return value


class UserSignupSerializer(serializers.Serializer):
    """Сериализатор добавления пользователя и отправки кода."""

    username = serializers.RegexField(
        regex=r'^[\w.@+-]+\Z',
        error_messages={
            'invalid': ('Имя пользователя содержит недопустимый символ.')
        },
        max_length=150,
        required=True
    )
    email = serializers.EmailField(required=True, max_length=254)

    def validate_username(self, value):
        """
        Валидация 'me'.
        """
        if value == 'me':
            raise serializers.ValidationError(
                "Имя \'me\' зарезервировано системой.")
        return value

    def create(self, validated_data):
        return User.objects.create_user(**validated_data)


class UserConfirmationCodeSerializer(serializers.Serializer):
    """Сериализатор подтверждения кода для получения токена."""

    username = serializers.CharField(required=True)
    confirmation_code = serializers.CharField(required=True)
