from django.db import models


class Person(models.Model):
    name = models.CharField(max_length=255)
    age = models.IntegerField()


class UsersPost(models.Model):
    post_title = models.CharField(max_length=100, null=True)
    post_text = models.CharField(max_length=2000, null=True)
    date_created = models.DateTimeField(auto_now_add=True, null=True)
    file = models.FileField(null=True)

