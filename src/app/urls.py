from django.urls import path

from . import views

app_name = "app"

urlpatterns = [
    path('', views.home),
    path('form', views.product_form, name='product-form'),
    path('callback', views.callback),
]
