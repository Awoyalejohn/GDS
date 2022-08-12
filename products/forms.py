from django import forms
from .widgets import CustomClearableFileInput
from .models import Product


class ProductForm(forms.ModelForm):

    class Meta:
        model = Product
        # Renders all fields except for the slug field
        exclude = ('slug',)

    image = forms.ImageField(label='Image', required=False, widget=CustomClearableFileInput)