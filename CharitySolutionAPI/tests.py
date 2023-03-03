from django.contrib.auth.models import User
from django.test import TestCase

from CharitySolutionAPI.models import OrganisationPost, Organisation
from CharitySolutionAPI import models


class TestAPI(TestCase):
    def setUp(self):
        self.test_user = User.objects.create(username="user", is_superuser=True)
        self.create_organisation = Organisation.objects.create(
            organisation_name="test_organisation",
            organisation_description="test_organisation_description",
            city="test_city",
            email="email",
            telegram_nick="telegram_nick",
            instagram_nick="instagram_nick",
            organisation_site_url="organisation_site_url",
            organisation_logo="test_logo",
        )

        self.create_organisation_post = OrganisationPost.objects.create(
            organisation=self.create_organisation,
            post_title="test_title",
            post_text="test_text",
            city="test_city",
            help_category="Another",
        )

        self.create_user = models.User.objects.create(
            user_surname="test_user_surname",
            user_first_name="test_first_surname",
            user_patronymic_name="test_patronymic_surname",
            city="test_sity",
            date_of_birth="2023-03-10 02:00:00+02",
            phone_number="+380661896330",
        )

        self.client.force_login(self.test_user)
        self.organisation = Organisation.objects.get(pk=self.test_user.id)

    def test_homepage(self):
        response = self.client.get("/")
        self.assertEqual(response.status_code, 200)

    def test_postline_page(self):
        response = self.client.get("/get_posts_list/")
        self.assertEqual(response.status_code, 200)

    def test_account_view(self):
        organisation_posts = OrganisationPost.objects.filter(
            organisation=self.test_user.id
        ).order_by("-date_created")

        response = self.client.post(
            "/get_account_view/",
            data={
                "organisation": self.organisation,
                "organisation_posts": organisation_posts,
            },
        )

        self.assertEqual(response.status_code, 200)

    def test_create_post(self):
        response = self.client.post("/create_post/")
        # After success 'create_post' page it have to be redirected to 'get_posts_list'
        self.assertEqual(response.url, "/get_posts_list")

    def test_organisation_creating_in_db(self):
        self.assertTrue(Organisation.objects.get(organisation_name="test_organisation"))

    def test_post_creating_in_db(self):
        response = OrganisationPost.objects.get(post_title="test_title")

        self.assertTrue(response)

    def test_user_creating_in_db(self):
        response = models.User.objects.get(user_surname="test_user_surname")

        self.assertTrue(response)
