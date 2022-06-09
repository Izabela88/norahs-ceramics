from django.views import View
from django.shortcuts import render, get_object_or_404
from django.http import HttpResponseRedirect, HttpRequest, HttpResponse
from basket.models import Basket, BasketProduct
from django.urls import reverse


class BasketView(View):
    def get(self, request: HttpRequest) -> HttpResponse:
        context = {}
        # if not request.user.is_authenticated:
        #     return render(request, "401.html")

        if request.user:
            basket = request.user.get_or_create_user_basket()
        else:
            basket = Basket().save()
        context = {
            "basket_products": basket.basket_products.all()
        }
        return render(request, "basket/basket.html", context)


class AddToBasketView(View):
    def post(self, request, product_id):

        if request.user:
            basket = request.user.get_or_create_user_basket()
        else:
            basket = Basket().save()

        basket.add_product(product_id=product_id)

        return HttpResponseRedirect(
            reverse("basket")
        )
