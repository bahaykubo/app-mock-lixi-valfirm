from django.http import HttpResponse, HttpResponseNotAllowed
from django.views.decorators.csrf import csrf_exempt

from mock_service.shared import token_generator


@csrf_exempt
def oauth(request):
    if request.method == 'POST':
        return HttpResponse(token_generator.generate_token_dictionary())
    else:
        return HttpResponseNotAllowed(['POST'])
