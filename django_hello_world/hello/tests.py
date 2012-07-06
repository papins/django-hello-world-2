from django.core.urlresolvers import reverse
from django.test import TestCase
from django.test.client import Client


class HttpTest(TestCase):
    fixtures = ['initial_data.json']

    def test_home(self):
        c = Client()

        response = c.get('/')
        self.assertEqual(response.status_code, 200)

        self.assertContains(response, '42 Coffee Cups Test Assignment')

        self.assertTrue('user_info' in response.context)
        self.assertEqual(response.context['user_info'].pk, 1)

        user_info = response.context['user_info']
        self.assertEqual(user_info.name, 'Sergey')
        self.assertEqual(user_info.last_name, 'Papin')
        self.assertEqual(user_info.email, 'papins@gmail.com')
        self.assertEqual(user_info.jabber, 'papins@gmail.com')
        self.assertEqual(user_info.skype, 'sergey.papa')

        self.assertContains(response, 'requests')

    def test_requests(self):
        c = Client()

        response = c.get('/requests/')
        self.assertEqual(response.status_code, 200)

        self.assertContains(response, 'First 10 http requests')

        self.assertTrue('request_list' in response.context)

        request_list = response.context['request_list']
        self.assertLessEqual(request_list.count(), 10)

    def test_context_processor(self):
        c = Client()

        response = c.get('/')
        self.assertEqual(response.status_code, 200)

        self.assertTrue('SETTINGS' in response.context)

        settings = response.context['SETTINGS']
        self.assertEqual(settings.SITE_ID, 1)
