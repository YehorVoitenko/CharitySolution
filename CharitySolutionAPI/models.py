from django.db import models

HELP_CATEGORIES = [
    ("Humanitarian aid", "Humanitarian aid"),
    ("Aid for children", "Aid for children"),
    ("Another", "Another"),
]


class Organisation(models.Model):
    organisation_name = models.CharField(max_length=100, unique=True)
    organisation_description = models.CharField(max_length=2000, null=True, blank=True)
    city = models.CharField(max_length=100, null=True, blank=True)
    email = models.EmailField(max_length=254, null=True, blank=True)
    telegram_nick = models.CharField(max_length=100, null=True, blank=True)
    instagram_nick = models.CharField(max_length=100, null=True, blank=True)
    organisation_site_url = models.CharField(max_length=100, null=True, blank=True)
    organisation_logo = models.FileField(
        null=True, blank=True, upload_to="organisation_logos"
    )

    def __str__(self):
        return self.organisation_name


class OrganisationPost(models.Model):
    organisation = models.ForeignKey(Organisation, on_delete=models.CASCADE)
    post_title = models.CharField(max_length=100)
    post_text = models.CharField(max_length=2000)
    city = models.CharField(max_length=255)
    help_category = models.CharField(
        max_length=255, choices=HELP_CATEGORIES, default="Humanitarian aid"
    )
    date_created = models.DateTimeField(auto_now_add=True)
    date_updated = models.DateTimeField(null=True)
    file = models.FileField(null=True, blank=True)

    def __str__(self):
        return self.post_title


class User(models.Model):
    user_first_name = models.CharField(max_length=255, null=False)
    user_surname = models.CharField(max_length=255, null=False)
    user_patronymic_name = models.CharField(max_length=255, null=False)
    date_of_birth = models.DateTimeField()
    city = models.CharField(max_length=255, blank=True, null=True)
    phone_number = models.CharField(max_length=13)

    def __str__(self):
        return self.user_surname
