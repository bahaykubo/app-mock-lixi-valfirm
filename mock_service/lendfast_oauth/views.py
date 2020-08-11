from django.http import HttpResponse, HttpResponseNotAllowed
from django.views.decorators.csrf import csrf_exempt
import random
import string
import json


@csrf_exempt
def oauth(request):
    if request.method == 'POST':
        dummy_token = dict()
        dummy_token['access_token'] = ''.join(random.choice(string.ascii_letters + string.digits) for _ in range(500))
        dummy_token['token_type'] = 'Bearer'
        dummy_token['expires_in'] = 479
        return HttpResponse(json.dumps(dummy_token))
    else:
        return HttpResponseNotAllowed(['POST'])
