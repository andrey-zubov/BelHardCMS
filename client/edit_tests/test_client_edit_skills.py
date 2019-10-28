from django.contrib.auth import get_user_model
from django.test import TestCase
from django.urls import reverse

from client.edit.pages_get import skills_page_get
from client.edit.utility import time_it
from client.models import Skills, Client


def create_client_instance(name):  # ONLY for 'test_user' NOT 'admin'
    user = get_user_model()
    us = user.objects.get(username=name)
    return Client.objects.create(user_client=us)


def get_client_instance(name):  # ONLY for 'admin' NOT 'test_user'
    user = get_user_model()
    us = user.objects.get(username=name)
    return Client.objects.get(user_client=us)


def create_skills(name, skill):
    # test_client = create_client_instance(name)    # ONLY for 'test_user' NOT 'admin'
    test_client = get_client_instance(name)  # ONLY for 'admin' NOT 'test_user'
    for i in skill:
        Skills.objects.create(client_skills=test_client, skill=i)
    sk = skills_page_get(test_client)['cl_skill']
    return ["'%s'" % i for i in sk]  # ["'123'", "'456'"]


class ClientEditSkillsTests(TestCase):
    TEST_USER_USERNAME = 'admin'  # 'test_user'
    TEST_USER_PASSWORD = 'admin'  # 'test_user'
    TEST_SKILLS = ['Python', 'Django']

    def setUp(self) -> None:
        # user = get_user_model()   # ONLY for 'test_user' NOT 'admin'
        # user.objects.create_user(self.TEST_USER_USERNAME, 'test_user@qwe.com', self.TEST_USER_PASSWORD)
        self.url = reverse('client_edit_skills')

    @time_it
    def test_page_open(self):
        """ Open URL = client/edit/skills/ """
        self.client.login(username=self.TEST_USER_USERNAME, password=self.TEST_USER_PASSWORD)
        response = self.client.get(self.url)
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'client/edit_forms/client_edit_skills.html')

    @time_it
    def test_GET_no_user(self):
        """ Open page without User Login - AnonymousUser. """
        response = self.client.get(self.url)
        self.assertQuerysetEqual(response.context['data'], [])

    @time_it
    def test_GET_user(self):
        """ request.GET with data from skills_page_get(client). """
        self.client.login(username=self.TEST_USER_USERNAME, password=self.TEST_USER_PASSWORD)
        sk = create_skills(self.TEST_USER_USERNAME, self.TEST_SKILLS)
        response = self.client.get(self.url)
        self.assertQuerysetEqual(response.context['data']['cl_skill'], sk)

    @time_it
    def test_POST_no_user(self):
        """ request.POST without User Login - AnonymousUser. """
        response = self.client.post(path=self.url, data={})
        self.assertEqual(response.status_code, 302)  # redirect

    @time_it
    def test_POST_user(self):
        """ request.POST this LoggedIn User. """
        self.client.login(username=self.TEST_USER_USERNAME, password=self.TEST_USER_PASSWORD)
        response = self.client.post(path=self.url, data={
            'skill': self.TEST_SKILLS,
        })  # saves to DB ????
        for i in self.TEST_SKILLS:
            i_skill = Skills.objects.get(client_skills=get_client_instance(self.TEST_USER_USERNAME), skill=i)
            self.assertEquals(i_skill.skill, i)
        self.assertEquals(response.status_code, 302)  # redirect


if __name__ == "__main__":
    ClientEditSkillsTests()
