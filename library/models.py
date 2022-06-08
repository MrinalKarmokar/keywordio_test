from django.db import models

class Book(models.Model):
    title = models.CharField(max_length=255)
    author = models.CharField(max_length=255)
    num_pages = models.IntegerField()
    publication = models.CharField(max_length=255)
    publisher = models.CharField(max_length=255)