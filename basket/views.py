from django.views import View
from django.shortcuts import render, get_object_or_404
from django.http import HttpResponseRedirect, HttpRequest, HttpResponse
from basket.models import Basket
from django.urls import reverse
import sweetify


class BasketView(View):
    def get(self, request: HttpRequest) -> HttpResponse:
        context = {}
        basket = Basket.get_basket(request)
        basket_summary = basket.basket_summary()
        context = {
            "basket_products": basket_summary.sorted_products,
            "sum_products_qty": basket_summary.total_qty,
            "total_basket_price": basket.total_basket_price,
        }
        return render(request, "basket/basket.html", context)


class AddToBasketView(View):
    def post(self, request, product_id):
        basket = Basket.get_basket(request)
        basket.add_product(product_id=product_id)
        sweetify.toast(
            self.request,
            "the product has been successfully added to the basket",
            timer=2500,
            position="top",
            
        )
        return HttpResponseRedirect(request.META.get("HTTP_REFERER"))


class SubtractFromBasketView(View):
    def post(self, request, product_id):
        basket = Basket.get_basket(request)
        basket.subtract_product(product_id=product_id)
        sweetify.toast(
            self.request,
            "the product has been successfully removed from the basket",
            timer=2500,
            position="top",
        )
        return HttpResponseRedirect(reverse("basket"))


class DeleteFromBasketView(View):
    def post(self, request, product_id):
        basket = Basket.get_basket(request)
        basket.delete_product(product_id=product_id)
        sweetify.toast(
            self.request,
            "the products has been successfully removed from the basket",
            timer=2500,
            position="top",
        )
        return HttpResponseRedirect(reverse("basket"))
