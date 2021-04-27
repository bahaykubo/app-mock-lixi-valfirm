from django.urls import path, re_path, include

# from . import views

urlpatterns = [
    path('v1/', include('mock_service.pricefinder.v1.urls'))
]
