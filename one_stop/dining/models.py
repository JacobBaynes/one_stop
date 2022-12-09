from django.db import models

# Create your models here.
class Location(models.Model):
    name = models.CharField(max_length=75, blank=True, null=True)
    phone_number = models.CharField(max_length=16, null=True)
    site = models.URLField(null=True)
    menu = models.URLField(null=True)
    hours = models.TextField()
    image = models.ImageField(upload_to='dining')