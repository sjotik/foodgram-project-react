from django.contrib.auth import get_user_model
from django.db import models

from foodgram_backend.settings import LEN_LIMIT

User = get_user_model()


class Tag(models.Model):
    name = models.CharField('Название', max_length=200, blank=False)
    color = models.CharField('Цвет', max_length=7, blank=False)
    slug = models.SlugField('Slug', max_length=200, unique=True)

    class Meta:
        verbose_name = 'Тег'
        verbose_name_plural = 'Теги'
        ordering = ('-id',)

    def __str__(self) -> str:
        return self.name


class Ingredient(models.Model):
    name = models.CharField(
        'Название', max_length=200, unique=True, blank=False)
    measurement_unit = models.CharField('Единицы измерения', max_length=5)

    class Meta:
        verbose_name = 'Ингредиент'
        verbose_name_plural = 'Ингредиенты'
        ordering = ('-id',)

    def __str__(self) -> str:
        return self.name


class Recipe(models.Model):
    name = models.CharField('Название', max_length=200, blank=False)
    text = models.TextField('Описание', blank=False)
    image = models.ImageField(
        'Изображение', null=True)
    cooking_time = models.PositiveIntegerField(
        'Время приготовления',)  # !!! must be >= 1
    author = models.ForeignKey(
        User,
        related_name='recipes',
        verbose_name='Автор',
        on_delete=models.CASCADE)
    tags = models.ManyToManyField(
        Tag, through='RecipeTag', verbose_name='Теги к рецепту')
    ingredients = models.ManyToManyField(
        Ingredient, through='RecipeIngredient', verbose_name='Ингредиенты')

    class Meta:
        verbose_name = 'Рецепт'
        verbose_name_plural = 'Рецепты'
        ordering = ('-id',)

    def __str__(self) -> str:
        return self.name[:LEN_LIMIT]


class RecipeTag(models.Model):
    recipe = models.ForeignKey(Recipe, on_delete=models.CASCADE)
    tag = models.ForeignKey(Tag, on_delete=models.CASCADE)

    class Meta:
        constraints = [
            models.UniqueConstraint(
                name='unique_recipe_tag',
                fields=['recipe', 'tag'],
            )
        ]

    def __str__(self) -> str:
        return f'{self.recipe} - {self.tag}'


class RecipeIngredient(models.Model):
    recipe = models.ForeignKey(Recipe, on_delete=models.CASCADE)
    ingredient = models.ForeignKey(Ingredient, on_delete=models.CASCADE)

    class Meta:
        constraints = [
            models.UniqueConstraint(
                name='unique_recipe_ingredient',
                fields=['recipe', 'ingredient'],
            )
        ]

    def __str__(self) -> str:
        return f'{self.ingredient} в {self.recipe}'


class Subscribe(models.Model):
    user = models.ForeignKey(
        User,
        verbose_name='Подписчик',
        on_delete=models.CASCADE,
        related_name='subscriber'
    )
    author = models.ForeignKey(
        User,
        verbose_name='Подписан на',
        on_delete=models.CASCADE,
        related_name='subscribed'
    )

    class Meta:
        verbose_name = "Подписка"
        verbose_name_plural = "Подписки"
        constraints = [
            models.UniqueConstraint(
                name='unique_couple_subscribe',
                fields=['user', 'author'],
            )
        ]

    def __str__(self):
        return (f'{self.user} подписан на {self.author}')


class Favorite(models.Model):
    user = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name='have_favorite',
        verbose_name='Пользователь'
    )
    recipe = models.ForeignKey(
        Recipe,
        on_delete=models.CASCADE,
        related_name='is_favorited',
        verbose_name='Рецепт'
    )

    class Meta:
        constraints = [models.UniqueConstraint(
            fields=['user', 'recipe'],
            name='unique_recipe_in_favorite'
        )]
        verbose_name = 'Избранное'
        verbose_name_plural = 'Избранные'
        ordering = ('-id',)

    def __str__(self) -> str:
        return (f'{self.recipe} в избранном у {self.user}')