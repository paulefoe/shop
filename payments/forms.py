from django import forms
from showcase.models import Product, Color, Size


class AddProductToBasket(forms.ModelForm):
    class Meta:
        model = Product
        fields = ['color', 'size', 'count']


class PickColor(forms.Form):
    color = forms.ModelMultipleChoiceField(queryset=Color.objects.all(), required=False)


class PickSize(forms.Form):
    size = forms.ModelMultipleChoiceField(queryset=Size.objects.all(), required=False)


class PickQuantity(forms.Form):
    count = forms.IntegerField(min_value=0, required=False)

