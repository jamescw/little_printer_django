import json

from django.test import TestCase

from publication.forms import HelloWorldPublicationForm


class TestPublicationViews(TestCase):
    """
    Tests publication meets Bergcloud API spec
    """
    def setUp(self):
        """
        Set up request params
        """
        self.data = {
            'name': 'James',
            'lang': 'english',
        }

    def test_meta(self):
        """
        Test json meta file contains expected config
        """
        form = HelloWorldPublicationForm()
        response = self.client.get('/meta.json')
        self.assertEqual(response.status_code, 200)
        json_data = json.loads(response.content)
        # test header content in meta file
        self.assertDictContainsSubset(form.meta, json_data)
        # test all defined form fields are present in field config
        index = 0
        for name, instance in form.fields.items():
            if name in self.data:
                self.assertDictContainsSubset(
                    instance.serialise(name),
                    json_data['config']['fields'][index]
                )
                index += 1

    def test_sample(self):
        """
        Test we can get an edition sample
        """
        response = self.client.get('/sample/')
        self.assertTemplateUsed(
            response,
            template_name='publication/sample.html'
        )
        self.assertContains(response, 'Hello World')

    def test_edition(self):
        """
        Test editions respect incoming params from Bergcloud
        """
        response = self.client.get('/edition/', data=self.data)
        self.assertTemplateUsed(
            response,
            template_name='publication/hello_world.html'
        )
        self.assertTrue('ETag' in response)
        self.assertContains(
            response,
            'Good evening {}'.format(self.data['name'])
        )
        self.data['lang'] = 'french'
        response = self.client.get('/edition/', data=self.data)
        self.assertContains(
            response,
            'Bonjour {}'.format(self.data['name'])
        )

    def test_validate_config_true(self):
        """
        Test expected params validate successfully
        """
        request_data = json.dumps(self.data)
        response = self.client.post(
            '/validate_config/',
            data={'config': request_data}
        )
        json_data = json.loads(response.content)
        self.assertTrue(json_data['valid'])

    def test_validate_config_false(self):
        """
        Test we return correct errors for missing params
        """
        self.data.pop('name')
        request_data = json.dumps(self.data)
        response = self.client.post(
            '/validate_config/',
            data={'config': request_data}
        )
        json_data = json.loads(response.content)
        self.assertFalse(json_data['valid'])
        self.assertEqual(json_data['errors'][0],
                         'Please enter your name')

    def test_icon(self):
        """
        Test we redirect to our icon file
        """
        response = self.client.get('/icon.png')
        self.assertEqual(response.status_code, 301)

