from django.forms import ModelForm
from django import forms
from .models import Product


class ProductForm(ModelForm):
    class Meta:
        model = Product
        fields = ['category', 'title', 'description', 'price']


class AddToCartForm(forms.Form):
    quantity = forms.IntegerField()


class CheckoutForm(forms.Form):
    first_name = forms.CharField(max_length=255)
    last_name = forms.CharField(max_length=255)
    email = forms.EmailField(max_length=255)
    phone = forms.CharField(max_length=255)
    address = forms.CharField(max_length=255)
    zipcode = forms.CharField(max_length=255)
