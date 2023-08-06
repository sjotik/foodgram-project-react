from django.contrib.auth import get_user_model
from rest_framework import filters
from djoser import views

from api.utils import CustomPagination

User = get_user_model()


class CustomUserViewset(views.UserViewSet):
    pagination_class = CustomPagination
    filter_backends = (filters.SearchFilter,)
    filter_fields = ('id',)
    search_fields = ('id',)
    lookup_field = 'id'
