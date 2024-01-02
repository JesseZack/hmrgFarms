from django.urls import path, include

app_name ='api'

urlpatterns = [
    path('crops/', include('crops.urls', namespace='crops')),
    path('farms/', include('farms.urls', namespace='farms')),
    path('users/', include('users.urls', namespace='users')),
]