from django.http import HttpResponse
from django.views.decorators.http import require_http_methods
from django.views.decorators.csrf import csrf_exempt
import random
import re
import json

from mock_service.shared import token_generator
from mock_service.shared import request_validator


@csrf_exempt
@require_http_methods(['GET'])
def images(request, image_id):
    # we have a set of specific images with an id range of 900-907
    # this is so we can provide a valid list of images for property/{id}/images
    # that they can then use to send request to this endpoint
    if request_validator.is_authorized(request.headers):
        random_id = _image_id_selector(image_id)
        with open(f'./mock_service/pricefinder/files/images/{random_id if random_id else image_id}.jpg', "rb") as file:
            return HttpResponse(file.read(), content_type="image/jpeg")
    else:
        return HttpResponse(status=401)


@csrf_exempt
@require_http_methods(['GET'])
def suggest(request):
    # we will always return the same address we are given from the request
    # and return an arbitrary property id just so the requester can make a further
    # request for property details and images
    if request_validator.is_authorized(request.headers):
        property_matches = []
        if request.GET.get('q'):
            property_matches.append({
                'property': {
                    'id': 424242
                },
                'display': request.GET.get('q')
            })
        return HttpResponse(json.dumps({'matches': property_matches}), content_type='application/json')
    else:
        return HttpResponse(status=401)


@csrf_exempt
@require_http_methods(['POST'])
def token(request):
    if all(query in request.POST.dict() for query in ['client_id', 'client_secret']):
        return HttpResponse(token_generator.generate_token_dictionary())
    else:
        return HttpResponse('{error: "invalid grant"}', status=400, content_type='application/json')


def _image_id_selector(image_id):
    if isinstance(image_id, int) and not re.search('^[9][0][0-7]$', str(image_id)):
        return random.randint(900, 907)
    else:
        return None
