from rest_framework import viewsets
from rest_framework.pagination import PageNumberPagination

from recipes.models import Tag
from .serializers import TagSeriaizer


class TagViewSet(viewsets.ModelViewSet):
    queryset = Tag.objects.all()
    serializer_class = TagSeriaizer
    pagination_class = None
