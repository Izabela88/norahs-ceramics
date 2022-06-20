from django.urls import path
from product.views import CheckoutView


urlpatterns = [
    path("", CheckoutView.as_view(), name="checkout"),
]
