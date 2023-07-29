from django.urls import include, path
from rest_framework.routers import DefaultRouter

from api.views import SubscribeApiView, SubscribtionsApiView

app_name = 'users'

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
    path('', include('djoser.urls'), name='auth'),
]
