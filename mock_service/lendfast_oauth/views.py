from django.http import HttpResponse
from django.views.decorators.csrf import csrf_exempt
from django.views.decorators.http import require_http_methods

from mock_service.shared import token_generator


@csrf_exempt
@require_http_methods(['POST'])
# pylint: disable=unused-argument
def oauth(request):
    return HttpResponse(token_generator.generate_token_dictionary())
