import os
import sys

import django
from django.contrib.auth import get_user_model
from django.test import TestCase
from django.urls import reverse

from client.models import Client

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
path = os.path.expanduser(BASE_DIR)
if path not in sys.path:
    sys.path.insert(0, path)
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "BelHardCRM.settings")
django.setup()


class ClientEditMainTests(TestCase):
    """ python manage.py test client/test_edit_client/ --keepdb """
    TEST_USER_USERNAME = 'admin'
    TEST_USER_PASSWORD = 'admin'
    TEST_USER_EMAIL = 'test_user'
    TEST_DATA_1 = {'client_first_name': 'Adm',
                   'client_last_name': 'Admin',
                   'patronymic':'Admin',
                   'sex':'М',
                   'date_born':date(1983,4,11),
                   'citizenship':'Респубика Беларусь'}

    def test_GET_user(self):
        self.client.login(username=self.TEST_USER_USERNAME, password=self.TEST_USER_PASSWORD)

        main = Client.objects.create(
                                        patronymic=self.TEST_DATA_1['patronymic'],
                                        citizenship=self.TEST_DATA_1['citizenship'],
                                        date_born=self.TEST_DATA_1['date_born'],)

        main_arr = [{'id': exp.id,
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
        self.assertEqual(response.context['data'], main_arr)
        self.assertEqual(response.status_code, 200)




    def test_page_open(self):
        self.client.login(username=self.TEST_USER_USERNAME, password=self.TEST_USER_PASSWORD)
        response = self.client.get(reverse('client_edit'))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'client/edit_forms/client_edit_main.html')

    def test_POST_no_user(self):
        self.url = reverse('client_edit')
        response = self.client.post(path=self.url, data={})
        self.assertEqual(response.status_code, 302)

    default_select_fields = ["'sex'", "'citizenship'", "'family_state'", "'children'", "'country'", "'city'", "'state'"]

    def test_GET_no_user(self):
        self.url = reverse('client_edit')
        response = self.client.get(self.url)
        self.assertQuerysetEqual(response.context['data'], self.default_select_fields)


if __name__ == "__main__":
    ClientEditMainTests()
