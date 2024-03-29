"""mock_service URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/3.0/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.urls import include, path

from mock_service.lixi_valfirm.service import mock_valfirm_service
from mock_service.lendfast.service import mock_lender_service

urlpatterns = [
    path('mockvalfirm/', mock_valfirm_service),
    path('mocklender/notify', mock_lender_service),
    path('as/token.oauth2', include('mock_service.lendfast_oauth.urls')),
    path('mocktrack/', include('mock_service.mocktrack.urls')),
    path('index.cfm', include('mock_service.mocktrack.urls')),
    path('pricefinder/', include('mock_service.pricefinder.urls'))
]
