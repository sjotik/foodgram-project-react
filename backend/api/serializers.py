from django.contrib.auth import get_user_model
from drf_extra_fields.fields import Base64ImageField
from rest_framework import serializers
from rest_framework.serializers import SerializerMethodField

from core.utils import ingredients_tags_action
from foodgram_backend.settings import MAX_VALUE, MIN_VALUE
from recipes.models import (
    Favorite, Ingredient, Recipe, RecipeIngredient, ShoppingCart, Tag)
from users.serializers import UserCustomSerializer


User = get_user_model()


class TagSeriaizer(serializers.ModelSerializer):
    """Сериализатор модели Тегов."""

    class Meta:
        model = Tag
        fields = ('id', 'name', 'color', 'slug')


class IngredientSeriaizer(serializers.ModelSerializer):
    """Сериализатор модели Ингредиентов."""

    class Meta:
        model = Ingredient
        fields = ('id', 'name', 'measurement_unit')


class RecipeIndredientSerializer(serializers.ModelSerializer):
    """
    Сериализатор для связывающей модели Рецепт-Ингредиент,
    для вывода данных.
    """
    id = serializers.ReadOnlyField(source='ingredient.id')
    name = serializers.ReadOnlyField(source='ingredient.name')
    measurement_unit = serializers.ReadOnlyField(
        source='ingredient.measurement_unit')

    class Meta:
        model = RecipeIngredient
        fields = ('id', 'name', 'measurement_unit', 'amount')


class RecipeIngredientAddSerializer(serializers.ModelSerializer):
    """
    Сериализатор для модели Рецепт-Ингредиент для добавления
    записи при создании рецепта.
    """
    id = serializers.PrimaryKeyRelatedField(
        source='ingredient',
        queryset=Ingredient.objects.all()
    )
    amount = serializers.IntegerField(
        max_value=MAX_VALUE, min_value=MIN_VALUE)

    class Meta:
        model = RecipeIngredient
        fields = ('id', 'amount')


class RecipeCreateSerializer(serializers.ModelSerializer):
    """
    Сериализатор для модели Рецептов для создания записи.
    """

    ingredients = RecipeIngredientAddSerializer(many=True)
    tags = serializers.PrimaryKeyRelatedField(
        queryset=Tag.objects.all(), many=True
    )
    image = Base64ImageField(required=False)
    cooking_time = serializers.IntegerField(
        max_value=MAX_VALUE, min_value=MIN_VALUE)

    class Meta:
        model = Recipe
        fields = (
            'ingredients', 'tags', 'image', 'name', 'text', 'cooking_time')

    def create(self, validated_data):
        ingredients = validated_data.pop('ingredients')
        tags = validated_data.pop('tags')
        recipe = Recipe.objects.create(**validated_data)

        ingredients_tags_action(recipe, ingredients, tags)

        return recipe

    def update(self, recipe, validated_data):
        recipe.name = validated_data.get('name', recipe.name)
        recipe.image = validated_data.get('image', recipe.image)
        recipe.text = validated_data.get('text', recipe.text)
        recipe.cooking_time = validated_data.get(
            'cooking_time', recipe.cooking_time)
        tags = validated_data.get('tags', recipe.tags)
        ingredients = validated_data.get('ingredients', recipe.ingredients)

        ingredients_tags_action(recipe, ingredients, tags)
        recipe.save()

        return recipe

    def to_representation(self, instance):
        request = self.context.get('request')
        context = {'request': request}
        return RecipeShowSerializer(instance, context=context).data


class RecipeShowSerializer(serializers.ModelSerializer):
    """
    Сериализатор модели Рецептов для вывода данных.
    """

    ingredients = RecipeIndredientSerializer(
        many=True, source='with_ingredients')
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
        user = self.context.get('request').user
        if user.is_anonymous:
            return False
        return obj.is_favorited.filter(user=user).exists()

    def get_is_in_shopping_cart(self, obj: Recipe) -> bool:
        user = self.context.get('request').user
        if user.is_anonymous:
            return False
        return obj.in_shopping_cart.filter(user=user).exists()


class RecipeShowShortSerializer(serializers.ModelSerializer):
    """
    Сериализатор модели Рецептов для вывода сокращенной информации.
    (для сериализатора модели Подписок)
    """

    class Meta:
        model = Recipe
        fields = ('id', 'name', 'image', 'cooking_time')
        read_only_fields = ('__all__',)


class SubscribeSerializer(serializers.ModelSerializer):
    """Сериализатор модели Подписок."""

    recipes = RecipeShowShortSerializer(many=True)
    recipes_count = SerializerMethodField()
    is_subscribed = SerializerMethodField()

    class Meta:
        model = User
        fields = (
            'email',
            'id',
            'username',
            'first_name',
            'last_name',
            'is_subscribed',
            'recipes',
            'recipes_count',
        )
        read_only_fields = ('__all__',)
        extra_kwargs = {
            'email': {'required': False},
            'username': {'required': False},
            'first_name': {'required': False},
            'last_name': {'required': False},
            'recipes': {'required': False},
        }

    def get_recipes_count(self, obj: User) -> int:
        """Поле количества рецептов автора."""
        return obj.recipes.count()

    def get_is_subscribed(self, obj: User) -> bool:
        """Поле проверки подписки на пользователя/автора."""

        # user = self.context.get('request').user
        user = self.context.get('user')
        if user.is_anonymous or (user == obj):
            return False
        return user.subscriber.filter(author=obj).exists()

    def validate(self, data):
        user = self.context['user']
        author = self.context['author']

        if user.subscriber.filter(author=author).exists():
            raise serializers.ValidationError(
                'Вы уже подписаны на этого автора')

        if user == author:
            raise serializers.ValidationError(
                'Невозможно подписаться на самого себя')

        return data


class FavoriteSerializer(serializers.ModelSerializer):
    """Сериализатор добавление в избранное с кастомным выводом"""

    class Meta:
        model = Favorite
        fields = ['user', 'recipe']

    def validate(self, attrs):
        request = self.context.get('request')
        user = attrs['user']
        recipe = attrs['recipe']

        if request.method == 'POST':
            if recipe.is_favorited.filter(user=user).exists():
                raise serializers.ValidationError('Рецепт уже в избранном')
        return super().validate(attrs)

    def create(self, validated_data):
        return Favorite.objects.create(**validated_data)

    def to_representation(self, instance):
        request = self.context.get('request')
        context = {'request': request}
        return RecipeShowSerializer(instance.recipe, context=context).data


class CartSerializer(serializers.ModelSerializer):
    """Сериализатор добавление в избранное с кастомным выводом"""

    class Meta:
        model = ShoppingCart
        fields = ['user', 'recipe']

    def validate(self, attrs):
        request = self.context.get('request')
        user = attrs['user']
        recipe = attrs['recipe']

        if request.method == 'POST':
            if recipe.in_shopping_cart.filter(user=user).exists():
                raise serializers.ValidationError('Рецепт уже в КОРЗИНЕ')
        return super().validate(attrs)

    def create(self, validated_data):
        return ShoppingCart.objects.create(**validated_data)

    def to_representation(self, instance):
        request = self.context.get('request')
        context = {'request': request}
        return RecipeShowShortSerializer(instance.recipe, context=context).data
