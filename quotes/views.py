from django.shortcuts import render
from django.views.generic import View
# Create your views here.
class QuoteRequestView(View):
    def get(self, request):
        template = 'quotes/quote_request.html'
        context = {}

        return render(request, template, context)