from django.contrib.auth import get_user_model
from djoser.serializers import UserCreateSerializer, UserSerializer


User = get_user_model()


class UserCustomSerializer(UserSerializer):
    """Сериализатор для модели User."""

    class Meta:
        model = User
        fields = (
            'email',
            'id',
            'username',
            'first_name',
            'last_name',
        )


class UserRegistrySerializer(UserCreateSerializer):
    """Сериализатор для регистрации пользователя."""

    class Meta:
        model = User
        fields = (
            'email',
            'id',
            'username',
            'first_name',
            'last_name',
            'password',
        )
