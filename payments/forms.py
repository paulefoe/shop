from django import forms
from showcase.models import Product


class AddProductToBasket(forms.ModelForm):
    class Meta:
        model = Product
        fields = ['color', 'size', 'count']
