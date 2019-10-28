from django.test import TestCase
from django.urls import reverse


class ClientEditSkillsTests(TestCase):
    TEST_USER_USERNAME = 'admin'
    TEST_USER_PASSWORD = 'admin'

    def test_page_open(self):
        self.client.login(username=self.TEST_USER_USERNAME, password=self.TEST_USER_PASSWORD)
        response = self.client.get(reverse('client_edit_skills'))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'client/edit_forms/client_edit_skills.html')


if __name__ == "__main__":
    cl_em = ClientEditSkillsTests()
    cl_em.test_page_open()
