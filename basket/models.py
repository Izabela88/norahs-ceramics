from django.db import models
from norahs_ceramics.model_mixin import TimestapModel
from customer.models import User
from uuid import uuid4
from product.models import Product
from collections import namedtuple

BasketSummary = namedtuple(
    "BasketSummary",
    ["total_qty", "total_price", "sorted_products", "vat_amount"],
)


class Basket(TimestapModel):
    id = models.UUIDField(primary_key=True, default=uuid4, editable=False)
    customer = models.ForeignKey(
        User, on_delete=models.CASCADE, related_name="customer", null=True
    )

    def add_product(self, product_id):
        basket_product = BasketProduct(
            product_id=product_id, basket_id=self.id
        )
        basket_product.save()

    def subtract_product(self, product_id):
        basket_product = BasketProduct.objects.filter(
            product_id=product_id, basket_id=self.id
        ).first()
        if basket_product:
            basket_product.delete()

    def delete_product(self, product_id):
        basket_products = BasketProduct.objects.filter(
            product_id=product_id, basket_id=self.id
        ).all()

        if basket_products:
            basket_products.all().delete()

    def total_basket_price(self):
        basket_products = BasketProduct.objects.filter(basket_id=self.id).all()
        total_price_pence = 0
        for basket_product in basket_products:
            total_price_pence += basket_product.product.price_pence
        return total_price_pence

    def total_basket_products_qty(self):
        basket_products = BasketProduct.objects.filter(basket_id=self.id).all()
        return len(basket_products)

    @classmethod
    def get_basket(cls, request):
        if request.user.is_authenticated:
            basket = request.user.get_or_create_user_basket()
        elif basket_id := request.session.get("basket_id"):
            basket = cls.objects.filter(id=basket_id).first()
            if not basket:
                basket = cls()
                basket.save()
            request.session["basket_id"] = str(basket.id)
        else:
            basket = cls()
            basket.save()
            request.session["basket_id"] = str(basket.id)
        return basket

    def basket_summary(self):
        if self.basket_products:
            basket_products = self.basket_products.all()
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
        total_qty = self.total_basket_products_qty()
        total_price = self.total_basket_price()
        vat_amount = total_price * 0.2
        basket_summary = BasketSummary(
            total_price=total_price,
            total_qty=total_qty,
            sorted_products=sorted_products,
            vat_amount=vat_amount,
        )
        return basket_summary


class BasketProduct(TimestapModel):
    basket = models.ForeignKey(
        Basket,
        on_delete=models.CASCADE,
        related_name="basket_products",
        null=False,
    )
    product = models.ForeignKey(
        Product,
        on_delete=models.CASCADE,
        related_name="basket_products",
        null=False,
    )
