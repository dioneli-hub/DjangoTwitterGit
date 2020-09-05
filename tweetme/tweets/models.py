from django.db import models


class Tweet(models.Model):
    # maps to SQL-data
    content = models.TextField(blank=True, null=True)
    image = models.FileField(blank=True, null=True) # upload_to=
