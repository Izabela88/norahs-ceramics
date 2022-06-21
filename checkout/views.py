from django.shortcuts import render
from django.views import View
from basket.models import Basket
from django.http import HttpResponseRedirect
from django.urls import reverse
import sweetify


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

        context = {
            "checkout_products": basket_summary.sorted_products,
            "total_checkout_price": basket.total_basket_price,
            "vat_amount": basket_summary.vat_amount,
        }

        return render(request, "checkout/checkout.html", context)
