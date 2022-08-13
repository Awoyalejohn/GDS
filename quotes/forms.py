from django import forms
from .models import QuoteRequest


class QuoteRequestForm(forms.ModelForm):
    class Meta:
        model = QuoteRequest
        fields = '__all__'