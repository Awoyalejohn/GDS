from django import forms
from .models import QuoteRequest, QuoteOrder


class QuoteRequestForm(forms.ModelForm):
    class Meta:
        model = QuoteRequest
        exclude = ('user',)


class QuoteOrderForm(forms.ModelForm):
    class Meta:
        model = QuoteOrder
        fields = ('user','name', 'email')