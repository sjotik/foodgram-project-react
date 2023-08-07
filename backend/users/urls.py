from django.urls import include, path
from rest_framework import routers

from api.views import SubscribeApiView, SubscribtionsApiView
from .views import CustomUserViewset

app_name = 'users'

router_v1 = routers.DefaultRouter()
router_v1.register(r'users', CustomUserViewset, basename='users')

urlpatterns = [
    path('auth/', include('djoser.urls.authtoken')),
    path(
        'users/subscriptions/',
        SubscribtionsApiView.as_view(),
        name='subscriptions'
         ),
    path(
        'users/<int:id>/subscribe/',
        SubscribeApiView.as_view(),
        name='subscribe'
         ),
    path('', include(router_v1.urls)),
]
