from django.urls import path

from .views import fill_in_product

app_name = "app"

urlpatterns = [
    path('form', fill_in_product, name='fill-in-product'),
]
