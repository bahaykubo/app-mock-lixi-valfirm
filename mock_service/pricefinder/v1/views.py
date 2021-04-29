from django.http import HttpResponse, HttpResponseNotAllowed
from django.views.decorators.http import require_http_methods
from django.views.decorators.csrf import csrf_exempt
import random
import re

from mock_service.shared import token_generator
from mock_service.shared import request_validator


@csrf_exempt
@require_http_methods(['GET'])
def images(request, image_id):
    # we have a set of specific images with an id range of 900-907
    # this is so we can provide a valid list of images for property/{id}/images
    # that they can then use to send request to this endpoint
    if request_validator.is_authorized(request):
        random_id = _image_id_selector(image_id)
        with open(f'./mock_service/pricefinder/files/images/{random_id if random_id else image_id}.jpg', "rb") as f:
            return HttpResponse(f.read(), content_type="image/jpeg")
    else:
        return HttpResponse(status=401)


@csrf_exempt
@require_http_methods(['POST'])
def token(request):
    if request.POST.get('client_id') and request.POST.get('client_secret'):
        return HttpResponse(token_generator.generate_token_dictionary())
    else:
        return HttpResponse('{error: "invalid grant"}', status=400, content_type='application/json')


def _image_id_selector(image_id):
    if not re.search('^[9][0][0-7]$', str(image_id)):
        return random.randint(900, 907)
    else:
        return None
