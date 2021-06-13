from django import forms
from enumfields import EnumField

from app.schema import Category

from .models import Product

class ProductForm(forms.ModelForm):
    city = forms.CharField(help_text="例：台北市")
    district = forms.CharField(help_text="例：大安區", required=False)
    category = EnumField(Category, max_length=1).formfield()

    class Meta:
        model = Product
        fields = [
            "item",
        ]

class DemandForm(ProductForm):
    price_low = forms.IntegerField(help_text="例：100")
    price_high = forms.IntegerField(help_text="例：500")


class SupplyForm(ProductForm):
    description = forms.CharField(
        help_text="填入此商品的描述，如：九成新、用不到故售",
        required=False,
        widget= forms.Textarea
    )
    photo = forms.ImageField()
    price = forms.IntegerField(help_text="您想賣（租）的金額")
    line_id = forms.CharField(help_text="您的 Line ID")
    phone_num = forms.CharField(help_text="您的聯絡電話")