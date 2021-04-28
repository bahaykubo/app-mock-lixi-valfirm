from django.http import HttpResponse, HttpResponseNotAllowed
from django.views.decorators.http import require_http_methods
from django.views.decorators.csrf import csrf_exempt
import random
import string
import json
import re


@csrf_exempt
@require_http_methods(['GET'])
def images(request, image_id):
    random_image = None
    if not re.search('^[9][0][0-7]$', str(image_id)):
        random_image = random.randint(900, 907)
    with open(f'./mock_service/pricefinder/files/images/{random_image if random_image else image_id}.jpg', "rb") as f:
        return HttpResponse(f.read(), content_type="image/jpeg")
