from django.views.decorators.csrf import csrf_exempt

from spyne.server.django import DjangoApplication
from spyne import Application, rpc, Service, Unicode, error
from spyne.protocol.soap import Soap11
from spyne.model.complex import ComplexModel

from mock_service.lixi_valfirm import config
from mock_service.lixi_valfirm.validators.valuation_message import authorized, valid_message


class AuthHeader(ComplexModel):
    __namespace__ = 'lixi.mock.valfirm.service'
    UserName = Unicode
    Password = Unicode


# pylint: disable=invalid-name,no-member
class MockValfirm(Service):

    __in_header__ = AuthHeader
    out_variable_name = config.OUT_VARIABLE_NAME

    @rpc(Unicode, _returns=Unicode,  _out_variable_name=out_variable_name)
    def Order(self, ValuationMessage):
        return validate_message(self.in_header.UserName, self.in_header.Password, ValuationMessage)

    @rpc(Unicode, _returns=Unicode,  _out_variable_name=out_variable_name)
    def Update(self, ValuationMessage):
        return validate_message(self.in_header.UserName, self.in_header.Password, ValuationMessage)

    @rpc(Unicode, _returns=Unicode,  _out_variable_name=out_variable_name)
    def Cancel(self, ValuationMessage):
        return validate_message(self.in_header.UserName, self.in_header.Password, ValuationMessage)

    @rpc(Unicode, _returns=Unicode,  _out_variable_name=out_variable_name)
    def CancelAmend(self, ValuationMessage):
        return validate_message(self.in_header.UserName, self.in_header.Password, ValuationMessage)

    @rpc(Unicode, _returns=Unicode,  _out_variable_name=out_variable_name)
    def AssignedValuer(self, ValuationMessage):
        return validate_message(self.in_header.UserName, self.in_header.Password, ValuationMessage)

    @rpc(Unicode, _returns=Unicode,  _out_variable_name=out_variable_name)
    def Delay(self, ValuationMessage):
        return validate_message(self.in_header.UserName, self.in_header.Password, ValuationMessage)

    @rpc(Unicode, _returns=Unicode,  _out_variable_name=out_variable_name)
    def FeeChange(self, ValuationMessage):
        return validate_message(self.in_header.UserName, self.in_header.Password, ValuationMessage)

    @rpc(Unicode, _returns=Unicode,  _out_variable_name=out_variable_name)
    def NoteAdded(self, ValuationMessage):
        return validate_message(self.in_header.UserName, self.in_header.Password, ValuationMessage)

    @rpc(Unicode, _returns=Unicode,  _out_variable_name=out_variable_name)
    def QuoteRequest(self, ValuationMessage):
        return validate_message(self.in_header.UserName, self.in_header.Password, ValuationMessage)

    @rpc(Unicode, _returns=Unicode,  _out_variable_name=out_variable_name)
    def QuoteResponse(self, ValuationMessage):
        return validate_message(self.in_header.UserName, self.in_header.Password, ValuationMessage)

    @rpc(Unicode, _returns=Unicode,  _out_variable_name=out_variable_name)
    def Error(self, ValuationMessage):
        return validate_message(self.in_header.UserName, self.in_header.Password, ValuationMessage)

    @rpc(Unicode, _returns=Unicode,  _out_variable_name=out_variable_name)
    def Amendment(self, ValuationMessage):
        return validate_message(self.in_header.UserName, self.in_header.Password, ValuationMessage)

    @rpc(Unicode, _returns=Unicode,  _out_variable_name=out_variable_name)
    def Escalate(self, ValuationMessage):
        return validate_message(self.in_header.UserName, self.in_header.Password, ValuationMessage)

    @rpc(Unicode, _returns=Unicode,  _out_variable_name=out_variable_name)
    def Complete(self, ValuationMessage):
        return validate_message(self.in_header.UserName, self.in_header.Password, ValuationMessage)


SCHEMA = config.SCHEMA_FILE


def validate_message(username, password, valuation_message):
    try:
        if not authorized(username, password):
            raise error.Fault(
                faultcode='Client', faultstring='Unable to process request. UserName or Password is incorrect.')
    except ValueError:
        raise error.Fault(faultcode='Client', faultstring='Unable to process request. No authorisation provided.')
    except Exception:
        raise error.Fault(faultcode='Server', faultstring='Unable to process request. Invalid authorisation.')

    try:
        if not valid_message(valuation_message, SCHEMA):
            raise error.Fault(faultcode='Client', faultstring='Unable to process request. ValuationMessage is invalid')
    except AttributeError:
        raise error.Fault(faultcode='Client', faultstring='Unable to process request. ValuationMessage is invalid')
    except Exception as exception:
        raise error.Fault(faultcode='Server', faultstring=f'Unable to process request. ValuationMessage: '
                                                          f'{valuation_message}. Error: {exception}')

    return "0"


application = Application([MockValfirm], 'lixi.mock.valfirm.service',
                          in_protocol=Soap11(validator='lxml'),
                          out_protocol=Soap11())

mock_valfirm_service = csrf_exempt(DjangoApplication(application))
