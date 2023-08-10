from django.http import FileResponse
from django.shortcuts import get_object_or_404
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework import status, permissions, viewsets
from rest_framework.decorators import action
from rest_framework.generics import ListAPIView
from rest_framework.response import Response
from rest_framework.views import APIView

from api.filters import IngredientsFilterSet, RecipeFilterSet
from core.utils import get_pdf_shopping_list
from recipes.models import (
    Ingredient, Recipe, ShoppingCart, Subscribe, Tag)
from users.models import User
from .paginators import CustomPagination
from .permissions import IsAuthorOrAdmin
from .serializers import (
    CartSerializer,
    FavoriteSerializer,
    IngredientSeriaizer,
    RecipeCreateSerializer,
    RecipeShowSerializer,
    SubscribeSerializer,
    TagSeriaizer,
)


class TagViewSet(viewsets.ModelViewSet):
    """Вьюсет модели Тегов."""

    queryset = Tag.objects.all()
    serializer_class = TagSeriaizer
    pagination_class = None
    permission_classes = [permissions.AllowAny]


class IngredientViewSet(viewsets.ModelViewSet):
    """Вьюсет модели Ингредиентов."""

    queryset = Ingredient.objects.all()
    serializer_class = IngredientSeriaizer
    pagination_class = None
    filter_backends = [DjangoFilterBackend]
    filterset_class = IngredientsFilterSet
    permission_classes = [permissions.AllowAny]


class RecipeViewSet(viewsets.ModelViewSet):
    """
    Вьюсет модели Рецептов с дополнительными действиями
    относительно ендпойнтов:
        /favorite
        /shopping_cart
        /download_shopping_cart
    """

    queryset = Recipe.objects.all()
    serializer_class = RecipeShowSerializer
    pagination_class = CustomPagination
    filter_backends = [DjangoFilterBackend]
    filterset_class = RecipeFilterSet
    permission_classes = [IsAuthorOrAdmin]
    http_method_names = ['get', 'post', 'patch', 'delete']

    def get_serializer_class(self):
        if self.request.method in ('POST', 'PATCH'):
            return RecipeCreateSerializer
        return RecipeShowSerializer

    def perform_create(self, serializer):
        serializer.save(author=self.request.user)

    @action(
        detail=True,
        methods=['POST', 'DELETE'],
        url_name='favorite',
        url_path='favorite',
        permission_classes=[permissions.IsAuthenticated]
    )
    def favorite(self, request, pk=None):
        user = request.user
        recipe = get_object_or_404(Recipe, pk=pk)
        if request.method == 'POST':
            context = {'request': request}
            data = {
                'user': user.pk,
                'recipe': recipe.pk,
            }
            serializer = FavoriteSerializer(data=data, context=context)
            serializer.is_valid(raise_exception=True)
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)

        favorite = recipe.is_favorited.filter(user=user).first()
        if not favorite:
            return Response(
                {'errors': 'Такого рецепта в избранном нет'},
                status=status.HTTP_400_BAD_REQUEST
            )
        favorite.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)

    @action(
        detail=True,
        methods=['POST', 'DELETE'],
        url_name='shopping_cart',
        url_path='shopping_cart',
        permission_classes=[permissions.IsAuthenticated]
    )
    def shopping_cart(self, request, pk=None):
        user = request.user
        recipe = get_object_or_404(Recipe, pk=pk)
        if request.method == 'POST':
            context = {'request': request}
            data = {
                'user': user.pk,
                'recipe': recipe.pk,
            }
            serializer = CartSerializer(data=data, context=context)
            serializer.is_valid(raise_exception=True)
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)

        else:
            if not recipe.in_shopping_cart.filter(user=user).exists():
                return Response(
                    {'errors': 'Рецепта в корзине нет'},
                    status=status.HTTP_400_BAD_REQUEST
                )
            cart = get_object_or_404(ShoppingCart, user=user, recipe=recipe)
            cart.delete()
            return Response(status=status.HTTP_204_NO_CONTENT)

    @action(
        detail=False,
        methods=["GET"],
        url_name='download_shopping_cart',
        url_path='download_shopping_cart',
        permission_classes=[permissions.IsAuthenticated]
    )
    def download_shopping_cart(self, request):
        buffer = get_pdf_shopping_list(request)

        return FileResponse(
            buffer, as_attachment=True, filename='your_shopping_cart.pdf')


class SubscribtionsApiView(ListAPIView):
    """
    Вьюсет модели Подписок, вызываемый
    ендпойнтом '/subscriptions'
    """

    queryset = User.objects.all()
    serializer_class = SubscribeSerializer
    permission_classes = [permissions.IsAuthenticated]
    pagination_class = CustomPagination

    def get_queryset(self):
        user = self.request.user
        return User.objects.filter(subscribed__user=user)


class SubscribeApiView(APIView):
    """
    Вьюсет, обрабатывающий добавление/удаление подписки.
    """

    permission_classes = [permissions.IsAuthenticated]

    def post(self, request, id=None):
        user = request.user
        author = get_object_or_404(User, pk=id)
        data = {'recipes': []}
        context = {'user': user, 'author': author}
        serializer = SubscribeSerializer(author, data=data, context=context)
        serializer.is_valid(raise_exception=True)
        subscription = Subscribe(user=user, author=author)
        subscription.save()

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
