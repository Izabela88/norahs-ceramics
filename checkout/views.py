from django.shortcuts import render, redirect
from django.views import View
from basket.models import Basket
from django.http import HttpResponseRedirect, HttpResponse
from django.urls import reverse
import sweetify
from django.conf import settings  # new
from django.http import JsonResponse
from django.views import View
from django.views.generic.base import TemplateView

from django.contrib.auth.decorators import login_required
import stripe
from django.http import HttpRequest, JsonResponse
from django.views.decorators.csrf import csrf_exempt
from checkout.forms import PersonalInformationForm, ShippingAddressForm
from customer.forms import AddressForm


class CheckoutView(View):
    def get(self, request):

        basket = Basket.get_basket(request)

        if not basket.basket_products.count():
            sweetify.toast(
                self.request,
                "your basket is empty!",
                timer=2500,
                position="top",
            )
            return HttpResponseRedirect(reverse("home"))

        else:
            basket_summary = basket.basket_summary()

        checkout_products = []
        for product_summary in basket_summary.sorted_products:
            checkout_product_data = {
                "name": product_summary["product"].name,
                "quantity": product_summary["qty"],
                "currency": "gbp",
                "amount": product_summary["total_product_price"],
            }
            checkout_products.append(checkout_product_data)
        request.session["checkout_products"] = checkout_products
        context = {
            "checkout_products": basket_summary.sorted_products,
            "total_checkout_price": basket.total_basket_price,
            "vat_amount": basket_summary.vat_amount,
        }
        return render(request, "checkout/checkout.html", context)


@csrf_exempt
def create_checkout_session(request):
    if request.method == "POST":
        domain_url = "http://localhost:8000/"
        stripe.api_key = settings.STRIPE_SECRET_KEY
        checkout_products = request.session["checkout_products"]
        try:
            checkout_session = stripe.checkout.Session.create(
                billing_address_collection="auto",
                shipping_options=[
                    {
                        "shipping_rate_data": {
                            "type": "fixed_amount",
                            "fixed_amount": {
                                "amount": 0,
                                "currency": "gbp",
                            },
                            "display_name": "Free shipping",
                            # Delivers between 5-7 business days
                            "delivery_estimate": {
                                "minimum": {
                                    "unit": "business_day",
                                    "value": 3,
                                },
                                "maximum": {
                                    "unit": "business_day",
                                    "value": 5,
                                },
                            },
                        }
                    },
                    {
                        "shipping_rate_data": {
                            "type": "fixed_amount",
                            "fixed_amount": {
                                "amount": 500,
                                "currency": "gbp",
                            },
                            "display_name": "Next day delivery",
                            # Delivers in exactly 1 business day
                            "delivery_estimate": {
                                "minimum": {
                                    "unit": "business_day",
                                    "value": 1,
                                },
                                "maximum": {
                                    "unit": "business_day",
                                    "value": 1,
                                },
                            },
                        }
                    },
                ],
                shipping_address_collection={
                    "allowed_countries": ["GB"],
                },
                success_url=domain_url
                + "checkout/success?session_id={CHECKOUT_SESSION_ID}",
                cancel_url=domain_url + "checkout/",
                payment_method_types=["card"],
                mode="payment",
                line_items=checkout_products,
            )
        except Exception as e:
            return HttpResponse(e)
        return redirect(checkout_session.url, code=303)


class SuccessView(TemplateView):
    template_name = "checkout/success.html"


class CancelledView(TemplateView):
    template_name = "checkout/checkout.html"

    def get(self, request, *args, **kwargs):
        return HttpResponseRedirect(reverse("checkout"))
