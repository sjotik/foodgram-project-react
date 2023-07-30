from django.shortcuts import get_object_or_404
from rest_framework import status, viewsets
from rest_framework.decorators import action, permission_classes
from rest_framework.generics import ListAPIView
from rest_framework.pagination import PageNumberPagination
from rest_framework.response import Response
from rest_framework.views import APIView

from recipes.models import Favorite, Ingredient, Recipe, Subscribe, Tag
# from users.views import UserViewSet
from users.models import User
from .serializers import (
    IngredientSeriaizer,
    RecipeShowSerializer,
    RecipeShowShortSerializer,
    SubscribeSerializer,
    TagSeriaizer,
    )


class TagViewSet(viewsets.ModelViewSet):
    queryset = Tag.objects.all()
    serializer_class = TagSeriaizer
    pagination_class = None


class IngredientViewSet(viewsets.ModelViewSet):
    queryset = Ingredient.objects.all()
    serializer_class = IngredientSeriaizer
    pagination_class = None


class RecipeViewSet(viewsets.ModelViewSet):
    queryset = Recipe.objects.all()
    serializer_class = RecipeShowSerializer
    # pagination_class = PageNumberPagination

    @action(
        detail=True,
        methods=['POST', 'DELETE'],
        url_name='favorite',
        url_path='favorite',
        # permission_classes=[]
    )
    def favorite(self, request, pk=None):
        user = request.user
        recipe = get_object_or_404(Recipe, pk=pk)
        if request.method == 'POST':
            if recipe.is_favorited.filter(user=user).exists():
                return Response(
                    {'errors': 'Рецепт уже в избранном'},
                    status=status.HTTP_400_BAD_REQUEST
                )
            favorite = Favorite(user=user, recipe=recipe)
            favorite.save()
            serializer = RecipeShowShortSerializer(recipe)
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        else:
            if not recipe.is_favorited.filter(user=user).exists():
                return Response(
                    {'errors': 'Такого рецепта в избранном нет'},
                    status=status.HTTP_400_BAD_REQUEST
                )
            favorite = get_object_or_404(Favorite, user=user, recipe=recipe)
            favorite.delete()
            return Response(status=status.HTTP_204_NO_CONTENT)


class SubscribtionsApiView(ListAPIView):
    queryset = User.objects.all()
    serializer_class = SubscribeSerializer
    # permission_classes = []
    # pagination_class = PageNumberPagination

    def get_queryset(self):
        user = self.request.user
        return User.objects.filter(subscribed__user=user)


class SubscribeApiView(APIView):

    # permission_classes = []

    def post(self, request, id=None):
        user = request.user
        author = get_object_or_404(User, pk=id)

        if user.subscriber.filter(author=author).exists():
            return Response(
                {'errors': 'Вы уже подписаны на этого автора'},
                status=status.HTTP_400_BAD_REQUEST)

        if user == author:
            return Response(
                {'errors': 'Невозможно подписаться на самого себя'},
                status=status.HTTP_400_BAD_REQUEST)

        subscription = Subscribe(user=user, author=author)
        subscription.save()
        serializer = SubscribeSerializer(author, context={'request': request})
        return Response(serializer.data, status=status.HTTP_201_CREATED)

    def delete(self, request, id=None):
        user = request.user
        author = get_object_or_404(User, pk=id)

        if not user.subscriber.filter(author=author).exists():
            return Response(
                {'errors': 'Такой подписки не существует'},
                status=status.HTTP_400_BAD_REQUEST)

        subscription = get_object_or_404(Subscribe, user=user, author=author)
        subscription.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)
