from django.db import models


class UsersPost(models.Model):
    post_title = models.CharField(max_length=100)
    post_text = models.CharField(max_length=2000)
    date_created = models.DateTimeField(auto_now_add=True)
    file = models.FileField(blank=True, null=True)
