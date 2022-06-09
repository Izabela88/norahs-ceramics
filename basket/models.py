from django.db import models
from norahs_ceramics.model_mixin import TimestapModel
from customer.models import User
from uuid import uuid4
from product.models import Product


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


class BasketProduct(TimestapModel):
    basket = models.ForeignKey(
        Basket, on_delete=models.CASCADE, related_name="basket", null=False
    )
    product = models.ForeignKey(
        Product,
        on_delete=models.CASCADE,
        related_name="basket_product",
        null=False,
    )
