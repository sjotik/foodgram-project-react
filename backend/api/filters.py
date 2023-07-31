from django_filters.rest_framework import (
    BooleanFilter, FilterSet, ModelMultipleChoiceFilter)

from recipes.models import Recipe, Tag


class RecipeFilterSet(FilterSet):
    is_favorited = BooleanFilter(
        field_name='is_favorited', method='filter_is_favorited')
    is_in_shopping_cart = BooleanFilter(
        field_name='is_in_shopping_cart', method='filter_is_in_shopping_cart')
    tags = ModelMultipleChoiceFilter(
        field_name='tags__slug',
        to_field_name='slug',
        queryset=Tag.objects.all(),
    )

    class Meta:
        model = Recipe
        fields = ['is_favorited', 'is_in_shopping_cart', 'tags']

    def filter_is_favorited(self, queryset, name, value):
        if self.request.user.is_authenticated and value:
            queryset = queryset.filter(is_favorited__user=self.request.user)
        return queryset

    def filter_is_in_shopping_cart(self, queryset, name, value):
        if self.request.user.is_authenticated and value:
            queryset = queryset.filter(
                in_shopping_cart__user=self.request.user)
        return queryset
