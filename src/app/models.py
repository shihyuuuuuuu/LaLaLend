from django.db import models


# Create your models here.
class Product(models.Model):
    user_id = models.CharField(max_length=255)
    username = models.CharField(max_length=255)
    item = models.CharField(max_length=255)
    location_long = models.DecimalField(max_digits=9, decimal_places=6)
    location_lat = models.DecimalField(max_digits=9, decimal_places=6)
    created_at = models.DateTimeField(auto_now_add=True)


class Demand(Product):
    price_low = models.IntegerField()
    price_high = models.IntegerField()


class Supply(Product):
    description = models.TextField()
    photo = models.ImageField(upload_to="images/")
    price = models.IntegerField()
