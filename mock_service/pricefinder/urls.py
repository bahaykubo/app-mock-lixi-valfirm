from django.urls import path, re_path, include

# see open api spec for pricefinder endpoints we are mocking here
# https://api.pricefinder.com.au/v1/swagger/index.html#/

urlpatterns = [
    path('v1/', include('mock_service.pricefinder.v1.urls'))
]
