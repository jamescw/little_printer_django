import json

from django.test import TestCase


class TestPrinterViews(TestCase):

    def setUp(self):
        self.data = {
            'name': 'James',
            'lang': 'english',
            'local_delivery_time': '2013-07-21T19:20:30.45+01:00'
        }

        self.meta = {
            "owner_email" : "publisher<at>bergcloud<dot>com",
            "publication_api_version": "1.0",
            "name": "Hello World Example",
            "description": "Say Hello in a few languages",
            "delivered_on": "every Monday",
            "send_timezone_info": True,
            "send_delivery_count": False,
            "external_configuration": False,
        }

    def test_edition(self):

        response = self.client.get('/edition/', data=self.data)
        self.assertContains(response, 'Good evening')

    def test_validate_config_true(self):

        self.data.pop('local_delivery_time')
        request_data = json.dumps(self.data)
        response = self.client.post(
            '/validate_config/',
            data={'config': request_data}
        )
        json_data = json.loads(response.content)
        self.assertTrue(json_data['valid'])

    def test_validate_config_false(self):

        self.data.pop('name')
        request_data = json.dumps(self.data)
        response = self.client.post(
            '/validate_config/',
            data={'config': request_data}
        )
        json_data = json.loads(response.content)
        self.assertFalse(json_data['valid'])

