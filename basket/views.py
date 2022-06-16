from django.views import View
from django.shortcuts import render, get_object_or_404
from django.http import HttpResponseRedirect, HttpRequest, HttpResponse
from basket.models import Basket, BasketProduct
from django.urls import reverse
from django.contrib import messages
import sweetify


class BasketView(View):
    def get(self, request: HttpRequest) -> HttpResponse:
        context = {}

        basket = Basket.get_basket(request)
        if basket.basket_products:
            basket_products = basket.basket_products.all()
        else:
            basket_products = []

        products_with_qty = {}

        for basket_product in basket_products:
            if basket_product.product_id in products_with_qty:
                products_with_qty[basket_product.product_id]["qty"] += 1
                products_with_qty[basket_product.product_id][
                    "total_product_price"
                ] = (
                    basket_product.product.price_pence
                    * products_with_qty[basket_product.product_id]["qty"]
                )
            else:
                products_with_qty[basket_product.product_id] = {
                    "product": basket_product.product,
                    "total_product_price": basket_product.product.price_pence,
                    "qty": 1,
                }
        sorted_products = sorted(
            list(products_with_qty.values()), key=lambda x: x["product"].name
        )
        context = {
            "basket_products": sorted_products,
            "sum_products_qty": basket.total_basket_products_qty(),
            "total_basket_price": basket.total_basket_price(),
        }
        return render(request, "basket/basket.html", context)


class AddToBasketView(View):
    def post(self, request, product_id):
        basket = Basket.get_basket(request)
        basket.add_product(product_id=product_id)
        sweetify.toast(self.request, "product added successfully")
        return HttpResponseRedirect(request.META.get("HTTP_REFERER"))


class SubtractFromBasketView(View):
    def post(self, request, product_id):
        basket = Basket.get_basket(request)
        basket.subtract_product(product_id=product_id)
        sweetify.toast(self.request, "product removed successfully")
        return HttpResponseRedirect(reverse("basket"))


class DeleteFromBasketView(View):
    def post(self, request, product_id):
        basket = Basket.get_basket(request)
        basket.delete_product(product_id=product_id)
        sweetify.toast(self.request, "products removed successfully")
        return HttpResponseRedirect(reverse("basket"))
