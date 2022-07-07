from django.db import models
from customer.models import User
from product.models import Product
from norahs_ceramics.model_mixin import TimestapModel


class ProductReview(TimestapModel):
    TYPE_SELECT = (
        (1, 1),
        (2, 2),
        (3, 3),
        (4, 4),
        (5, 5),
    )
    product = models.ForeignKey(
        Product,
        on_delete=models.CASCADE,
        null=False,
        related_name="product_reviews",
    )
    reviewer = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        null=False,
        related_name="product_reviews",
    )
    description = models.TextField(blank=False, null=False, default="")
    stars = models.IntegerField(choices=TYPE_SELECT, blank=False, null=False)
    is_visible = models.BooleanField(null=False, default=False)
    is_admin_approved = models.BooleanField(null=False, default=False)

    @property
    def reviews_rating(self) -> tuple[float, int]:
        """Return user avarage reviews rating

        Returns:
            tuple[float, int]: Avarage rating and number of reviews
        """
        reviews = self.product_reviews.filter(
            is_admin_approved=True, is_visible=True
        )
        ratings = [i.stars for i in reviews]
        try:
            avg_rating = round(sum(ratings) / len(reviews))
        except ZeroDivisionError:
            avg_rating = 0
        return avg_rating, len(reviews)
