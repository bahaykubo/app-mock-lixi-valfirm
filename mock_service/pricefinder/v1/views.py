from django.http import HttpResponse, HttpResponseNotAllowed
from django.views.decorators.csrf import csrf_exempt
import random
import string
import json


@csrf_exempt
def images(request):
    if request.method == 'GET':
        random_number = random.randint(0, 1)
        with open(f'./mock_service/pricefinder/images/{random_number}.jpg', "rb") as f:
            return HttpResponse(f.read(), content_type="image/jpeg")
        # return HttpResponse('hello')
    else:
        return HttpResponseNotAllowed(['POST'])
