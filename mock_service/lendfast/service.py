from django.http import HttpResponse
from django.views.decorators.csrf import csrf_exempt
from lxml import etree

TNS = 'http://www.sandstone-vms.com.au/schema/vms/1.0'


@csrf_exempt
def mock_lender_service(request):
    if request.method != 'POST':
        return HttpResponse(status=400)

    try:
        root = etree.fromstring(request.body)
    except etree.XMLSyntaxError:
        return HttpResponse('not found', status=404)

    if etree.QName(root).localname != 'notificationList':
        return HttpResponse('not found', status=404)

    return HttpResponse(
        f'<tns:acknowledge xmlns:tns="{TNS}"/>',
        content_type='text/xml',
    )
