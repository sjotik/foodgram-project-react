from django.urls import include, path


app_name = 'users'

urlpatterns = [
    path('auth/', include('djoser.urls.authtoken')),
    path('', include('djoser.urls'), name='auth'),
]
