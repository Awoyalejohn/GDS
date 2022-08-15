from django import forms
from .models import QuoteRequest, QuoteOrder


class QuoteRequestForm(forms.ModelForm):
    class Meta:
        model = QuoteRequest
        exclude = ('user', 'quote_request_number')

        labels = {
            'type': 'What type of design do you need?',
            'size': 'What size?',
        }

    def __init__(self, *args, **kwargs):
        super(QuoteRequestForm, self).__init__(*args, **kwargs)
        self.fields['name'].widget.attrs['placeholder'] = 'Give the design a name'
        self.fields['description'].widget.attrs['placeholder'] = 'Write a description here'
    



class QuoteOrderForm(forms.ModelForm):
    class Meta:
        model = QuoteOrder
        fields = ('name', 'email')