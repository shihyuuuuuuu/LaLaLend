from django.urls import path

from . import views

app_name = "app"

urlpatterns = [
    path('form', views.fill_in_product, name='fill-in-product'),
    path('callback', views.callback)
]
