from django.db import models
from django.contrib.auth import get_user_model
from django.core.validators import RegexValidator

User = get_user_model()

HELP_CATEGORIES = [
    ("Humanitarian aid", "Humanitarian aid"),
    ("Aid for children", "Aid for children"),
    ("Another", "Another"),
]


class Organisation(models.Model):
    client_id = models.ForeignKey(User, on_delete=models.CASCADE)
    organisation_name = models.CharField(max_length=100, unique=True)
    organisation_description = models.CharField(max_length=2000, null=True, blank=True)
    city = models.CharField(max_length=100, null=True, blank=True)
    email = models.EmailField(max_length=254, null=True, blank=True, unique=True)
    telegram_nick = models.CharField(max_length=100, null=True, blank=True, unique=True)
    instagram_nick = models.CharField(
        max_length=100, null=True, blank=True, unique=True
    )
    organisation_site_url = models.CharField(
        max_length=100, null=True, blank=True, unique=True
    )
    organisation_logo = models.FileField(
        null=True,
        blank=True,
        upload_to="organisation_logos",
        default="organisation_logos/default_logo/default_organisation_logo.jpeg",
    )

    class Meta:
        indexes = [
            models.Index(fields=['client_id'], name='organisation_name_idx'),
        ]

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
    meeting_date = models.DateTimeField(null=True, blank=True)
    meeting_time = models.TimeField(null=True, blank=True)
    file = models.FileField(null=True, blank=True)

    def __str__(self):
        return self.post_title


class User(models.Model):
    phone_regex = RegexValidator(regex=r"^\+?1?\d{10,13}$")

    client_id = models.ForeignKey(User, on_delete=models.CASCADE)
    user_first_name = models.CharField(max_length=255, null=False)
    user_surname = models.CharField(max_length=255, null=False)
    user_patronymic_name = models.CharField(max_length=255, null=False)
    date_of_birth = models.DateTimeField(null=True, blank=True)
    city = models.CharField(max_length=255, blank=True, null=True)
    phone_number = models.CharField(
        validators=[phone_regex], max_length=13, null=True, unique=True
    )
    email = models.EmailField(null=True, blank=True, unique=True)
    password = models.CharField(max_length=8, null=False)

    def __str__(self):
        return self.user_surname
