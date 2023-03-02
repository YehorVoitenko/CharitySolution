from django.test import TestCase

# Create your tests here.


class TestAPI(TestCase):
    def test_home_page(self):
        response = self.client.get("/")
        self.assertEqual(response.status_code, 200)

    def test_success_post_editing(self):
        response = self.client.post("/edit_post/1")
        self.assertEqual(response.status_code, 302)

    def test_success_account_editing(self):
        response = self.client.post("/edit_organisation_account/1")
        self.assertEqual(response.status_code, 302)
