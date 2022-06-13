from django.urls import path
from basket.views import (
    BasketView,
    AddToBasketView,
    SubtractFromBasketView,
    DeleteFromBasketView,
)



urlpatterns = [
    path("", BasketView.as_view(), name="basket"),
    path(
        "<int:product_id>/add", AddToBasketView.as_view(), name="add_to_basket"
    ),
    path(
        "<int:product_id>/subtract",
        SubtractFromBasketView.as_view(),
        name="subtract_from_basket",
    ),
    path(
        "<int:product_id>/delete",
        DeleteFromBasketView.as_view(),
        name="delete_from_basket",
    ),

]
