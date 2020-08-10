from django.http import HttpResponse
from django.views.decorators.csrf import csrf_exempt
import random
import string


@csrf_exempt
def oauth(request):
    dummy_token = dict()
    dummy_token['access_token'] = ''.join(random.choice(string.ascii_letters + string.digits) for each in range(500))
    dummy_token['token_type'] = 'Bearer'
    dummy_token['expires_in'] = 479
    return HttpResponse(str(dummy_token))
