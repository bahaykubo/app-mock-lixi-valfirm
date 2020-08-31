from django.http import HttpResponse, HttpResponseNotAllowed
from django.views.decorators.csrf import csrf_exempt
import random
from xml.etree import ElementTree
import secrets
from datetime import datetime
import os
import io
from reportlab.pdfgen import canvas


@csrf_exempt
def mocktrack(request):
    if not allowed_request_method(request.method):
        return HttpResponseNotAllowed(['GET', 'POST'])

    try:
        action = validate_request_and_get_action(request.GET)
    except PermissionError as error:
        return HttpResponse(error_response(3, error), content_type='text/xml;charset=UTF-8')

    try:
        request_dict = convert_xml_request_to_dictionary(request.body)
    except SyntaxError as error:
        return HttpResponse(error_response(63, error), content_type='text/xml;charset=UTF-8')

    if address_complete(request_dict):
        if action['fuseaction'] == 'api':
            response = api_response(request_dict, action)
            return HttpResponse(response, content_type='text/xml;charset=UTF-8')
        elif action['fuseaction'] == 'pdf':
            pdf = create_pdf(request_dict['property'])
            response = HttpResponse(pdf, content_type='application/pdf;charset=UTF-8')
            response['Content-Disposition'] = 'attachment; filename=mocktrack_report.pdf'
            return response
    else:
        return HttpResponse(error_response(102, 'No address match'), content_type='text/xml;charset=UTF-8')


def allowed_request_method(method):
    if method.lower() not in ['post', 'get']:
        return False
    else:
        return True


def convert_xml_request_to_dictionary(xml):
    try:
        xml_request = ElementTree.fromstring(xml.decode('utf-8'))
        xml_request_dict = dict()
        for child in xml_request.iter('*'):
            if 'xmlns' not in child.attrib:
                xml_request_dict[child.tag] = {k: v for k, v in child.attrib.items() if v is not ''}
        return xml_request_dict
    except ElementTree.ParseError as e:
        raise SyntaxError(f'Unrecognised XML Format - please check schema {e}')


def address_complete(request):
    try:
        if request['property'] and ('address' in request['property'] or all(
            key.lower() in request['property'] for key in (
                'streetnum', 'street', 'streettype', 'suburb', 'postcode', 'state'))):
            return True
        else:
            return False
    except Exception:
        return False


def validate_request_and_get_action(url_string_parameters):
    try:
        fuseaction = url_string_parameters.get('fuseaction', None)
        account_id = url_string_parameters.get('accountid', None)
        password = url_string_parameters.get('password', None)
        auto_login = url_string_parameters.get('autologin', None)
        auto_password = url_string_parameters.get('autopassword', None)
        realtime_val_auth = url_string_parameters.get('realtimevalauth', None)

        action = dict()
        if fuseaction and account_id and password and auto_login and auto_password:
            action['account_id'] = account_id
            if fuseaction == 'api.interface':
                action['fuseaction'] = 'api'
            elif fuseaction == 'api.retrievevaluationpdf':
                if not realtime_val_auth:
                    raise PermissionError()
                action['realtime_val_auth'] = realtime_val_auth
                action['fuseaction'] = 'pdf'
            return action
        else:
            raise PermissionError()
    except Exception as e:
        raise PermissionError('Incorrect Login details supplied')


def api_response(request, action):
    datetime_now = datetime.now().strftime("%b %d %Y %I:%S%p")
    property = request['property']
    address = property['address'] if 'address' in property else ''
    streetnum = property['streetnum'] if 'streetnum' in property else ''
    street = f'{property["street"].upper()} {property["streettype"].upper()}' if 'street' in property else ''
    suburb = property['suburb'].upper() if 'suburb' in property else ''
    postcode = property['postcode'] if 'postcode' in property else ''
    state = property['state'].upper() if 'state' in property else ''
    order_number = property['reference'].upper() if 'reference' in property else ''

    input_address = f'{streetnum} {street} {suburb} {postcode} {state}' if 'street' in property else address
    output_address = f'{streetnum} {street} {suburb} {postcode}' if 'street' in property else address

    estimate = 485000 if 'estimatedvalue' not in property else(
        2500042 if property['estimatedvalue'] == '489042' else int(property['estimatedvalue']))
    fsd = 0.05

    valuation_result = f'realtimevalid="{action["account_id"]}" realtimevalauth="{secrets.token_hex(19)}" datetime="{datetime_now}" realtimevaluation="{estimate}" confidencelevel="5.0" fsd="{fsd}" valuerangelower="{int(estimate-(estimate*fsd))}" valuerangeupper="{int(estimate+(estimate*fsd))}"'

    if 'address' in property:
        valuation_property = f'postcode="{postcode}" street="STREET" suburb="SUBURB" concataddress="{output_address}" propertytypeid="{property["propertytype"]}" propertytype="House" htproptypeid="{property["propertytype"]}" addresspointtoid="9276074" floorplate="242" asofdate="{datetime_now}" applicantsestimatedvalue="{estimate}" reference="{order_number}" x_coord="1698302.720" y_coord="1042621.340" lat="-37.757575" lon="145.037833"'
    else:
        valuation_property = f'postcode="{postcode}" buildingnumber="{streetnum}" street="{street}" suburb="{suburb}" concataddress="{output_address}" propertytypeid="{property["propertytype"]}" propertytype="House" htproptypeid="{property["propertytype"]}" addresspointtoid="9276074" floorplate="242" asofdate="{datetime_now}" applicantsestimatedvalue="{estimate}" reference="{order_number}" x_coord="1698302.720" y_coord="1042621.340" lat="-37.757575" lon="145.037833"'

    address_matching = f'apiused="true" matched="true" foundindatabase="true" inputaddress="{input_address}" outputaddress="{output_address}" postcodeconfidence=""'

    return f'''<?xml version="1.0" ?>
    <hometrack>
        <realtime interfaceversion="2.2" accountid="{request['realtime']['accountid']}">
            <valuationresponse orderid="{random.randrange(1, 10**7):07}">
                <errors/>
                <valuationresult {valuation_result}>
                    <errors/>
                    <warnings/>
                    <valuationproperty {valuation_property}/>
                    <addressmatching {address_matching}/>
                </valuationresult>
            </valuationresponse>
        </realtime>
    </hometrack>'''


def create_pdf(property):
    buffer = io.BytesIO()
    p = canvas.Canvas(buffer)
    p.drawString(100, 100, f'Valocity Realtime API {property["reference"] if "reference" in property else ""}')
    p.showPage()
    p.save()
    buffer.seek(0)
    return buffer


def error_response(error_id, message):
    return f'''<?xml version="1.0" ?>
    <hometrack>
        <realtime interfaceversion="2.2" accountid="-1">
            <valuationresponse>
                <errors>
                    <error errorid="{error_id}" errormessage="{message}"/>
                </errors>
                <valuationresult/>
            </valuationresponse>
        </realtime>
    </hometrack>'''
