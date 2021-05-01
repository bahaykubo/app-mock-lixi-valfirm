from unittest import TestCase
import requests

from test import config


class TestMocktrack(TestCase):

    def setUp(self):
        self.xml = f'''<?xml version="1.0" encoding="utf-8"?>
            <hometrack>
                <realtime accountid="123456">
                    <valuationrequest>
                        <property reference="CTT-EA49-CRF" propertytype="3" streetnum="86" street="oriel"
                            streettype="road" suburb="ivanhoe" postcode="4242" state="nsw"
                            estimatedvalue="485000"/>
                    </valuationrequest>
                </realtime>
            </hometrack>'''

    def set_url(self, action, env=None):
        return f'{config.hostname()}/mocktrack/index.cfm?fuseaction={"api.interface" if action == "api" else "api.retrievevaluationpdf"}&accountid=13265&password=AbCdEfG1234&autologin=ThisIsMyLOGIN&autopassword=th1sIsMyPWord&realtimevalauth=abc'

    def test_api_response(self):
        response = requests.post(self.set_url('api'), data=self.xml)
        self.assertEqual(response.status_code, 200)
        self.assertIn('/xml', response.headers['content-type'])

    def test_pdf_response(self):
        response = requests.post(self.set_url('pdf'), data=self.xml)
        self.assertEqual(response.status_code, 200)
        self.assertIn('/pdf', response.headers['content-type'])
