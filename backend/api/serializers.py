from django.contrib.auth import get_user_model
from rest_framework import serializers

from recipes.models import Tag


User = get_user_model()


class TagSeriaizer(serializers.ModelSerializer):
    class Meta:
        model = Tag
        fields = ('id', 'name', 'color', 'slug')