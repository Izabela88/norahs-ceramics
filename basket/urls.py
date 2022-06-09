from django.urls import path
from basket.views import BasketView, AddToBasketView


urlpatterns = [
    path("", BasketView.as_view(), name="basket"),
    path("<int:product_id>/", AddToBasketView.as_view(), name="add_to_basket"),
]
