from unittest.util import _MAX_LENGTH
from django.db import models

# Create your models here.


class Guitars(models.Model):
    incrementingIndex = models.AutoField(primary_key=True)
    itemName = models.CharField(max_length=200)
    brandName = models.CharField(max_length=200)
    description = models.TextField()
    salesPrice = models.IntegerField()
    pictureMain = models.URLField()
    qtyInStock = models.IntegerField()
    qtyOnOrder = models.IntegerField()
    colour = models.CharField(max_length=200)
    pickup = models.CharField(max_length=200)
    bodyShape = models.CharField(max_length=200)
    spotifyPreviewURL = models.URLField()

    def __str__(self):
        return self.itemName
