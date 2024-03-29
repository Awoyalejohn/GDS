from urllib import request
from django.urls import reverse_lazy
from django.shortcuts import render, redirect, reverse, get_object_or_404
from django.http import HttpResponseRedirect
from django.views.generic import (
    View,
    TemplateView,
    ListView,
    CreateView,
    UpdateView
)
from django.contrib import messages
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth.mixins import UserPassesTestMixin
from django.core.mail import send_mail
from django.template.loader import render_to_string
from django.conf import settings
from profiles.models import UserProfile
from .models import QuoteOrder, QuoteFufillment
from .forms import QuoteRequestForm, QuoteOrderForm, QuoteFufillmentForm
from math import ceil
import uuid
import stripe


class QuoteRequestView(LoginRequiredMixin, View):
    """A view to request and purchase a specific graphic design"""

    def get(self, request):
        stripe_public_key = settings.STRIPE_PUBLIC_KEY
        stripe_secret_key = settings.STRIPE_SECRET_KEY
        stripe.api_key = stripe_secret_key
        form = QuoteRequestForm()

        template = "quotes/quote_request.html"
        context = {
            "form": form,
            "stripe_public_key": stripe_public_key,
            "stripe_secret_key": stripe_secret_key,
        }

        return render(request, template, context)

    def post(self, request):
        type_cost = None
        selected_type = None
        type = request.POST["type"]
        if type == "IC" or type == "ST":
            type_cost = 9.99
            if type == "IC":
                selected_type = "Icon"
            else:
                selected_type = "Sticker"
        elif type == "LG" or type == "BN":
            type_cost = 19.99
            if type == "LG":
                selected_type = "Logo"
            else:
                selected_type = "Banner"
        elif type == "PS" or type == "WP":
            type_cost = 39.99
            if type == "PS":
                selected_type = "Poster"
            else:
                selected_type = "Wallpaper"
        else:
            messages.error(request, "Something went wrong wth your request")
            return redirect(reverse("quote_request"))

        size_cost = None
        selected_size = None

        size = request.POST["size"]
        if size == "S":
            size_cost = 9.99
            selected_size = "Small"
        elif size == "M":
            size_cost = 19.99
            selected_size = "Medium"
        elif size == "L":
            size_cost = 29.99
            selected_size = "Large"
        else:
            messages.error(request, "Something went wrong wth your request")
            return redirect(reverse("quote_request"))

        subtotal = round(type_cost + size_cost, 2)

        if subtotal > settings.DISCOUNT_THRESHOLD:
            discount = ceil(subtotal * settings.DISCOUNT_PERCENTAGE / 100)

        else:
            discount = 0

        total = round(subtotal - discount, 2)

        quote_item_name = request.POST["name"]
        quote_description = request.POST["description"]

        form = QuoteRequestForm(request.POST)
        form.instance.user = UserProfile.objects.get(user=self.request.user)
        uuid_number = str(uuid.uuid4())
        form.instance.quote_request_number = uuid_number
        if form.is_valid():
            form.save()
            request.session["quote_item_name"] = quote_item_name
            request.session["quote_description"] = quote_description
            request.session["quote_subtotal"] = subtotal
            request.session["quote_discount"] = discount
            request.session["quote_total"] = total
            request.session["selected_type"] = selected_type
            request.session["selected_size"] = selected_size
            request.session["quote_request_number"] = uuid_number
            request.session["from_quote_request"] = True
            messages.info(
                request,
                "Just need some more information to complete your order."
            )
            return HttpResponseRedirect(reverse("quote_checkout"))


class QuoteCheckoutView(LoginRequiredMixin, View):
    """
    A view to checkout quote after
    getting the data from the QuoteRequestView
    """
    def get(self, request):
        # Checks if the user was sent here from quote request view
        if "from_quote_request" not in request.session:
            messages.info(
                request,
                "You need to submit a request before checkout!"
            )
            return HttpResponseRedirect(reverse("quote_request"))
        # Removes from_quote_request key from the session to prevent
        # access to the checkout view if it was not from the quote request view
        request.session.pop("from_quote_request")

        stripe_public_key = settings.STRIPE_PUBLIC_KEY
        stripe_secret_key = settings.STRIPE_SECRET_KEY

        data_dict = {
            "name": self.request.user,
            "email": UserProfile.objects.get(
                user=self.request.user
                ).user.email,
        }

        form = QuoteOrderForm(data_dict)
        quote_item_name = request.session["quote_item_name"]
        quote_description = request.session["quote_description"]
        quote_subtotal = request.session["quote_subtotal"]
        quote_discount = request.session["quote_discount"]
        quote_total = request.session["quote_total"]
        selected_type = request.session["selected_type"]
        selected_size = request.session["selected_size"]
        quote_order_number = request.session["quote_request_number"]

        stripe_total = round(quote_total * 100)
        stripe.api_key = stripe_secret_key
        payment_intent = stripe.PaymentIntent.create(
            amount=stripe_total,
            currency=settings.STRIPE_CURRENCY,
        )

        if not stripe_public_key:
            messages.warning(
                request,
                "Stripe public key is missing. \
                Did you forget to set in your environment?",
            )

        template = "quotes/quote_checkout.html"

        context = {
            "form": form,
            "quote_item_name": quote_item_name,
            "quote_description": quote_description,
            "quote_subtotal": quote_subtotal,
            "quote_discount": quote_discount,
            "quote_total": quote_total,
            "selected_type": selected_type,
            "selected_size": selected_size,
            "quote_order_number": quote_order_number,
            "stripe_public_key": stripe_public_key,
            "client_secret": payment_intent.client_secret,
        }

        return render(request, template, context)

    def post(self, request):
        stripe_public_key = settings.STRIPE_PUBLIC_KEY
        stripe_secret_key = settings.STRIPE_SECRET_KEY

        quote_order_number = request.session["quote_request_number"]

        form = QuoteOrderForm(request.POST)
        form.instance.user = UserProfile.objects.get(user=self.request.user)
        form.instance.name = request.POST["name"]
        form.instance.email = request.POST["email"]
        form.instance.quote_request_name = request.session["quote_item_name"]
        form.instance.type = request.session["selected_type"]
        form.instance.size = request.session["selected_size"]
        form.instance.description = request.session["quote_description"]
        form.instance.subtotal = request.session["quote_subtotal"]
        form.instance.discount = request.session["quote_discount"]
        form.instance.total = request.session["quote_total"]
        form.instance.quote_order_number = (
            request.session["quote_request_number"]
        )

        if form.is_valid():
            form.save()
            # send email
            quote_order = get_object_or_404(
                QuoteOrder, quote_order_number=form.instance.quote_order_number
            )
            cust_email = quote_order.email
            subject = render_to_string(
                "quotes/confirmation_emails/confirmation_email_subject.txt",
                {"quote_order": quote_order},
            )
            body = render_to_string(
                "quotes/confirmation_emails/confirmation_email_body.txt",
                {
                    "quote_order": quote_order,
                    "contact_email": settings.DEFAULT_FROM_EMAIL,
                },
            )

            send_mail(subject, body, settings.DEFAULT_FROM_EMAIL, [cust_email])
            return redirect(
                reverse("quote_checkout_success", args=[quote_order_number])
            )
        else:
            messages.error(
                request,
                "There was an error with your form. \
            Please double check your information.",
            )


class QuoteCheckoutSuccess(View):
    """A view to handle successful quote request checkouts"""

    def get(self, request, quote_order_number):
        quote_order = get_object_or_404(
            QuoteOrder, quote_order_number=quote_order_number
        )
        if not (
            self.request.user.is_superuser or
            self.request.user == quote_order.user.user
        ):
            messages.error(
                request,
                "You are not authorised to view this page!"
            )
            return HttpResponseRedirect(reverse("home"))
        messages.success(
            request,
            f"Order successfuly processed! \
            Your order number is {quote_order_number}. A confirmation \
            email will be sent to {quote_order.email}.",
        )

        template = "quotes/quote_checkout_success.html"
        context = {"quote_order": quote_order}
        return render(request, template, context)


class QuoteHistoryView(LoginRequiredMixin, TemplateView):
    """A view to list a users quote request history"""

    template_name = "quotes/quote_history.html"

    def get_context_data(self, **kwargs):
        context = super(QuoteHistoryView, self).get_context_data(**kwargs)
        profile = get_object_or_404(UserProfile, user=self.request.user)
        quote_orders = profile.quoteorder_set.all()
        context["quote_orders"] = quote_orders
        return context


class QuoteHistoryDetail(UserPassesTestMixin, TemplateView):
    """A view to display a specific user quote request in more detail"""

    template_name = "quotes/quote_checkout_success.html"

    def get_context_data(self, quote_order_number, **kwargs):
        context = super(QuoteHistoryDetail, self).get_context_data(**kwargs)
        quote_order = get_object_or_404(
            QuoteOrder, quote_order_number=quote_order_number
        )

        messages.info(
            self.request,
            (
                f"This is a past confirmation for quote\
                    order number {quote_order_number}. "
                "A confirmation email was sent on the order date."
            ),
        )
        context["quote_order"] = quote_order
        context["from_quote_history"] = True
        return context

    # restrict access mixin from
    # https://stackoverflow.com/questions/58217055/
    # how-can-i-restrict-access-to-a-view-to-only-super-users-in-django
    def test_func(self):
        quote_order_number = self.kwargs.get("quote_order_number")
        quote_order = get_object_or_404(
            QuoteOrder, quote_order_number=quote_order_number
        )
        return (
            self.request.user.is_superuser or
            self.request.user == quote_order.user.user
        )


class SuperUserCheck(UserPassesTestMixin, View):
    """
    A CBV mixin to prevent access from users
    that are not superusers
    From https://stackoverflow.com/questions/67351312/
    django-check-if-superuser-in-class-based-view

    """

    def test_func(self):
        return self.request.user.is_superuser


class QuoteOrderList(SuperUserCheck, ListView):
    """A view to list all the customer quote orders for the admin"""

    model = QuoteOrder
    template_name = "quotes/quote_order_list.html"
    context_object_name = "quote_orders"


class QuoteOrderFufillCreate(SuperUserCheck, CreateView):
    """
    A view to display an individual customer quote order
    and upload a graphic design for the customer to download
    """

    model = QuoteFufillment
    template_name = "quotes/quote_fufillment.html"
    success_url = reverse_lazy("quote_orders")
    form_class = QuoteFufillmentForm

    def get_context_data(self, **kwargs):
        context = super(
            QuoteOrderFufillCreate,
            self
            ).get_context_data(**kwargs)
        quote_order = QuoteOrder.objects.get(
            quote_order_number=self.kwargs["quote_order_number"]
        )
        context["quote_order"] = quote_order
        return context

    def form_valid(self, form):
        form.instance.quote_order = QuoteOrder.objects.get(
            quote_order_number=self.kwargs["quote_order_number"]
        )
        status = form.cleaned_data["status"]
        if status:
            quote_order = QuoteOrder.objects.get(
                quote_order_number=self.kwargs["quote_order_number"]
            )
            cust_email = quote_order.email
            subject = render_to_string(
                "quotes/confirmation_emails/confirmation_email_subject_quote_fufillment.txt",
                {"quote_order": quote_order},
            )
            body = render_to_string(
                "quotes/confirmation_emails/confirmation_email_body_quote_fufillment.txt",
                {
                    "quote_order": quote_order,
                    "contact_email": settings.DEFAULT_FROM_EMAIL,
                },
            )

            send_mail(subject, body, settings.DEFAULT_FROM_EMAIL, [cust_email])
        return super().form_valid(form)


class QuoteOrderFufillUpdate(SuperUserCheck, UpdateView):
    """
    A view to display an individual customer quote order
    and change the uploaded graphic design for the customer to download
    """

    model = QuoteFufillment
    template_name = "quotes/quote_fufillment.html"
    success_url = reverse_lazy("quote_orders")
    form_class = QuoteFufillmentForm

    def get_object(self):
        quote_order = QuoteOrder.objects.get(
            quote_order_number=self.kwargs["quote_order_number"]
        )
        return quote_order.quote_order_set

    def get_context_data(self, **kwargs):
        context = super(
            QuoteOrderFufillUpdate,
            self
            ).get_context_data(**kwargs)
        quote_order = QuoteOrder.objects.get(
            quote_order_number=self.kwargs["quote_order_number"]
        )
        context["quote_order"] = quote_order
        return context

    def form_valid(self, form):
        status = form.cleaned_data["status"]
        if status:
            quote_order = QuoteOrder.objects.get(
                quote_order_number=self.kwargs["quote_order_number"]
            )
            cust_email = quote_order.email
            subject = render_to_string(
                "quotes/confirmation_emails/confirmation_email_subject_quote_fufillment.txt",
                {"quote_order": quote_order},
            )
            body = render_to_string(
                "quotes/confirmation_emails/confirmation_email_body_quote_fufillment.txt",
                {
                    "quote_order": quote_order,
                    "contact_email": settings.DEFAULT_FROM_EMAIL,
                },
            )

            send_mail(subject, body, settings.DEFAULT_FROM_EMAIL, [cust_email])
        return super().form_valid(form)
