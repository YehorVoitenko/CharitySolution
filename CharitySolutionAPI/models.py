from django.db import models


class Organisation(models.Model):
    organisation_name = models.CharField(max_length=100)


class OrganisationPost(models.Model):
    organisation = models.ForeignKey(Organisation, on_delete=models.CASCADE)
    post_title = models.CharField(max_length=100)
    post_text = models.CharField(max_length=2000)
    date_created = models.DateTimeField(auto_now_add=True)
    file = models.FileField(null=True, blank=True)

    def __str__(self):
        return self.post_title