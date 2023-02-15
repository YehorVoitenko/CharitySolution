from django.db import models


class Organisation(models.Model):
    organisation_name = models.CharField(max_length=100, unique=True)
    organisation_description = models.CharField(max_length=2000)
    city = models.CharField(max_length=100, null=True)
    email = models.EmailField(max_length=254, null=True)
    telegram_nick = models.CharField(max_length=100, null=True)
    instagram_nick = models.CharField(max_length=100, null=True)
    organisation_site_url = models.CharField(max_length=100, null=True)
    organisation_logo = models.FileField(null=True, blank=True, upload_to='organisation_logos')


class OrganisationPost(models.Model):
    organisation = models.ForeignKey(Organisation, on_delete=models.CASCADE)
    post_title = models.CharField(max_length=100)
    post_text = models.CharField(max_length=2000)
    date_created = models.DateTimeField(auto_now_add=True)
    date_updated = models.DateTimeField(null=True)
    file = models.FileField(null=True, blank=True)

    def __str__(self):
        return self.post_title
