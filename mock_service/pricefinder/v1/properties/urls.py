from django.urls import path

from . import views

urlpatterns = [
    path('<int:property_id>', views.property),
    path('<int:property_id>/images', views.images),
]
