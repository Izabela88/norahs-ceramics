from django.db import models
from norahs_ceramics.model_mixin import TimestapModel
from customer.models import User, AddressDetails
from product.models import Product


class Order(TimestapModel):
    user = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        null=True,
        related_name="orders",
    )
    status = models.CharField(max_length=300, null=False)
    bill_pence = models.IntegerField()
    transaction_id = models.CharField(max_length=300)


class OrderProduct(TimestapModel):
    order = models.ForeignKey(
        Order,
        on_delete=models.CASCADE,
        null=False,
        related_name="order_products",
    )
    product = models.ForeignKey(
        Product,
        on_delete=models.CASCADE,
        null=False,
        related_name="order_products",
    )
