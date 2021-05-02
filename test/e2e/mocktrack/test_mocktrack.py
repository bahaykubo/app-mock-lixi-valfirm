from unittest import TestCase
import requests
from pathlib import Path

from test import config


class TestMocktrack(TestCase):

    def setUp(self):
        self.xml = Path('./test/files/mocktrack/valid.xml').read_text()

    @staticmethod
    def set_url(action):
        return f'{config.hostname()}/mocktrack/index.cfm?fuseaction={"api.interface" if action == "api" else "api.retrievevaluationpdf"}&accountid=13265&password=AbCdEfG1234&autologin=ThisIsMyLOGIN&autopassword=th1sIsMyPWord&realtimevalauth=abc'

    def test_api_response(self):
        response = requests.post(self.set_url('api'), data=self.xml)
        self.assertEqual(response.status_code, 200)
        self.assertIn('/xml', response.headers['content-type'])

    def test_pdf_response(self):
        response = requests.post(self.set_url('pdf'), data=self.xml)
        self.assertEqual(response.status_code, 200)
        self.assertIn('/pdf', response.headers['content-type'])
