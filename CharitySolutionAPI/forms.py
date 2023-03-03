from .models import OrganisationPost, Organisation
from django.forms import ModelForm, TextInput, Textarea


class OrganisationPostForm(ModelForm):
    class Meta:
        model = OrganisationPost
        fields = ["post_title", "post_text", "city", "help_category", "file"]
        widgets = {
            "post_text": Textarea(
                attrs={
                    "class": "form-control col-md-3",
                    "name": "post_text",
                    "rows": "4",
                    "cols": "10",
                    "placeholder": "Write your post...",
                },
            ),
            "post_title": TextInput(
                attrs={
                    "placeholder": "Here your post title...",
                    "class": "form-control form-control-lg col-md-3",
                    "aria-label": ".form-control-lg example",
                    "name": "post_title",
                }
            ),
            "city": TextInput(
                attrs={
                    "class": "form-control col-md-3",
                    "name": "city",
                    "placeholder": "Kyiv, Kharkiv, Lviv...",
                }
            ),
        }


class OrganisationForm(ModelForm):
    class Meta:
        model = Organisation
        fields = [
            "organisation_name",
            "organisation_description",
            "city",
            "email",
            "telegram_nick",
            "instagram_nick",
            "organisation_site_url",
            "organisation_logo",
        ]

        widgets = {
            "organisation_description": Textarea(
                attrs={
                    "class": "form-control",
                    "name": "organisation_description",
                    "rows": "4",
                    "cols": "10",
                    "placeholder": "Write your organisation description...",
                },
            ),
            "organisation_name": TextInput(
                attrs={"class": "form-control", "name": "organisation_name"}
            ),
            "city": TextInput(
                attrs={
                    "class": "form-control",
                    "name": "city",
                    "placeholder": "Kyiv, Kharkiv, Lviv...",
                }
            ),
            "email": TextInput(
                attrs={
                    "class": "form-control",
                    "name": "email",
                    "placeholder": "you@example.com",
                }
            ),
            "telegram_nick": TextInput(
                attrs={
                    "class": "form-control",
                    "name": "telegram_nick",
                    "placeholder": "@Nick",
                }
            ),
            "instagram_nick": TextInput(
                attrs={
                    "class": "form-control",
                    "name": "instagram_nick",
                    "placeholder": "@Nick",
                }
            ),
            "organisation_site_url": TextInput(
                attrs={
                    "class": "form-control",
                    "name": "organisation_site_url",
                    "placeholder": "www.site.com",
                }
            ),
        }
