from django.shortcuts import render, redirect, get_object_or_404
from django.views import View
from basket.models import Basket
from django.http import HttpResponseRedirect, HttpResponse
from django.urls import reverse
import sweetify
from django.conf import settings  # new
from django.http import JsonResponse
from django.views import View
from django.views.generic.base import TemplateView
from django.utils.decorators import method_decorator
from django.contrib.auth.decorators import login_required
import stripe
from django.http import HttpRequest, JsonResponse
from django.views.decorators.csrf import csrf_exempt
from checkout.forms import PersonalInformationForm, ShippingAddressForm
from customer.forms import AddressForm
from order.models import Order, OrderProduct
from order.data_objects import OrderStatus


class OrderSummaryView(View):
    def get(self, request):
        if request.session.pop("cancel_message", None):
            sweetify.toast(
                request,
                "the payment process has been canceled!",
                timer=4500,
                position="top",
                icon="error",
            )
        basket = Basket.get_basket(request)
        if not basket.basket_products.count():
            sweetify.toast(
                self.request,
                "your basket is empty!",
                timer=2500,
                position="top",
                icon="info",
            )
            return HttpResponseRedirect(reverse("home"))

        else:
            basket_summary = basket.basket_summary()

        checkout_products = {"line_items": [], "product_ids": []}
        for product_summary in basket_summary.sorted_products:
            line_item = {
                "name": product_summary["product"].name,
                "quantity": product_summary["qty"],
                "currency": "gbp",
                "amount": product_summary["product"].price_pence,
            }
            checkout_products["line_items"].append(line_item)
            for _ in range(product_summary["qty"]):
                checkout_products["product_ids"].append(
                    product_summary["product"].id
                )
        request.session["checkout_products"] = checkout_products
        request.session["basket_id"] = str(basket.id)

        context = {
            "checkout_products": basket_summary.sorted_products,
            "total_checkout_price": basket.total_basket_price,
            "vat_amount": basket_summary.vat_amount,
        }
        return render(request, "checkout/checkout.html", context)


stripe.api_key = settings.STRIPE_SECRET_KEY


@csrf_exempt
def create_checkout_session(request):
    if request.method == "POST":
        domain_url = "http://localhost:8000/"
        try:
            checkout_products = request.session["checkout_products"]
            basket_id = request.session["basket_id"]

        except KeyError as e:
            return HttpResponseRedirect(reverse("home"))
        basket = Basket.objects.filter(id=basket_id).first()
        if not basket:
            sweetify.toast(
                request,
                "the basket is empty!",
                timer=2500,
                position="top",
                icon="info",
            )
            return HttpResponseRedirect(reverse("home"))
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
                + "checkout/success/{CHECKOUT_SESSION_ID}",
                cancel_url=domain_url + "checkout/cancel",
                payment_method_types=["card"],
                mode="payment",
                line_items=checkout_products["line_items"],
            )
        except Exception as e:
            return HttpResponse(e)

        return redirect(checkout_session.url, code=303)


class SuccessView(View):
    def get(self, request, session_id):
        context = {}
        session = stripe.checkout.Session.retrieve(session_id)
        context["customer"] = stripe.Customer.retrieve(session.customer)

        try:
            checkout_products = request.session["checkout_products"]
            basket_id = request.session["basket_id"]

        except KeyError as e:
            sweetify.toast(
                request,
                "no products in the basket!",
                timer=2500,
                position="top",
                icon="info",
            )
            return HttpResponseRedirect(reverse("home"))
        if request.user.is_authenticated:
            order_user = request.user
        else:
            order_user = None
        order = Order.objects.create(
            user=order_user,
            status=OrderStatus.PAID.value,
            bill_pence=sum(
                [i["amount"] for i in checkout_products["line_items"]]
            ),
            transaction_id=session["payment_intent"],
        )
        for product_id in checkout_products["product_ids"]:
            OrderProduct.objects.create(
                order_id=order.id, product_id=product_id
            )
        basket_id = request.session["basket_id"]
        basket = Basket.objects.filter(id=basket_id).first()
        if basket:
            basket.delete()
            request.session.pop("checkout_products", None)
            request.session.pop("basket_id", None)
        order = Order.objects.first()
        context["order"] = order
        return render(request, "checkout/success.html", context)


class CancelledView(TemplateView):
    template_name = "checkout/checkout.html"

    def get(self, request, *args, **kwargs):
        request.session["cancel_message"] = True
        return HttpResponseRedirect(reverse("checkout"))