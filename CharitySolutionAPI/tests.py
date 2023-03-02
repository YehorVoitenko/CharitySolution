from django.contrib.auth.models import User
from django.test import TestCase
from CharitySolutionAPI.models import OrganisationPost, Organisation


class TestAPI(TestCase):
    def test_homepage(self):
        response = self.client.get('/')
        self.assertEqual(response.status_code, 200)

    def test_postline_page(self):
        response = self.client.get('/get_posts_list/')
        self.assertEqual(response.status_code, 200)

    # def test_organisation_post_form(self):
    #     # https://www.valentinog.com/blog/testing-modelform/
    #     from django.contrib.auth.models import User
    #     from django.http import HttpRequest
    #     request = HttpRequest()
    #     request.POST = {
    #         "post_title": 'test',
    #         "post_text": "test",
    #         "city": "test",
    #         "help_category": "Another",
    #         'file': 'test.png'
    #     }
    #
    #     form = OrganisationPostForm(request.POST, request.FILES)
    #
    #     self.assertTrue(form.is_valid())

    def test_organisation_creating_in_db(self):
        Organisation.objects.create(organisation_name='test_organisation',
                                    organisation_description='test_organisation_description',
                                    city='test_city', email='email', telegram_nick='telegram_nick',
                                    instagram_nick='instagram_nick', organisation_site_url='organisation_site_url',
                                    organisation_logo='test_logo')

        self.assertTrue(Organisation.objects.get(organisation_name='test_organisation'))

    def test_post_creating_in_db(self):
        Organisation.objects.create(organisation_name='test_organisation')
        organisation = Organisation.objects.get(organisation_name='test_organisation')

        OrganisationPost.objects.create(organisation=organisation, post_title='test_title', post_text='test_text',
                                        city='test_city', help_category='Another')

        response = OrganisationPost.objects.get(post_title='test_title')

        self.assertTrue(response)

        return OrganisationPost.objects.get(post_title='test_title')

