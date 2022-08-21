from django import forms
from .models import Testimonial


class TestimonialForm(forms.ModelForm):
    class Meta:
        model = Testimonial
        fields = ('body',)

        labels = {
        'body': 'Your Testimonial',
    }