from django import forms
from .models import Product


class ProductForm(forms.ModelForm):

    class Meta:
        model = Product
        # Renders all fields except for the slug field
        exclude = ('slug',)
