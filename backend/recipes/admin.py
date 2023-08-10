from django.contrib import admin
from django.utils.safestring import mark_safe, SafeString

from foodgram_backend.settings import MIN_VALUE
from .models import (
    Favorite, Ingredient, Recipe, RecipeIngredient, RecipeTag, Subscribe, Tag)


class TagInline(admin.TabularInline):
    model = RecipeTag
    extra = 0
    verbose_name = 'Тег рецепта'
    verbose_name_plural = 'Теги рецепта'


class IngredientInline(admin.TabularInline):
    model = RecipeIngredient
    extra = 0
    min_num = MIN_VALUE
    verbose_name = 'Ингредиент рецепта'
    verbose_name_plural = 'Ингредиенты рецепта'


@admin.register(Tag)
class TagAdmin(admin.ModelAdmin):
    list_display = ('name', 'slug', 'color')
    search_fields = ('name', 'slug')
    list_filter = ('name',)
    list_editable = ('color',)
    empty_value_display = '-пусто-'


@admin.register(Ingredient)
class IngredientAdmin(admin.ModelAdmin):
    list_display = ('id', 'name', 'measurement_unit')
    search_fields = ('name',)
    list_filter = ('measurement_unit',)
    empty_value_display = '-пусто-'


@admin.register(Recipe)
class RecipeAdmin(admin.ModelAdmin):
    list_display = (
        'id', 'name', 'author', 'cooking_time', 'get_favorited', 'get_image',)
    readonly_fields = ('author',)
    list_display_links = ('name',)
    search_fields = ('name', 'tags', 'author')
    list_filter = ('name', 'tags__name', 'author__username')
    inlines = (TagInline, IngredientInline)

    def get_favorited(self, obj: Recipe) -> int:
        return obj.is_favorited.count()

    get_favorited.short_description = 'В избранном'

    def get_image(self, obj: Recipe) -> SafeString:
        if obj.image:
            return mark_safe(f'<img src={obj.image.url} width=50>')

    get_image.short_description = 'Изображение'

    def save_model(self, request, obj, form, change):
        obj.author = request.user
        super().save_model(request, obj, form, change)


@admin.register(Subscribe)
class SubscribeAdmin(admin.ModelAdmin):
    list_display = ('id', 'user', 'author')


@admin.register(Favorite)
class FavoriteAdmin(admin.ModelAdmin):
    list_display = ('id', 'user', 'recipe')


@admin.register(RecipeIngredient)
class RecipeIngredientAdmin(admin.ModelAdmin):
    list_display = ('id', 'recipe', 'ingredient', 'amount')


@admin.register(RecipeTag)
class RecipeTagAdmin(admin.ModelAdmin):
    list_display = ('id', 'recipe', 'tag')
