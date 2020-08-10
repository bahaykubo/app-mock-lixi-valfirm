from django.views.decorators.csrf import csrf_exempt

from spyne.server.django import DjangoApplication
from spyne import Application, rpc, Service, Unicode, error, AnyXml
from spyne.protocol.soap import Soap11
from spyne.server.django import DjangoApplication
from spyne.model.complex import ComplexModel


class MockLender(Service):

    @rpc(Unicode, _returns=Unicode, _out_message_name='acknowledge')
    def notificationList(ctx, notification):
        pass


application = Application([MockLender], 'http://www.sandstone-vms.com.au/schema/vms/1.0',
                          in_protocol=Soap11(validator='soft'),
                          out_protocol=Soap11())

mock_lender_service = csrf_exempt(DjangoApplication(application))
