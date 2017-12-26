from django import forms

from showcase.models import Product, Color, Size
from .models import Order, OrderItem


class AddProductToBasket(forms.ModelForm):
    class Meta:
        model = Product
        fields = ['color', 'size', 'count']


class PickColor(forms.Form):
    color = forms.ModelMultipleChoiceField(queryset=Color.objects.all(), required=False)
    # colors = Color.objects.all()
    # choices = [a.color for a in colors]
    # color = forms.ChoiceField(choices=choices)


class PickSize(forms.Form):
    size = forms.ModelMultipleChoiceField(queryset=Size.objects.all(), required=False)


class PickQuantity(forms.Form):
    count = forms.IntegerField(min_value=0, required=False)

