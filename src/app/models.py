from django.db import models
from enumfields import EnumField
from fuzzywuzzy import fuzz
from geopy import distance

from .schema import Category


# Create your models here.
class Product(models.Model):
    user_id = models.CharField(max_length=255)
    username = models.CharField(max_length=255)
    item = models.CharField(max_length=255)
    category = EnumField(Category, default=Category.lilicoco)
    location_long = models.DecimalField(max_digits=9, decimal_places=6)
    location_lat = models.DecimalField(max_digits=9, decimal_places=6)
    created_at = models.DateTimeField(auto_now_add=True)

    def cal_name(self, p2):
        return fuzz.ratio(self.item, p2.item) / 100

    def cal_dist(self, p2):
        p1_location = (self.location_lat, self.location_long)
        p2_location = (p2.location_lat, p2.location_long)
        dist =  distance.distance(p1_location, p2_location).kilometers
        return 1 if 0<=dist<5 else 0.75 if 5<=dist<10 else 0.5 if 10<=dist<15 else 0.25 if 15<=dist<20 else 0

    def cal_price(self, p2):
        if isinstance(self, Supply):
            s, d = self, p2
        elif isinstance(self, Demand):
            s, d = p2, self
        if d.price_low <= s.price <= d.price_high:
            return 1
        return 0.5

    def weighted_score(self, n, d, p):
        return 50*n + 35*d + 15*p

    def recommend(self):
        if isinstance(self, Demand):
            products = Supply.objects.all()
        elif isinstance(self, Supply):
            products = Demand.objects.all()

        product_score = []
        for p in products:
            if fuzz.ratio(self.item, p.item) == 0:
                continue
            else:
                n_score = self.cal_name(p)
                d_score = self.cal_dist(p)
                p_score = self.cal_price(p)
                total_score = self.weighted_score(n_score, d_score, p_score)
                product_score.append([p, total_score])

        result = sorted(product_score, key=lambda p: p[1], reverse=True)
        if isinstance(self, Demand):
            return result[:3]
        else:
            return [i for i in result if i[1] >= 50]

class Demand(Product):
    price_low = models.IntegerField()
    price_high = models.IntegerField()


class Supply(Product):
    description = models.TextField()
    photo = models.ImageField(upload_to="images/")
    price = models.IntegerField()
