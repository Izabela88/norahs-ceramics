from django.db import models
from django.core.validators import MaxValueValidator, MinValueValidator
from norahs_ceramics.fields import CaseInsensitiveCharField
from norahs_ceramics.model_mixin import TimestapModel
from django.core.exceptions import ValidationError


class Category(TimestapModel):
    name = models.CharField(max_length=30, primary_key=True)


class SubCategory(TimestapModel):
    name = models.CharField(max_length=30, primary_key=True)
    category = models.ForeignKey(
        Category, on_delete=models.CASCADE, related_name="parent_category"
    )


class Product(TimestapModel):
    name = CaseInsensitiveCharField(max_length=100)
    slug = CaseInsensitiveCharField(max_length=200, unique=True)
    price_pence = models.DecimalField(
        max_digits=6, decimal_places=2, validators=[MinValueValidator(0.00)]
    )
    description = models.TextField(max_length=2000)
    short_description = models.TextField(max_length=1000)
    is_active = models.BooleanField(default=False)
    is_featured = models.BooleanField(default=False)
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
    sub_category = models.ForeignKey(
        SubCategory, on_delete=models.CASCADE, related_name="sub_category"
    )

    def validate_image(self):
        # https://stackoverflow.com/questions/6195478/max-image-size-on-file-upload
        filesize = self.file.size
        megabyte_limit = 0.4
        if filesize > megabyte_limit * 1024 * 1024:
            raise ValidationError(
                "Image is too big. Max file size is %sMB" % str(megabyte_limit)
            )
    image = models.ImageField(
        upload_to="product_images/",
        null=True,
        blank=True,
        validators=[validate_image],
    )


class Color(TimestapModel):
    name = models.CharField(max_length=30, primary_key=True, unique=True)


class ProductColor(TimestapModel):
    product = models.ForeignKey(
        Product, on_delete=models.CASCADE, related_name="product"
    )
    color = models.ForeignKey(Color, on_delete=models.CASCADE, related_name="color")
