from django.contrib import admin
from .models import Product, Demand, Supply

# Register your models here.


admin.site.register(Product)
admin.site.register(Demand)
admin.site.register(Supply)