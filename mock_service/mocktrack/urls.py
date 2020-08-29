from django.urls import path, re_path

from . import views

urlpatterns = [
    path('', views.mocktrack, name='mocktrack'),
    path('index.cfm', views.mocktrack, name='mocktrack'),
]
