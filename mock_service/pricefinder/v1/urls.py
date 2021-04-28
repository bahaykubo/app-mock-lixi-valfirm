from django.urls import path

from . import views

urlpatterns = [
    path('oauth2/token', views.token),
    path('images/<int:image_id>', views.images),
]
