from django import forms
from showcase.models import Product


class AddProductToBasket(forms.ModelForm):
    class Meta:
        model = Product
        fields = ['color', 'size', 'count']


class PickColor(forms.ModelForm):
    class Meta:
        model = Product
        fields = ['color']


class PickSize(forms.ModelForm):
    class Meta:
        model = Product
        fields = ['size']


class PickQuantity(forms.ModelForm):
    class Meta:
        model = Product
        fields = ['count']

