from django.contrib.auth.models import AbstractUser
from phonenumber_field.modelfields import PhoneNumberField
from norahs_ceramics.model_mixin import TimestapModel
from django.db import models


class User(AbstractUser):
    phone_number = PhoneNumberField(null=True, blank=False, unique=True)
    address_details = models.OneToOneField(
        "AddressDetails", null=True, on_delete=models.CASCADE
    )

    def get_or_create_user_basket(self):
        from basket.models import Basket

        user_basket = (
            Basket.objects.filter(customer_id=self.id)
            .order_by("-created_at")
            .first()
        )
        if not user_basket:
            user_basket = Basket.objects.create(customer_id=self.id)
        return user_basket


class AddressDetails(TimestapModel):
    address_1 = models.CharField(
        verbose_name="Address", max_length=100, null=True
    )
    address_2 = models.CharField(
        verbose_name="Address 1", max_length=100, null=True
    )

    town = models.CharField(
        verbose_name="Town/City", max_length=100, null=True
    )
    postcode = models.CharField(
        verbose_name="Post Code", max_length=8, null=True
    )
    county = models.CharField(verbose_name="County", max_length=100, null=True)
    country = models.CharField(
        verbose_name="Country", max_length=100, null=True
    )
