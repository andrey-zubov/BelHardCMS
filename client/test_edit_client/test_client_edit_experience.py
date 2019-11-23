import os
import sys
from datetime import date

import django
from django.contrib.auth import get_user_model
from django.test import TestCase
from django.urls import reverse

from client.edit.utility import time_it

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
path = os.path.expanduser(BASE_DIR)
if path not in sys.path:
    sys.path.insert(0, path)
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "BelHardCRM.settings")
django.setup()

from client.models import Client, Sphere, Experience


class ClientEditExperienceTests(TestCase):
    """ python manage.py test client/test_edit_client/ --keepdb """
    TEST_USER_USERNAME = 'test_user'
    TEST_USER_PASSWORD = 'test_user'
    TEST_USER_EMAIL = 'test_user'
    TEST_DATA_1 = {'name': 'rocket_science_1',
                   'sphere': Sphere.objects.all().first().id,
                   'position': 'rocket_science_1',
                   'start_date': date(2018, 1, 1),
                   'end_date': date.today(),
                   'duties': 'Hello',
                   }
    def setUp(self) -> None:
        user = get_user_model()
        self.test_user = user.objects.create_user(self.TEST_USER_USERNAME, self.TEST_USER_EMAIL,
                                                  self.TEST_USER_PASSWORD)
        self.client_inst = Client.objects.create(user_client=self.test_user)
        self.url = reverse('client_edit_experience')

    def test_page_open(self):
        self.client.login(username=self.TEST_USER_USERNAME, password=self.TEST_USER_PASSWORD)
        response = self.client.get(self.url)
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'client/edit_forms/client_edit_experience.html')

    def test_POST_no_user(self):
        response = self.client.post(path=self.url, data={})
        self.assertEqual(response.status_code, 302)

    default_select_fields = ["'sphere'"]

    def test_GET_no_user(self):
        response = self.client.get(self.url)
        self.assertQuerysetEqual(response.context['data'], self.default_select_fields)


    @time_it
    def test_GET_user(self):
        """ request.GET with data from skills_page_get(client). """
        self.client.login(username=self.TEST_USER_USERNAME, password=self.TEST_USER_PASSWORD)

        exp = Experience.objects.create(client_exp=self.client_inst,
                                        name=self.TEST_DATA_1['name'],
                                        position=self.TEST_DATA_1['position'],
                                        start_date=self.TEST_DATA_1['start_date'],
                                        end_date=self.TEST_DATA_1['end_date'],
                                        duties=self.TEST_DATA_1['duties'],
                                        )
        exp.sphere.add(self.TEST_DATA_1['sphere'])

        exp_arr = [{'id': exp.id,
                    'client_exp_id': self.client_inst.id,
                    'name': self.TEST_DATA_1['name'],
                    'sphere': [Sphere.objects.get(id=self.TEST_DATA_1['sphere']).sphere_word],
                    'position': self.TEST_DATA_1['position'],
                    'start_date': self.TEST_DATA_1['start_date'] if self.TEST_DATA_1[
                        'start_date'] else None,
                    'end_date': self.TEST_DATA_1['end_date'] if self.TEST_DATA_1['end_date'] else None,
                    'duties': self.TEST_DATA_1['duties'],
                    }]
        response = self.client.get(self.url)
        self.assertEqual(response.context['data']['cl_exp'], exp_arr)
        self.assertEqual(response.status_code, 200)

    @time_it
    def test_POST_user(self): #не работает
        self.client.login(username=self.TEST_USER_USERNAME, password=self.TEST_USER_PASSWORD)
        response = self.client.post(path=self.url, data=self.TEST_DATA_1)

        user_exp = Experience.objects.get(client_exp=self.client_inst)

        self.assertEqual(user_exp.name, self.TEST_DATA_1['name'])
        self.assertEqual(user_exp.sphere.first().id, self.TEST_DATA_1['sphere'])
        self.assertEqual(user_exp.position, self.TEST_DATA_1['position'])
        self.assertEqual(user_exp.start_date, self.TEST_DATA_1['start_date'])
        self.assertEqual(user_exp.end_date, self.TEST_DATA_1['end_date'])
        self.assertEqual(user_exp.duties, self.TEST_DATA_1['duties'])

        self.assertEquals(response.status_code, 302)




if __name__ == "__main__":
    ClientEditExperienceTests()
