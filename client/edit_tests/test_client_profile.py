from django.test import TestCase
from django.urls import reverse


# BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
# path = os.path.expanduser(BASE_DIR)
# if path not in sys.path:
#     sys.path.insert(0, path)
# os.environ.setdefault("DJANGO_SETTINGS_MODULE", "BelHardCRM.settings")
# django.setup()


class ClientProfileTests(TestCase):
    TEST_USER_USERNAME = 'admin'
    TEST_USER_PASSWORD = 'admin'

    def test_page_open(self):
        self.client.login(username=self.TEST_USER_USERNAME, password=self.TEST_USER_PASSWORD)
        response = self.client.get(reverse('client_profile'))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'client/client_profile.html')


if __name__ == "__main__":
    cl_pr = ClientProfileTests()
    cl_pr.test_page_open()
