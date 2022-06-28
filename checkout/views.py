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
from django.utils.decorators import method_decorator
from django.contrib.auth.decorators import login_required
import stripe
from django.http import HttpRequest, JsonResponse
from django.views.decorators.csrf import csrf_exempt
from checkout.forms import PersonalInformationForm, ShippingAddressForm
from customer.forms import AddressForm
from order.models import Order, OrderProduct
from order.data_objects import OrderStatus


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


@csrf_exempt
def create_checkout_session(request):
    if request.method == "POST":
        domain_url = "http://localhost:8000/"
        stripe.api_key = settings.STRIPE_SECRET_KEY
        try:
            checkout_products = request.session["checkout_products"]
            basket_id = request.session["basket_id"]

        except KeyError as e:
            return HttpResponseRedirect(reverse("home"))
        basket = Basket.objects.filter(id=basket_id).first()
        if not basket:
            sweetify.toast(
                request,
                "no basket!",
                timer=2500,
                position="top",
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
                + "checkout/success?session_id={CHECKOUT_SESSION_ID}",
                cancel_url=domain_url + "checkout/",
                payment_method_types=["card"],
                mode="payment",
                line_items=checkout_products["line_items"],
            )
        except Exception as e:
            return HttpResponse(e)
        if request.user.is_authenticated:
            order_user = request.user
        else:
            order_user = None
        order = Order.objects.create(
            user=order_user,
            status=OrderStatus.PENDING.value,
            bill_pence=sum(
                [i["amount"] for i in checkout_products["line_items"]]
            ),
            transaction_id=checkout_session["payment_intent"],
        )
        for product_id in checkout_products["product_ids"]:
            OrderProduct.objects.create(
                order_id=order.id, product_id=product_id
            )

        # basket.delete()
        # request.session.pop("checkout_products", None)
        # request.session.pop("basket_id", None)
        return redirect(checkout_session.url, code=303)


class SuccessView(TemplateView):
    template_name = "checkout/success.html"


class CancelledView(TemplateView):
    template_name = "checkout/checkout.html"

    def get(self, request, *args, **kwargs):
        return HttpResponseRedirect(reverse("checkout"))


endpoint_secret = settings.STRIPE_WEBHOOK_KEY


@csrf_exempt
def my_webhook_view(request):
    payload = request.body
    sig_header = request.META["HTTP_STRIPE_SIGNATURE"]
    event = None

    try:
        event = stripe.Webhook.construct_event(
            payload, sig_header, endpoint_secret
        )
    except ValueError as e:
        # Invalid payload
        return HttpResponse(status=400)
    except stripe.error.SignatureVerificationError as e:
        # Invalid signature
        return HttpResponse(status=400)

    # Handle the checkout.session.completed event
    if event["type"] == "checkout.session.completed":
        session = event["data"]["object"]

        # Save an order in your database, marked as 'awaiting payment'
        create_order(session)

        # Check if the order is already paid (for example, from a card payment)
        #
        # A delayed notification payment will have an `unpaid` status, as
        # you're still waiting for funds to be transferred from the customer's
        # account.
        if session.payment_status == "paid":
            # Fulfill the purchase
            fulfill_order(session)

    elif event["type"] == "checkout.session.async_payment_succeeded":
        session = event["data"]["object"]

        # Fulfill the purchase
        fulfill_order(session)

    elif event["type"] == "checkout.session.async_payment_failed":
        session = event["data"]["object"]

        # Send an email to the customer asking them to retry their order
        email_customer_about_failed_payment(session)

    # Passed signature verification
    return HttpResponse(status=200)


def fulfill_order(session):
    # TODO: fill me in
    print("Fulfilling order")


def create_order(session):
    # TODO: fill me in
    print("Creating order")


def email_customer_about_failed_payment(session):
    # TODO: fill me in
    print("Emailing customer")
