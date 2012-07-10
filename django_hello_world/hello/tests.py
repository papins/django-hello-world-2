from django.core.urlresolvers import reverse
from django.test import TestCase
from django.test.client import Client


class HttpTest(TestCase):
    fixtures = ['initial_data.json']

    def test_home(self):
        c = Client()

        response = c.get(reverse('home'))
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

        self.assertContains(response, 'Photo:')

    def test_requests(self):
        c = Client()

        response = c.get(reverse('requests'))
        self.assertEqual(response.status_code, 200)

        self.assertContains(response, 'Last 10 http requests')

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

    def test_edit_form(self):
        c = Client()

        response = c.get(reverse('edit'))
        self.assertRedirects(response, '/accounts/login/?next=/edit/')

        c.login(username='admin', password='admin')

        response = c.get(reverse('edit'))
        self.assertEqual(response.status_code, 200)

        self.assertContains(response, '42 Coffee Cups Test Assignment')

        self.assertTrue('form' in response.context)

        # empty values
        response = c.post(reverse("edit"), {
            "name": "",
            "last_name": "",
            "date_of_birth": "",
            "email": "",
            "jabbber": "",
            "skype": "",
            "bio": "",
            "other_contacts": ""
        })
        self.assertEqual(response.status_code, 200)
        self.assertFormError(response, 'form', 'name',
                             [u'This field is required.'])
        self.assertFormError(response, 'form', 'last_name',
                             [u'This field is required.'])
        self.assertFormError(response, 'form', 'date_of_birth',
                             [u'This field is required.'])
        self.assertFormError(response, 'form', 'email',
                             [u'This field is required.'])
        self.assertFormError(response, 'form', 'skype',
                             [u'This field is required.'])
        self.assertFormError(response, 'form', 'bio', [])
        self.assertFormError(response, 'form', 'other_contacts', [])

        # invalid date_of_birth, email, jabber
        response = c.post(reverse("edit"), {
            "date_of_birth": "foo",
            "email": "foo",
            "jabber": "foo",
        })
        self.assertEqual(response.status_code, 200)
        self.assertFormError(response, 'form', 'date_of_birth',
                             [u'Enter a valid date.'])
        self.assertFormError(response, 'form', 'email',
                             [u'Enter a valid e-mail address.'])
        self.assertFormError(response, 'form', 'jabber',
                             [u'Enter a valid e-mail address.'])

        # valid values
        response = c.post(reverse("edit"), {
            "name": "Sergey",
            "last_name": "Papin",
            "date_of_birth": "1977-04-10",
            "email": "papins@gmail.com",
            "jabbber": "papins@gmail.com",
            "skype": "papins@gmail.com",
            "bio": "some bio",
            "other_contacts": "",
        })
        self.assertEqual(response.status_code, 200)
        self.assertFormError(response, 'form', 'name', [])
        self.assertFormError(response, 'form', 'last_name', [])
        self.assertFormError(response, 'form', 'date_of_birth', [])
        self.assertFormError(response, 'form', 'email', [])
        self.assertFormError(response, 'form', 'skype', [])
        self.assertFormError(response, 'form', 'bio', [])
        self.assertFormError(response, 'form', 'other_contacts', [])
