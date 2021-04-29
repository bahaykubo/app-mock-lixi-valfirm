from django.urls import path, re_path, include

from . import views

urlpatterns = [
    path('<int:property_id>', views.property),
    path('<int:property_id>/images', views.images),
]
