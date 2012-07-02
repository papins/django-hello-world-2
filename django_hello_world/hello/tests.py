from django.core.urlresolvers import reverse
from django.test import TestCase
from django.test.client import Client



class HttpTest(TestCase):
    def test_home(self):
        fixtures = ['initial_data.json']

        c = Client()
        # response = c.get(reverse('home'))
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
