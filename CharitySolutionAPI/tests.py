from django.db.models.query import QuerySet
from django.contrib.auth.models import User as Auth_User
from django.test import TestCase, Client

from CharitySolutionAPI.models import OrganisationPost, Organisation
from CharitySolutionAPI import models


class TestAPI(TestCase):
    def setUp(self):
        self.client = Client()

        # Create auth user, this case its organisation
        self.create_auth_organisation = Auth_User.objects.create(
            username="organisation", is_superuser=True
        )
        self.get_auth_organisation = Auth_User.objects.get(username="organisation")

        # Create auth user, this case its just user
        self.create_auth_organisation = Auth_User.objects.create(
            username="user", is_superuser=False, is_staff=False
        )
        self.get_auth_user = Auth_User.objects.get(username="user")

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
            client_id=self.get_auth_organisation,
        )
        self.get_organisation = Organisation.objects.get(
            organisation_name="test_organisation"
        )

        # Create organisation post
        self.create_organisation_post = OrganisationPost.objects.create(
            organisation=self.get_organisation,
            post_title="test_title",
            post_text="test_text",
            city="test_city",
            help_category="Another",
            date_created="2023-03-09 18:52:40.411183+02",
            meeting_date="2023-03-23 02:00:00+02",
            meeting_time="22:54:00",
        )
        self.get_organisation_post = OrganisationPost.objects.get(
            post_title="test_title"
        )

        # Create ordinary site user
        self.create_user = models.User.objects.create(
            user_surname="test_user_surname",
            user_first_name="test_first_surname",
            user_patronymic_name="test_patronymic_surname",
            city="test_sity",
            date_of_birth="2023-03-10 02:00:00+02",
            phone_number="+380661896330",
            client_id=self.get_auth_organisation,
        )
        self.get_user = models.User.objects.get(user_surname="test_user_surname")

        # Force loging just by auth user
        self.client.force_login(self.get_auth_organisation)

    # Method return rows from table
    @staticmethod
    def get_values_from_db(db_name: "QuerySet") -> dict:
        return list(db_name.objects.values())[0].values()

    def test_homepage(self):
        response = self.client.get("/")

        # Check response status code
        self.assertEqual(response.status_code, 200)

    def test_post_roll_page(self):
        response = self.client.get("/get_post_roll/")

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
            organisation=self.get_auth_organisation.id
        ).order_by("-date_created")

        # Posting data to page
        response = self.client.get(
            "/get_organisation_account_view/",
            data={
                "organisation": self.get_organisation,
                "organisation_posts": organisation_posts,
            },
        )

        self.assertEqual(response.status_code, 200)

        # Check if the organisation info exists at page
        for element in self.get_values_from_db(Organisation):
            self.assertContains(response, element)

    def test_create_post(self):
        response = self.client.post("/create_post/")

        # After success 'create_post' page it have to be redirected to 'get_post_roll'
        self.assertEqual(response.url, "/get_post_roll")

    def test_post_roll(self):
        response = self.client.get("/get_post_roll/")

        # Check if the post exists at page
        self.assertContains(response, "test_title")
        self.assertContains(response, "test_organisation")
        self.assertContains(response, "test_city")
        self.assertContains(response, "Another")

        # Check if the button for getting more info is exists
        self.assertContains(response, "get_more_info_about_post")

    def test_user_logout(self):
        self.client.get("/logout_current_client/")
        response = self.client.get("/create_post/")
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "Not enough privileges to perform an action")

    def test_login_navbar_elements_organisation_view(self):
        self.client.logout()
        self.client.force_login(self.get_auth_organisation)
        homepage_response = self.client.get("/")
        self.assertContains(
            homepage_response,
            '<a class="nav-link" href="/get_organisation_account_view/">Account</a>',
        )
        self.assertContains(
            homepage_response,
            ' <a class="nav-link" href="/logout_current_client/">LogOut</a>',
        )
        self.assertContains(
            homepage_response,
            ' <a class="nav-link" href="/get_post_roll/">Wall<span class="sr-only">(current)</span></a>',
        )

    def test_logout_navbar_elements(self):
        self.client.logout()
        homepage_response = self.client.get("/")
        self.assertNotContains(
            homepage_response,
            '<a class="nav-link" href="/get_organisation_account_view/">Account</a>',
        )
        self.assertNotContains(
            homepage_response,
            ' <a class="nav-link" href="/logout_current_client/">LogOut</a>',
        )
        self.assertContains(
            homepage_response,
            ' <a class="nav-link" href="/get_post_roll/">Wall<span class="sr-only">(current)</span></a>',
        )
        self.assertContains(
            homepage_response, ' <a class="nav-link" href="/login_user/">LogIn</a>'
        )

    def test_organisation_bio(self):
        response = self.client.get(f"/organisation_bio/{self.get_organisation.id}")
        self.assertContains(response, f"<h4><b>Name:</b> test_organisation</h4>")
        self.assertContains(response, "test_organisation_description<br></h4>")
        self.assertContains(response, "<h4><b>City: </b>test_city</h4>")
        self.assertContains(response, "<h4><b>Email: </b>email</h4>")
        self.assertContains(response, "<h4><b>Telegram: </b>telegram_nick\n    </h4>")
        self.assertContains(response, "<h4><b>Instagram: </b>instagram_nick\n    </h4>")
        self.assertContains(
            response,
            '<h4><b>Site: </b>\n        <a href="https://organisation_site_url">organisation_site_url</a></h4>',
        )
