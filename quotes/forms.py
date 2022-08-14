from django import forms
from .models import QuoteRequest, QuoteOrder


class QuoteRequestForm(forms.ModelForm):
    class Meta:
        model = QuoteRequest
        exclude = ('user', 'quote_request_number')


class QuoteOrderForm(forms.ModelForm):
    class Meta:
        model = QuoteOrder
        fields = ('name', 'email')