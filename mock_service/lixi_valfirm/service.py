from django.views.decorators.csrf import csrf_exempt

from spyne.server.django import DjangoApplication
from spyne import Application, rpc, Service, Unicode, error, AnyXml
from spyne.protocol.soap import Soap11
from spyne.server.django import DjangoApplication
from spyne.model.complex import ComplexModel

from mock_service.lixi_valfirm import config
from mock_service.lixi_valfirm.validators.valuation_message import authorized, valid_message


class AuthHeader(ComplexModel):
    __namespace__ = 'lixi.mock.valfirm.service'
    UserName = Unicode
    Password = Unicode


class MockValfirm(Service):
    __in_header__ = AuthHeader
    out_variable_name = config.OUT_VARIABLE_NAME

    @rpc(Unicode, _returns=Unicode,  _out_variable_name=out_variable_name)
    def Order(ctx, ValuationMessage):
        return validate_message(ctx.in_header.UserName, ctx.in_header.Password, ValuationMessage)

    @rpc(Unicode, _returns=Unicode,  _out_variable_name=out_variable_name)
    def Update(ctx, ValuationMessage):
        return validate_message(ctx.in_header.UserName, ctx.in_header.Password, ValuationMessage)

    @rpc(Unicode, _returns=Unicode,  _out_variable_name=out_variable_name)
    def Cancel(ctx, ValuationMessage):
        return validate_message(ctx.in_header.UserName, ctx.in_header.Password, ValuationMessage)

    @rpc(Unicode, _returns=Unicode,  _out_variable_name=out_variable_name)
    def CancelAmend(ctx, ValuationMessage):
        return validate_message(ctx.in_header.UserName, ctx.in_header.Password, ValuationMessage)

    @rpc(Unicode, _returns=Unicode,  _out_variable_name=out_variable_name)
    def AssignedValuer(ctx, ValuationMessage):
        return validate_message(ctx.in_header.UserName, ctx.in_header.Password, ValuationMessage)

    @rpc(Unicode, _returns=Unicode,  _out_variable_name=out_variable_name)
    def Delay(ctx, ValuationMessage):
        return validate_message(ctx.in_header.UserName, ctx.in_header.Password, ValuationMessage)

    @rpc(Unicode, _returns=Unicode,  _out_variable_name=out_variable_name)
    def FeeChange(ctx, ValuationMessage):
        return validate_message(ctx.in_header.UserName, ctx.in_header.Password, ValuationMessage)

    @rpc(Unicode, _returns=Unicode,  _out_variable_name=out_variable_name)
    def NoteAdded(ctx, ValuationMessage):
        return validate_message(ctx.in_header.UserName, ctx.in_header.Password, ValuationMessage)

    @rpc(Unicode, _returns=Unicode,  _out_variable_name=out_variable_name)
    def QuoteRequest(ctx, ValuationMessage):
        return validate_message(ctx.in_header.UserName, ctx.in_header.Password, ValuationMessage)

    @rpc(Unicode, _returns=Unicode,  _out_variable_name=out_variable_name)
    def QuoteResponse(ctx, ValuationMessage):
        return validate_message(ctx.in_header.UserName, ctx.in_header.Password, ValuationMessage)

    @rpc(Unicode, _returns=Unicode,  _out_variable_name=out_variable_name)
    def Error(ctx, ValuationMessage):
        return validate_message(ctx.in_header.UserName, ctx.in_header.Password, ValuationMessage)

    @rpc(Unicode, _returns=Unicode,  _out_variable_name=out_variable_name)
    def Amendment(ctx, ValuationMessage):
        return validate_message(ctx.in_header.UserName, ctx.in_header.Password, ValuationMessage)

    @rpc(Unicode, _returns=Unicode,  _out_variable_name=out_variable_name)
    def Escalate(ctx, ValuationMessage):
        return validate_message(ctx.in_header.UserName, ctx.in_header.Password, ValuationMessage)

    @rpc(Unicode, _returns=Unicode,  _out_variable_name=out_variable_name)
    def Complete(ctx, ValuationMessage):
        return validate_message(ctx.in_header.UserName, ctx.in_header.Password, ValuationMessage)


schema = config.SCHEMA_FILE


def validate_message(username, password, valuation_message):
    try:
        if not authorized(username, password):
            raise error.Fault(
                faultcode='Client', faultstring='Unable to process request. UserName or Password is incorrect.')
    except ValueError:
        raise error.Fault(faultcode='Client', faultstring='Unable to process request. No authorisation provided.')
    except Exception as e:
        raise error.Fault(faultcode='Server', faultstring='Unable to process request. Invalid authorisation.')

    try:
        if not valid_message(valuation_message, schema):
            raise error.Fault(faultcode='Client', faultstring='Unable to process request. ValuationMessage is invalid')
    except AttributeError:
        raise error.Fault(faultcode='Client', faultstring='Unable to process request. ValuationMessage is invalid')
    except Exception as e:
        raise error.Fault(faultcode='Server', faultstring=f'Unable to process request. ValuationMessage: '
                                                          f'{valuation_message}. Error: {e}')

    return "0"


application = Application([MockValfirm], 'lixi.mock.valfirm.service',
                          in_protocol=Soap11(validator='lxml'),
                          out_protocol=Soap11())

mock_valfirm_service = csrf_exempt(DjangoApplication(application))
