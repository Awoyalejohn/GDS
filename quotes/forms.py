from django import forms
from .models import QuoteRequest, QuoteOrder


class QuoteRequestForm(forms.ModelForm):
    class Meta:
        model = QuoteRequest
        fields = '__all__'


class QuoteOrderForm(forms.ModelForm):
    class Meta:
        model = QuoteOrder
        fields = '__all__'