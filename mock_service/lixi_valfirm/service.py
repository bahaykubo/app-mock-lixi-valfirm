from django.http import HttpResponse
from django.views.decorators.csrf import csrf_exempt
from lxml import etree

from mock_service.lixi_valfirm import config
from mock_service.lixi_valfirm.validators.valuation_message import authorized, valid_message

SOAP_NS = 'http://schemas.xmlsoap.org/soap/envelope/'
TNS = 'lixi.mock.valfirm.service'
VALID_ACTIONS = frozenset([
    'Order', 'Update', 'Cancel', 'CancelAmend', 'AssignedValuer',
    'Delay', 'FeeChange', 'NoteAdded', 'QuoteRequest', 'QuoteResponse',
    'Error', 'Amendment', 'Escalate', 'Complete',
])
SCHEMA = config.SCHEMA_FILE


def _soap_response(action, result):
    return (
        "<?xml version='1.0' encoding='UTF-8'?>"
        f'<soap-env:Envelope xmlns:soap-env="{SOAP_NS}">'
        f'<soap-env:Body>'
        f'<tns:{action}Response xmlns:tns="{TNS}">'
        f'<tns:Result>{result}</tns:Result>'
        f'</tns:{action}Response>'
        f'</soap-env:Body>'
        f'</soap-env:Envelope>'
    )


def _soap_fault(faultcode, faultstring):
    body = (
        "<?xml version='1.0' encoding='UTF-8'?>"
        f'<soap-env:Envelope xmlns:soap-env="{SOAP_NS}">'
        f'<soap-env:Body>'
        f'<soap-env:Fault>'
        f'<faultcode>soap-env:{faultcode}</faultcode>'
        f'<faultstring>{faultstring}</faultstring>'
        f'</soap-env:Fault>'
        f'</soap-env:Body>'
        f'</soap-env:Envelope>'
    )
    return HttpResponse(body, content_type='text/xml', status=500)


@csrf_exempt
def mock_valfirm_service(request):
    if request.method != 'POST':
        return HttpResponse(status=405)

    try:
        envelope = etree.fromstring(request.body)
    except etree.XMLSyntaxError as e:
        return _soap_fault('Client', str(e))

    header = envelope.find(f'{{{SOAP_NS}}}Header')
    auth = header.find(f'{{{TNS}}}AuthHeader') if header is not None else None
    username = auth.findtext(f'{{{TNS}}}UserName') if auth is not None else None
    password = auth.findtext(f'{{{TNS}}}Password') if auth is not None else None

    body = envelope.find(f'{{{SOAP_NS}}}Body')
    action_el = body[0] if body is not None and len(body) else None
    if action_el is None:
        return _soap_fault('Client', 'No body element found')

    action = etree.QName(action_el).localname
    if action not in VALID_ACTIONS:
        return _soap_fault('Client', 'No matching global declaration available for the validation root')

    msg_el = action_el.find(f'{{{TNS}}}ValuationMessage')
    valuation_message = msg_el.text if msg_el is not None else None

    try:
        if not authorized(username, password):
            return _soap_fault('Server', 'Unable to process request. Invalid authorisation.')
    except ValueError:
        return _soap_fault('Client', 'Unable to process request. No authorisation provided.')
    except Exception:
        return _soap_fault('Server', 'Unable to process request. Invalid authorisation.')

    try:
        if not valid_message(valuation_message, SCHEMA):
            return _soap_fault('Client', 'Unable to process request. ValuationMessage is invalid')
    except AttributeError:
        return _soap_fault('Client', 'Unable to process request. ValuationMessage is invalid')
    except Exception as e:
        return _soap_fault('Server', f'Unable to process request. ValuationMessage: {valuation_message}. Error: {e}')

    return HttpResponse(_soap_response(action, '0'), content_type='text/xml')
