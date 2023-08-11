from http import HTTPStatus

from django.test import TestCase
from rest_framework import status
from rest_framework.test import APIClient

from foodgram_backend.settings import TEST_IMAGE
from recipes.models import Ingredient, Tag, User


class FoodgramAPITestCase(TestCase):
    def setUp(self):
        self.guest_client = APIClient()
        self.client = APIClient()
        self.user = User.objects.create_user(
            username='testuser',
            password='QAZwsx!1',
            email='test@test.loc',
            first_name='Test',
            last_name='Testov',
        )
        self.tag = Tag.objects.create(
            name="Test", color="#74h7as", slug="test")
        self.ingr = Ingredient.objects.create(
            name="test", measurement_unit="t")
        auth_url = '/api/auth/token/login/'
        data = {'email': 'test@test.loc', 'password': 'QAZwsx!1'}
        self.token = self.client.post(
            auth_url, data=data, format='json').data['auth_token']
        self.client.credentials(HTTP_AUTHORIZATION='Token ' + self.token)

    def test_list_exists(self):
        """Проверка доступности главной страницы."""
        response = self.guest_client.get('/api/recipes/')
        self.assertEqual(
            response.status_code, HTTPStatus.OK, 'Страница недоступна')

    def test_create_recipe(self):
        """Тест добавления рецепта"""
        url = '/api/recipes/'
        data = {
            'name': 'TEST1',
            'text': 'TEST1',
            'cooking_time': 5,
            'image': TEST_IMAGE,
            'ingredients': [{"id": 1, "amount": 150}],
            'tags': [1],
        }
        response = self.client.post(url, data=data, format='json')
        self.assertEqual(
            response.status_code,
            status.HTTP_201_CREATED,
            'Не удалось создать рецепт'
        )
