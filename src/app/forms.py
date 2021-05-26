from django import forms
from .models import Product

class ProductForm(forms.ModelForm):
    city = forms.CharField(help_text="例：台北市")
    district = forms.CharField(help_text="例：中正區")
    village = forms.CharField(help_text="例：建國里")

    class Meta:
        model = Product
        fields = [
            "username",
            "item",
        ]

class DemandForm(ProductForm):
    price_low = forms.IntegerField()
    price_high = forms.IntegerField()


class SupplyForm(ProductForm):
    description = forms.CharField(widget= forms.Textarea,required=True)
    photo = forms.ImageField()
    price = forms.IntegerField()