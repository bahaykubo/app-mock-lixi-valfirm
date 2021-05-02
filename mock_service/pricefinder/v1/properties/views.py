from django.http import HttpResponse
from django.views.decorators.http import require_http_methods
from django.views.decorators.csrf import csrf_exempt

from mock_service.shared import request_validator


@csrf_exempt
@require_http_methods(['GET'])
# pylint: disable=unused-argument
def images(request, property_id):
    # we don't care what property id we get from the request
    # we will always return a list of images based on the images
    # we have on pricefinder/files/images so that the requester will
    # always get images on their subsequent request for the actual image
    if request_validator.is_authorized(request.headers):
        with open('./mock_service/pricefinder/files/property_images.json', 'rb') as file:
            return HttpResponse(file, content_type='application/json')
    else:
        return HttpResponse(status=401)


@csrf_exempt
@require_http_methods(['GET'])
# pylint: disable=unused-argument
def property(request, property_id):
    # we don't care what property id we get from the request
    # we will always return a generic property
    if request_validator.is_authorized(request.headers):
        with open('./mock_service/pricefinder/files/property.json', 'rb') as file:
            return HttpResponse(file, content_type='application/json')
    else:
        return HttpResponse(status=401)
