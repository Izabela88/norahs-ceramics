from django.db import models
from django.core.validators import MaxValueValidator, MinValueValidator
from norahs_ceramics.fields import CaseInsensitiveCharField
from norahs_ceramics.model_mixin import TimestapModel


class Category(TimestapModel):
    name = models.CharField(max_length=30, primary_key=True)


class SubCategory(TimestapModel):
    name = models.CharField(max_length=30, primary_key=True)
    category_id = models.ForeignKey(
        Category, on_delete=models.CASCADE, related_name="parent_category"
    )


class Product(TimestapModel):
    name = CaseInsensitiveCharField(max_length=100)
    slug = CaseInsensitiveCharField(max_length=200)
    price_pence = models.DecimalField(
        max_digits=6, decimal_places=2, validators=[MinValueValidator(0.00)]
    )
    description = models.TextField(max_length=2000)
    short_description = models.TextField(max_length=1000)
    is_active = models.BooleanField(null=True)
    is_featured = models.BooleanField(null=True)
    width_cm = models.PositiveIntegerField(
        null=True,
        blank=True,
        validators=[MinValueValidator(1)],
    )
    height_cm = models.PositiveIntegerField(
        null=True,
        blank=True,
        validators=[MinValueValidator(1)],
    )
    length_cm = models.PositiveIntegerField(
        null=True,
        blank=True,
        validators=[MinValueValidator(1)],
    )
    volume_ml = models.PositiveIntegerField(
        null=True,
        blank=True,
        validators=[MinValueValidator(1)],
    )
    category = models.ForeignKey(
        Category, on_delete=models.CASCADE, related_name="category"
    )


class Color(TimestapModel):
    name = models.CharField(max_length=30, primary_key=True)


class ProductColor(TimestapModel):
    product = models.ForeignKey(
        Product, on_delete=models.CASCADE, related_name="product"
    )
    color = models.ForeignKey(Color, on_delete=models.CASCADE, related_name="color")
