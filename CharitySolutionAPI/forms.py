from .models import OrganisationPost, Organisation, User
from django.forms import ModelForm, TextInput, Textarea, EmailInput, PasswordInput


class OrganisationPostForm(ModelForm):
    class Meta:
        model = OrganisationPost
        fields = [
            "post_title",
            "post_text",
            "city",
            "help_category",
            "file",
            "meeting_date",
            "meeting_time",
        ]
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
            "meeting_date": TextInput(attrs={"type": "date"}),
            "meeting_time": TextInput(attrs={"type": "time"}),
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


class UserForm(ModelForm):
    class Meta:
        model = User
        fields = [
            "date_of_birth",
            "user_first_name",
            "user_surname",
            "user_patronymic_name",
            "city",
            "phone_number",
            "email",
            "password",
        ]
        widgets = {
            "user_first_name": TextInput(
                attrs={
                    "class": "form-control col-md-3",
                    "name": "user_first_name",
                    "placeholder": "Your name",
                }
            ),
            "user_surname": TextInput(
                attrs={
                    "class": "form-control col-md-3",
                    "name": "user_surname",
                    "placeholder": "Your surname",
                }
            ),
            "user_patronymic_name": TextInput(
                attrs={
                    "class": "form-control  col-md-3",
                    "name": "user_patronymic_name",
                    "placeholder": "Your patronymic name",
                }
            ),
            "city": TextInput(
                attrs={
                    "class": "form-control  col-md-3",
                    "name": "city",
                    "placeholder": "Kyiv, Kharkiv, Lviv...",
                }
            ),
            "phone_number": TextInput(
                attrs={
                    "type": "tel",
                    "class": "form-control  col-md-3",
                    "name": "phone_number",
                    "placeholder": "+380 050 00 00 000",
                }
            ),
            "email": EmailInput(
                attrs={
                    "class": "form-control  col-md-3",
                    "name": "email",
                    "placeholder": "user@gmail.com",
                }
            ),
            "password": PasswordInput(
                attrs={
                    "type": "password",
                    "class": "form-control  col-md-3",
                    "placeholder": "Password",
                }
            ),
            "date_of_birth": TextInput(attrs={"type": "date"}),
        }
