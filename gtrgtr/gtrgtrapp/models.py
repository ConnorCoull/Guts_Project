from django.db import models

# Create your models here.
class Guitars(models.Model):
    incrementingIndex = models.AutoField(primary_key=True)
    itemName = models.CharField()
    brandName = models.CharField()
    description = models.TextField()
    salesPrice = models.IntegerField()
    pictureMain = models.URLField()
    qtyInStock = models.IntegerField()
    qtyOnOrder = models.IntegerField()
    colour = models.CharField()
    pickup = models.CharField()
    bodyShape = models.CharField()
    spotifyPreviewURL = models.URLField()

    def __str__(self):
        return self.itemName