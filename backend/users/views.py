from django.contrib.auth import get_user_model
from djoser import views
from rest_framework import filters, permissions, status
from rest_framework.decorators import action
from rest_framework.response import Response

from api.utils import CustomPagination
from .serializers import UserCustomSerializer

User = get_user_model()


class CustomUserViewset(views.UserViewSet):
    pagination_class = CustomPagination
    filter_backends = (filters.SearchFilter,)
    filter_fields = ('id',)
    search_fields = ('id',)
    lookup_field = 'id'

    @action(
        methods=['GET'],
        detail=False,
        pagination_class=None,
        url_path='me',
        url_name='me',
        permission_classes=[permissions.IsAuthenticated],
    )
    def me(self, request):
        """Обработка эндпойнта /me."""
        serializer = UserCustomSerializer(request.user)
        return Response(serializer.data, status=status.HTTP_200_OK)
