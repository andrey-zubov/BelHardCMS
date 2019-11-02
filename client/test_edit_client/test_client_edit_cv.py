from django.contrib.auth import get_user_model
from django.test import TestCase
from django.urls import reverse

from client.edit.pages_get import cv_page_get
from client.edit.utility import time_it
from client.models import Client, CV, Employment, TimeJob, TypeSalary, Direction


# def get_client_instance(name):
#     user = get_user_model()
#     us = user.objects.get(username=name)
#     return Client.objects.get(user_client=us)


class ClientEditCVTests(TestCase):
    """ python manage.py test client/test_edit_client/ --keepdb """
    TEST_USER_USERNAME = 'test_user'
    TEST_USER_PASSWORD = 'test_user'
    TEST_USER_EMAIL = 'test_user'
    TEST_DATA = {'position': 'jun',
                 'direction': Direction.objects.all()[0].id,  # pre defined array
                 'employment': Employment.objects.all()[0],  # pre defined array
                 'time_job': TimeJob.objects.all()[0],  # pre defined array
                 'salary': '100',
                 'type_salary': TypeSalary.objects.all()[0],  # pre defined array
                 }
    default_select_fields = ["'employment'", "'time_job'", "'type_salary'", "'direction'"]

    def setUp(self) -> None:
        user = get_user_model()
        self.test_user = user.objects.create_user(self.TEST_USER_USERNAME, self.TEST_USER_EMAIL,
                                                  self.TEST_USER_PASSWORD)
        self.client_inst = Client.objects.create(user_client=self.test_user)
        self.url = reverse('client_edit_cv')

    @time_it
    def test_page_open(self):
        """ Open URL = client/edit/cv/ """
        self.client.login(username=self.TEST_USER_USERNAME, password=self.TEST_USER_PASSWORD)
        response = self.client.get(self.url)
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'client/edit_forms/client_edit_cv.html')

    @time_it
    def test_GET_no_user(self):
        """ Open page without User Login - AnonymousUser. """
        response = self.client.get(self.url)
        self.assertQuerysetEqual(response.context['data'], self.default_select_fields)

    @time_it
    def test_GET_user(self):
        """ request.GET with data from skills_page_get(client). """
        self.client.login(username=self.TEST_USER_USERNAME, password=self.TEST_USER_PASSWORD)

        CV.objects.create(client_cv=self.client_inst,
                          position=self.TEST_DATA['position'],
                          direction=Direction.objects.all()[0],
                          employment=self.TEST_DATA['employment'],
                          time_job=self.TEST_DATA['time_job'],
                          salary=self.TEST_DATA['salary'],
                          type_salary=self.TEST_DATA['type_salary'],
                          )
        cv_arr = cv_page_get(self.client_inst)['cl_cvs']
        # print(cv_arr)
        response = self.client.get(self.url)
        # print(response.context['data']['cl_cvs'])
        self.assertEqual(response.context['data']['cl_cvs'], cv_arr)
        self.assertEqual(response.status_code, 200)

    @time_it
    def test_POST_no_user(self):
        """ request.POST without User Login - AnonymousUser. """
        response = self.client.post(path=self.url, data={})
        self.assertEqual(response.status_code, 302)  # redirect

    @time_it
    def test_POST_user(self):
        """ request.POST this LoggedIn User. """
        self.client.login(username=self.TEST_USER_USERNAME, password=self.TEST_USER_PASSWORD)

        response = self.client.post(path=self.url, data=self.TEST_DATA)  # saves to DB ????

        user_cv = CV.objects.get(client_cv=self.client_inst)

        self.assertEqual(user_cv.position, self.TEST_DATA['position'])
        self.assertEqual(user_cv.direction.id, self.TEST_DATA['direction'])
        self.assertEqual(user_cv.employment, self.TEST_DATA['employment'])
        self.assertEqual(user_cv.time_job, self.TEST_DATA['time_job'])
        self.assertEqual(user_cv.salary, self.TEST_DATA['salary'])
        self.assertEqual(user_cv.type_salary, self.TEST_DATA['type_salary'])

        self.assertEquals(response.status_code, 302)  # redirect


if __name__ == "__main__":
    ClientEditCVTests()
