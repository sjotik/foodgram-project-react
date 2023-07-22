from django.contrib.auth import get_user_model
from rest_framework import filters, viewsets
from rest_framework.pagination import PageNumberPagination

from .serializers import UserCustomSerializer

User = get_user_model()


class UserViewSet(viewsets.ModelViewSet):
    """Вьсет модели User"""

    queryset = User.objects.all()
    serializer_class = UserCustomSerializer
    # permission_classes = (IsAdminSuperuser,)
    filter_backends = (filters.SearchFilter,)
    filter_fields = ('username',)
    search_fields = ('username',)
    lookup_field = 'username'
    pagination_class = PageNumberPagination
