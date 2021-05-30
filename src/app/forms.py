from django import forms
from enumfields import EnumField

from app.schema import Category

from .models import Product

class ProductForm(forms.ModelForm):
    city = forms.CharField(help_text="例：台北市")
    district = forms.CharField(help_text="例：中正區")
    category = EnumField(Category, max_length=1).formfield()

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