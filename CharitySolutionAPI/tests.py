from django.test import TestCase
from CharitySolutionAPI.models import OrganisationPost, Organisation


class TestAPI(TestCase):
    def test_homepage(self):
        response = self.client.get('/')
        self.assertEqual(response.status_code, 200)

    # def test_edit_post(self):
    #     post_id = self.test_post_creating_in_db().id
    #     response = self.client.get(f'/edit_post/{post_id}')
    #     print(response)

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

