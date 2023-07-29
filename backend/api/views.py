from django.shortcuts import get_object_or_404
from rest_framework import status, viewsets
from rest_framework.decorators import action
from rest_framework.generics import ListAPIView
from rest_framework.pagination import PageNumberPagination
from rest_framework.response import Response
from rest_framework.views import APIView

from recipes.models import Ingredient, Recipe, Subscribe, Tag
# from users.views import UserViewSet
from users.models import User
from .serializers import (
    IngredientSeriaizer,
    RecipeShowSerializer,
    SubscribeSerializer,
    TagSeriaizer,
    UserCustomSerializer
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

    def post(self, request, id):
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

    def delete(self, request, id):
        user = request.user
        author = get_object_or_404(User, pk=id)

        if not user.subscriber.filter(author=author).exists():
            return Response(
                {'errors': 'Такой подписки не существует'},
                status=status.HTTP_400_BAD_REQUEST)

        subscription = get_object_or_404(Subscribe, user=user, author=author)
        subscription.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)
