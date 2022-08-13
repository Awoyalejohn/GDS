from django.shortcuts import render, redirect, reverse
from django.views.generic import View
from django.contrib import messages
from .forms import QuoteRequestForm
# Create your views here.
class QuoteRequestView(View):
    def get(self, request):
        form = QuoteRequestForm()
        template = 'quotes/quote_request.html'
        context = {'form': form}

        return render(request, template, context)
    
    def post(self, request):
        form = QuoteRequestForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, 'Thank you for your request')
            return redirect(reverse('quote_request'))
