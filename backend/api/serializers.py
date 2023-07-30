from django.contrib.auth import get_user_model
from rest_framework import serializers
from rest_framework.serializers import SerializerMethodField

from recipes.models import Ingredient, Recipe, RecipeIngredient, Tag
from users.serializers import UserCustomSerializer


User = get_user_model()


class TagSeriaizer(serializers.ModelSerializer):
    class Meta:
        model = Tag
        fields = ('id', 'name', 'color', 'slug')


class IngredientSeriaizer(serializers.ModelSerializer):
    class Meta:
        model = Ingredient
        fields = ('id', 'name', 'measurement_unit')


class RecipeIndredientSerializer(serializers.ModelSerializer):
    id = serializers.ReadOnlyField(source='ingredient.id')
    name = serializers.ReadOnlyField(source='ingredient.name')
    measurement_unit = serializers.ReadOnlyField(
        source='ingredient.measurement_unit')

    class Meta:
        model = RecipeIngredient
        fields = ('id', 'name', 'measurement_unit', 'amount')


class RecipeShowSerializer(serializers.ModelSerializer):
    ingredients = RecipeIndredientSerializer(
        many=True, source='with_ingredient')
    tags = TagSeriaizer(many=True)
    author = UserCustomSerializer()
    is_favorited = SerializerMethodField()
    is_in_shopping_cart = SerializerMethodField()

    class Meta:
        model = Recipe
        fields = (
            'id',
            'tags',
            'author',
            'ingredients',
            'is_favorited',
            'is_in_shopping_cart',
            'name',
            'image',
            'text',
            'cooking_time'
        )
        read_only_fields = ('__all__',)

    def get_is_favorited(self, obj: Recipe) -> bool:
        user = self.context.get("request").user
        if user.is_anonymous:
            return False
        return obj.is_favorited.filter(user=user).exists()

    def get_is_in_shopping_cart(self, obj: Recipe) -> bool:
        user = self.context.get("request").user
        if user.is_anonymous:
            return False
        return obj.in_shopping_cart.filter(user=user).exists()


class RecipeShowShortSerializer(serializers.ModelSerializer):

    class Meta:
        model = Recipe
        fields = ('id', 'name', 'image', 'cooking_time')
        read_only_fields = ('__all__',)


class SubscribeSerializer(serializers.ModelSerializer):
    recipes = RecipeShowShortSerializer(many=True)
    recipes_count = SerializerMethodField()
    is_subscribed = SerializerMethodField()

    class Meta:
        model = User
        fields = (
            "email",
            "id",
            "username",
            "first_name",
            "last_name",
            "is_subscribed",
            "recipes",
            "recipes_count",
        )
        read_only_fields = ("__all__",)

    def get_recipes_count(self, obj: User) -> int:
        return obj.recipes.count()

    def get_is_subscribed(self, obj: User) -> bool:
        """Поле проверки подписки на пользователя/автора."""

        user = self.context.get("request").user
        if user.is_anonymous or (user == obj):
            return False
        return user.subscriber.filter(author=obj).exists()
