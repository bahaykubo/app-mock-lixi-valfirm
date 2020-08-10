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
from django.conf.urls import url

from spyne.protocol.soap import Soap11
from spyne.server.django import DjangoView

from mock_service.lixi_valfirm.service import mock_valfirm_service, application, MockValfirm
from mock_service.lendfast.service import mock_lender_service, application, MockLender

urlpatterns = [
    url(r'^mockvalfirm/', mock_valfirm_service),
    url(r'^mocklender/', mock_lender_service),
]
