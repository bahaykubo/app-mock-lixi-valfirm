from django.urls import path

from . import views

urlpatterns = [
    path('', views.oauth, name='oauth'),
]
