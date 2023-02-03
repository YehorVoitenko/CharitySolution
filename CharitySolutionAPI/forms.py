from .models import OrganisationPost
from django.forms import ModelForm, TextInput, Textarea


class OrganisationPostForm(ModelForm):
    class Meta:
        model = OrganisationPost
        fields = ["post_title", "post_text", "file"]
        widgets = {'post_text': Textarea(
            attrs={
                "class": "form-control col-md-3",
                "name": "post_text",
                "rows": "4",
                "cols": "10",
                "placeholder": "Write your post..."
            },
        ),
            'post_title': TextInput(
                attrs={
                    "placeholder": "Here your post title...",
                    "class": "form-control form-control-lg col-md-3",
                    "aria-label": ".form-control-lg example",
                    "name": "post_title"
                })
        }
