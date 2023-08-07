from django.contrib.auth import get_user_model
from djoser.serializers import UserCreateSerializer, UserSerializer
from rest_framework import serializers

User = get_user_model()


class UserCustomSerializer(UserSerializer):
    """Сериализатор для модели User."""

    is_subscribed = serializers.SerializerMethodField()

    class Meta:
        model = User
        fields = (
            'email',
            'id',
            'username',
            'first_name',
            'last_name',
            'is_subscribed',
        )
        read_only_fields = ('is_subscribed',)

    def get_is_subscribed(self, obj: User) -> bool:
        """Поле проверки подписки на пользователя/автора."""

        if self.context.get('request'):
            user = self.context.get('request').user
            if not (user.is_anonymous or (user == obj)):
                return user.subscriber.filter(author=obj).exists()
        return False


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
