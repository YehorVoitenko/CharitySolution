from django.db.models.query import QuerySet
from django.contrib.auth.models import User as Auth_User
from django.test import TestCase

from CharitySolutionAPI.models import OrganisationPost, Organisation
from CharitySolutionAPI import models


class TestAPI(TestCase):
    def setUp(self):
        # Create auth user, this case its organisation
        self.create_auth_organisation = Auth_User.objects.create(
            username="organisation", is_superuser=True
        )

        # Create organisation
        self.create_organisation = Organisation.objects.create(
            organisation_name="test_organisation",
            organisation_description="test_organisation_description",
            city="test_city",
            email="email",
            telegram_nick="telegram_nick",
            instagram_nick="instagram_nick",
            organisation_site_url="organisation_site_url",
            organisation_logo="test_logo",
            client_id=self.create_auth_organisation,
        )

        # Create organisation post
        self.create_organisation_post = OrganisationPost.objects.create(
            organisation=self.create_organisation,
            post_title="test_title",
            post_text="test_text",
            city="test_city",
            help_category="Another",
            date_created="2023-03-09 18:52:40.411183+02",
            meeting_date="2023-03-23 02:00:00+02",
            meeting_time="22:54:00",
        )

        # Create ordinary site user
        self.create_user = models.User.objects.create(
            user_surname="test_user_surname",
            user_first_name="test_first_surname",
            user_patronymic_name="test_patronymic_surname",
            city="test_sity",
            date_of_birth="2023-03-10 02:00:00+02",
            phone_number="+380661896330",
            client_id=self.create_auth_organisation,
        )

        # Force loging just by auth user
        self.client.force_login(self.create_auth_organisation)

        # TODO: Replace it by static method or by instance method
        self.organisation = Organisation.objects.get(
            pk=self.create_auth_organisation.id
        )

    # Method return rows from table
    @staticmethod
    def get_values_from_db(db_name: "QuerySet") -> dict:
        return list(db_name.objects.values())[0].values()

    # Method return columns from table
    @staticmethod
    def get_keys_from_db(db_name: "QuerySet") -> dict:
        return list(db_name.objects.keys())[0].keys()

    def test_homepage(self):
        response = self.client.get("/")

        # Check response status code
        self.assertEqual(response.status_code, 200)

    def test_postline_page(self):
        response = self.client.get("/get_posts_list/")

        # Check response status code
        self.assertEqual(response.status_code, 200)

        users_info_in_page = [
            "test_title",
            "test_organisation",
            "test_city",
            "Another",
        ]

        # Check if the post exists at page
        for element in users_info_in_page:
            self.assertContains(response, element)

        # Check if the button for getting more info is exists
        self.assertContains(response, "get_more_info_about_post")

    def test_account_view(self):
        organisation_posts = OrganisationPost.objects.filter(
            organisation=self.create_auth_organisation.id
        ).order_by("-date_created")

        # Posting data to page
        response = self.client.post(
            "/get_organisation_account_view/",
            data={
                "organisation": self.organisation,
                "organisation_posts": organisation_posts,
            },
        )

        self.assertEqual(response.status_code, 200)

        # Check if the organisation info exists at page
        for element in self.get_values_from_db(Organisation):
            self.assertContains(response, element)

    def test_create_post(self):
        response = self.client.post("/create_post/")

        # After success 'create_post' page it have to be redirected to 'get_posts_list'
        self.assertEqual(response.url, "/get_posts_list")

    def test_organisation_creating_in_db(self):
        # Check if organisation was created
        organisation = Organisation.objects.get(organisation_name="test_organisation")
        self.assertTrue(organisation)
        return organisation

    def test_post_creating_in_db(self):
        # Check if organisation post was created
        self.assertTrue(OrganisationPost.objects.get(post_title="test_title"))

    def test_user_creating_in_db(self):
        # Check if auth user was created
        self.assertTrue(models.User.objects.get(user_surname="test_user_surname"))

    def test_postline(self):
        response = self.client.get("/get_posts_list/")

        # Check if the post exists at page
        self.assertContains(response, "test_title")
        self.assertContains(response, "test_organisation")
        self.assertContains(response, "test_city")
        self.assertContains(response, "Another")

        # Check if the button for getting more info is exists
        self.assertContains(response, "get_more_info_about_post")


# TODO: recreate SQL requests, because every time created auth_user. CHECK BY: User.objects.values()

# TODO: add testing for logout organisation and login user

# TODO: check if navbar changing by login user or login organisation
