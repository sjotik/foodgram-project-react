from django.contrib.auth import get_user_model
from drf_extra_fields.fields import Base64ImageField
from rest_framework import serializers
from rest_framework.serializers import SerializerMethodField

from recipes.models import Ingredient, Recipe, RecipeIngredient, RecipeTag, Tag
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


class RecipeIngredientAddSerializer(serializers.ModelSerializer):
    id = serializers.PrimaryKeyRelatedField(
        source='ingredient',
        queryset=Ingredient.objects.all()
    )

    class Meta:
        model = RecipeIngredient
        fields = ('id', 'amount')


class RecipeCreateSerializer(serializers.ModelSerializer):
    ingredients = RecipeIngredientAddSerializer(many=True)
    tags = serializers.PrimaryKeyRelatedField(
        queryset=Tag.objects.all(), many=True
    )
    image = Base64ImageField(required=False)

    class Meta:
        model = Recipe
        fields = (
            'ingredients', 'tags', 'image', 'name', 'text', 'cooking_time')

    def create(self, validated_data):
        ingredients = validated_data.pop('ingredients')
        tags = validated_data.pop('tags')
        recipe = Recipe.objects.create(**validated_data)

        for ingredient in ingredients:
            ingr_obj = ingredient['ingredient']
            amount = ingredient['amount']
            RecipeIngredient(
                recipe=recipe, ingredient=ingr_obj, amount=amount).save()

        for tag in tags:
            RecipeTag.objects.create(recipe=recipe, tag=tag)

        return recipe

    def update(self, recipe, validated_data):
        recipe.name = validated_data.get('name', recipe.name)
        recipe.image = validated_data.get('image', recipe.image)
        recipe.text = validated_data.get('text', recipe.text)
        recipe.cooking_time = validated_data.get(
            'cooking_time', recipe.cooking_time)
        if validated_data.get('tags'):
            tags = validated_data.pop('tags')
            recipe.with_tags.all().delete()
            for tag in tags:
                RecipeTag.objects.create(recipe=recipe, tag=tag)
        if validated_data.get('ingredients'):
            ingredients = validated_data.pop('ingredients', recipe)
            recipe.with_ingredients.all().delete()
            for ingredient in ingredients:
                ingr_obj = ingredient['ingredient']
                amount = ingredient['amount']
                RecipeIngredient(
                    recipe=recipe, ingredient=ingr_obj, amount=amount).save()
        recipe.save()

        return recipe

    def to_representation(self, instance):
        request = self.context.get('request')
        context = {'request': request}
        return RecipeShowSerializer(instance, context=context).data


class RecipeShowSerializer(serializers.ModelSerializer):
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
