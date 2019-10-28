from django.contrib.auth import get_user_model
from django.test import TestCase
from django.urls import reverse

from client.edit.pages_get import skills_page_get
from client.models import Skills, Client


def create_client_instance(name):
    user = get_user_model()
    us = user.objects.get(username=name)
    return Client.objects.create(user_client=us)


def create_skills(name, skill):
    test_client = create_client_instance(name)
    for i in skill:
        Skills.objects.create(client_skills=test_client, skill=i)
    sk = skills_page_get(test_client)['cl_skill']
    return ["'%s'" % i for i in sk]  # ["'123'", "'456'"]


class ClientEditSkillsTests(TestCase):
    TEST_USER_USERNAME = 'test_user'
    TEST_USER_PASSWORD = 'test_user'
    test_skills = ('123', '456')

    def setUp(self) -> None:
        user = get_user_model()
        user.objects.create_user(self.TEST_USER_USERNAME, 'test_user@qwe.com', self.TEST_USER_PASSWORD)

    def test_page_open(self):
        self.client.login(username=self.TEST_USER_USERNAME, password=self.TEST_USER_PASSWORD)
        response = self.client.get(reverse('client_edit_skills'))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'client/edit_forms/client_edit_skills.html')

    def test_get_response_zero(self):
        response = self.client.get(reverse('client_edit_skills'))
        self.assertQuerysetEqual(response.context['data'], [])

    def test_get_response_user(self):
        self.client.login(username=self.TEST_USER_USERNAME, password=self.TEST_USER_PASSWORD)
        sk = create_skills(self.TEST_USER_USERNAME, self.test_skills)
        response = self.client.get(reverse('client_edit_skills'))
        self.assertQuerysetEqual(
            response.context['data']['cl_skill'],
            sk)


if __name__ == "__main__":
    cl_em = ClientEditSkillsTests()
    cl_em.test_page_open()
