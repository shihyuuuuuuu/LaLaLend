from django.db import models
from enumfields import EnumField
from geopy import distance

from .schema import Category


# Create your models here.
class Product(models.Model):
    user_id = models.CharField(max_length=255)
    item = models.CharField(max_length=255)
    category = EnumField(Category, default=Category.lilicoco)
    location_long = models.DecimalField(max_digits=9, decimal_places=6)
    location_lat = models.DecimalField(max_digits=9, decimal_places=6)
    created_at = models.DateTimeField(auto_now_add=True)

    def cal_name(self, p2):
        return len(set(self.item) & set(p2.item)) / len(self.item)

    def cal_dist(self, p2):
        p1_location = (self.location_lat, self.location_long)
        p2_location = (p2.location_lat, p2.location_long)
        dist =  distance.distance(p1_location, p2_location).kilometers
        
        if 0 <= dist < 5:
            score, string = [1, "< 5 公里"]
        elif 5 <= dist < 10:
            score, string = [0.75, "5~10 公里"]
        elif 10 <= dist < 15:
            score, string = [0.5, "10~15 公里"]
        elif 15 <= dist < 20:
            score, string = [0.25, "15~20 公里"]
        elif 20 <= dist:
            score, string = [0.0, "> 20 公里"]
        else:
            score, string = [0.0, "未知 公里"]
        
        return [score, string]

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
            products = Supply.objects.filter(category=self.category)
        elif isinstance(self, Supply):
            products = Demand.objects.filter(category=self.category)

        product_score = []
        for p in products:
            if len(set(self.item) & set(p.item)) / len(self.item) < 0.3:
                continue
            else:
                n_score = self.cal_name(p)
                d_score, dist = self.cal_dist(p)
                p_score = self.cal_price(p)
                total_score = self.weighted_score(n_score, d_score, p_score)
                product_score.append([p, total_score, dist])

        result = sorted(product_score, key=lambda p: p[1], reverse=True)
        if isinstance(self, Demand):
            return result[:3]
        else:
            return [i for i in result if i[1] >= 20]
    
    def __str__(self) -> str:
        return self.item

class Demand(Product):
    price_low = models.IntegerField()
    price_high = models.IntegerField()


class Supply(Product):
    description = models.TextField()
    photo = models.ImageField(max_length=255, upload_to="images/")
    price = models.IntegerField()
    line_id =  models.CharField(max_length=255, blank=True)
    phone_num = models.CharField(max_length=255, blank=True)
