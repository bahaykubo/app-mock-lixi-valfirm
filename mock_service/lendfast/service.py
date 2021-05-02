from django.views.decorators.csrf import csrf_exempt

from spyne.server.django import DjangoApplication
from spyne import Application, rpc, Service, Unicode
from spyne.protocol.xml import XmlDocument
from spyne.model.fault import Fault


class MockLender(Service):

    @rpc(Unicode, _returns=Unicode, _out_message_name='acknowledge')
    # pylint: disable=invalid-name,unused-argument
    def notificationList(self, notification):
        # pylint: disable=no-member
        method = self.transport.req_method
        if method.lower() != 'post':
            raise Fault(faultcode='Client', faultstring=f'{method} is not allowed')


application = Application([MockLender], 'http://www.sandstone-vms.com.au/schema/vms/1.0',
                          in_protocol=XmlDocument(),
                          out_protocol=XmlDocument())

mock_lender_service = csrf_exempt(DjangoApplication(application))
