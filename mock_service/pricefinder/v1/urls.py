from django.urls import path, include

from . import views

urlpatterns = [
    path('oauth2/token', views.token),
    path('images/<int:image_id>', views.images),
    path('properties/', include('mock_service.pricefinder.v1.properties.urls'))
]
