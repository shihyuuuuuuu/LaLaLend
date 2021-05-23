from django import forms
from .models import Demand, Product, Supply

class ProductForm(forms.ModelForm):
    class Meta:
        model = Product
        fields = [
            "username",
            "item",
            "location_long",
            "location_lat",
        ]

class DemandForm(ProductForm):
    price_low = forms.IntegerField()
    price_high = forms.IntegerField()


class SupplyForm(ProductForm):
    description = forms.CharField(widget= forms.Textarea,required=True)
    photo = forms.ImageField()
    price = forms.IntegerField()